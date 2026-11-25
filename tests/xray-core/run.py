# SPDX-License-Identifier: GPL-3.0-only

import argparse
import html
import ipaddress
import json
import os
import socket
import subprocess
import tempfile
import time
from pathlib import Path

from inputs import install_latest, load_bundle, sha256
from lab import LOOPBACK, Lab, Probe, routing_rule

TEST_DIR = Path(__file__).resolve().parent


def varint(number):
    encoded = bytearray()
    while number >= 128:
        encoded.append((number & 127) | 128)
        number >>= 7
    encoded.append(number)
    return bytes(encoded)


def bytes_field(number, value):
    return varint((number << 3) | 2) + varint(len(value)) + value


def fixture(path, tag, entries):
    group = bytes_field(1, tag.upper().encode("ascii"))
    for entry in entries:
        group += bytes_field(2, entry)
    path.write_bytes(bytes_field(1, group))


def domain_entry(name):
    return b"\x08\x02" + bytes_field(2, name.encode("ascii"))


def ip_entry(cidr):
    prefix = ipaddress.ip_network(cidr)
    return bytes_field(1, prefix.network_address.packed) + b"\x10" + varint(prefix.prefixlen)


class Report:
    def __init__(self):
        self.core = None
        self.geodata = None
        self.manifest_sha256 = None
        self.packages = 0
        self.cases = []

    def case(self, name, run):
        start = time.monotonic()
        try:
            observed = run()
            passed = True
        except Exception as error:
            observed = str(error) or type(error).__name__
            passed = False
        return self.record(name, passed, observed, time.monotonic() - start)

    def record(self, name, passed, observed, duration=0):
        self.cases.append({"name": name, "passed": passed, "observed": observed, "seconds": round(duration, 3)})
        print(f"{'PASS' if passed else 'FAIL'} {name}", flush=True)
        if not passed:
            print(observed, flush=True)
        return passed

    def write(self, directory):
        passed = sum(case["passed"] for case in self.cases)
        failed = len(self.cases) - passed
        result = {
            "xray_version": self.core.version if self.core else None,
            "xray_archive_sha256": self.core.archive_sha256 if self.core else None,
            "geodata_version": self.geodata,
            "manifest_sha256": self.manifest_sha256,
            "package_count": self.packages,
            "passed": passed,
            "failed": failed,
            "cases": self.cases,
        }
        directory.joinpath("report.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        lines = [
            "# Xray integration results",
            "",
            f"Xray: `{result['xray_version'] or 'unavailable'}`",
            f"GeoData: `{self.geodata or 'unavailable'}`",
            f"Packages: **{self.packages}**",
            f"Cases: **{passed} passed, {failed} failed**",
            "",
            "| Case | Result | Observed |",
            "| --- | --- | --- |",
        ]
        for case in self.cases:
            detail = html.escape(case["observed"]).replace("|", "&#124;").replace("\n", "<br>")
            status = "Pass" if case["passed"] else "Fail"
            lines.append(f"| {case['name']} | {status} | {detail} |")
        markdown = "\n".join(lines) + "\n"
        directory.joinpath("report.md").write_text(markdown, encoding="utf-8")
        if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
            with Path(summary).open("a", encoding="utf-8") as file:
                file.write(markdown)
        print(f"{passed} passed, {failed} failed. Report: {directory / 'report.md'}", flush=True)
        return int(failed != 0)


def exercise_packages(lab, packages, report):
    medium = next(package for package in packages if package.category == "tif-medium")
    baseline = (
        Probe(medium.positives[0], "BLOCK"),
        Probe(medium.control, "DIRECT"),
    )
    if not report.case("Server and client examples over VLESS", lambda: lab.traffic("examples", baseline)):
        return False

    for package in packages:
        expected = "ALLOW" if package.policy == "allow" else "BLOCK"
        probes = [Probe(host, expected) for host in package.positives]
        probes.append(Probe(package.control, "DIRECT"))
        rule = routing_rule(package.kind, package.asset, package.category, expected)
        report.case(
            f"Package {package.category} ({package.entries:,} entries)",
            lambda: lab.traffic(package.category, probes, rules=[rule]),
        )
    return True


def exercise_routing(lab, assets, report):
    denied = "deny.routing.invalid"
    allowed = f"safe.{denied}"
    filename = "sample-domain.dat"
    ip_filename = "sample-ip.dat"
    fixture(assets / filename, "deny", [domain_entry(denied)])
    fixture(assets / "sample-allow.dat", "allow", [domain_entry(allowed)])
    fixture(assets / ip_filename, "ranges", [ip_entry("198.51.100.64/26"), ip_entry("2001:db8:20::/64")])

    block = routing_rule("domain", filename, "deny", "BLOCK")
    allow = routing_rule("domain", "sample-allow.dat", "allow", "ALLOW")
    ip = routing_rule("ip", ip_filename, "ranges", "BLOCK")
    report.case("Allow rule before block rule", lambda: lab.traffic(
        "allow-first", [Probe(allowed, "ALLOW"), Probe(denied, "BLOCK"), Probe(f"not-{denied}", "DIRECT")],
        rules=[allow, block], assets=assets,
    ))
    report.case("Block rule before allow rule", lambda: lab.traffic(
        "block-first", [Probe(allowed, "BLOCK")], rules=[block, allow], assets=assets,
    ))
    report.case("Domain and IP files in one configuration", lambda: lab.traffic(
        "mixed", [Probe(f"sub.{denied}", "BLOCK"), Probe("198.51.100.65", "BLOCK"),
                  Probe(f"{denied}.unrelated.invalid", "DIRECT")],
        rules=[block, ip], assets=assets,
    ))
    report.case("IPv4 CIDR boundaries", lambda: lab.traffic(
        "ipv4", [Probe("198.51.100.64", "BLOCK"), Probe("198.51.100.127", "BLOCK"),
                 Probe("198.51.100.63", "DIRECT"), Probe("198.51.100.128", "DIRECT")],
        rules=[ip], assets=assets,
    ))
    report.case("IPv6 CIDR boundaries", lambda: lab.traffic(
        "ipv6", [Probe("2001:db8:20::", "BLOCK"), Probe("2001:db8:20:0:ffff:ffff:ffff:ffff", "BLOCK"),
                 Probe("2001:db8:1f:ffff::1", "DIRECT"), Probe("2001:db8:20:1::1", "DIRECT")],
        rules=[ip], assets=assets,
    ))
    report.case("IP request with HTTP sniffing disabled", lambda: lab.traffic(
        "sniff-off", [Probe("192.0.2.10", "DIRECT", denied)], rules=[block], assets=assets,
    ))
    report.case("HTTP host detected with routeOnly sniffing", lambda: lab.traffic(
        "sniff-on", [Probe("192.0.2.10", "BLOCK", denied), Probe("192.0.2.10", "DIRECT", "other.invalid")],
        rules=[block], assets=assets, sniff=True,
    ))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as local_dns:
        local_dns.bind((LOOPBACK, 0))
        dns = {
            "hosts": {"blocked.lookup.invalid": "198.51.100.65", "other.lookup.invalid": "198.51.100.1"},
            "servers": [{"address": LOOPBACK, "port": local_dns.getsockname()[1]}],
        }
        for strategy in ("AsIs", "IPIfNonMatch", "IPOnDemand"):
            expected = "DIRECT" if strategy == "AsIs" else "BLOCK"
            report.case(f"DNS routing strategy {strategy}", lambda: lab.traffic(
                f"dns-{strategy}", [Probe("blocked.lookup.invalid", expected), Probe("other.lookup.invalid", "DIRECT")],
                rules=[ip], assets=assets, strategy=strategy, dns=dns,
            ))
        catch_all = {"type": "field", "network": "tcp", "outboundTag": "DIRECT"}
        for strategy, expected in (("IPIfNonMatch", "DIRECT"), ("IPOnDemand", "BLOCK")):
            report.case(f"Catch-all with DNS strategy {strategy}", lambda: lab.traffic(
                f"catch-all-{strategy}", [Probe("blocked.lookup.invalid", expected)],
                rules=[ip, catch_all], assets=assets, strategy=strategy, dns=dns,
            ))

    (assets / "truncated.dat").write_bytes(b"\x0a\x05\x0a")
    (assets / "empty.dat").write_bytes(b"")
    for title, asset, tag, marker in (
        ("Missing data file", "missing.dat", "deny", "missing.dat"),
        ("Unknown category", filename, "not-present", "not-present"),
        ("Truncated data", "truncated.dat", "deny", "truncated.dat"),
        ("Empty data", "empty.dat", "deny", "empty.dat"),
    ):
        report.case(title, lambda: lab.reject_config(
            f"invalid-{asset}", [routing_rule("domain", asset, tag, "BLOCK")], assets, marker,
        ))


def run(args, report):
    report.core = install_latest(args.runtime_dir)
    version = subprocess.run(
        [str(report.core.executable), "version"], capture_output=True, text=True, timeout=15, check=True,
    ).stdout.splitlines()[0]
    if version.split()[1] != report.core.version.removeprefix("v"):
        raise ValueError(f"Unexpected Xray executable version: {version}")
    report.record("Official Xray binary", True, version)

    report.geodata, packages = load_bundle(args.assets_dir)
    report.manifest_sha256 = sha256(args.assets_dir / "manifest.json")
    report.packages = len(packages)
    report.record("Release files and original sources", True, f"SHA-256 and entry counts verified for {len(packages)} packages")

    with tempfile.TemporaryDirectory(prefix="xray-", dir=args.report_dir) as tmp:
        work = Path(tmp).resolve()
        fixtures = work / "fixtures"
        fixtures.mkdir()
        with Lab(report.core.executable, work, args.assets_dir) as lab:
            if exercise_packages(lab, packages, report):
                exercise_routing(lab, fixtures, report)


def main():
    parser = argparse.ArgumentParser(description="Exercise the release with real loopback Xray client/server traffic")
    parser.add_argument("--assets-dir", type=Path, default=Path("dist"), help="generated release bundle")
    parser.add_argument("--runtime-dir", type=Path, default=TEST_DIR / ".runtime", help="verified Xray runtime cache")
    parser.add_argument("--report-dir", type=Path, default=TEST_DIR / ".results", help="Markdown and JSON report directory")
    args = parser.parse_args()
    args.assets_dir = args.assets_dir.resolve()
    args.runtime_dir = args.runtime_dir.resolve()
    args.report_dir = args.report_dir.resolve()
    args.report_dir.mkdir(parents=True, exist_ok=True)
    report = Report()
    try:
        run(args, report)
    except Exception as error:
        report.record("Integration setup", False, str(error) or type(error).__name__)
    return report.write(args.report_dir)


if __name__ == "__main__":
    raise SystemExit(main())
