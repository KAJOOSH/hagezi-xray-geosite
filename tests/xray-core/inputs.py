# SPDX-License-Identifier: GPL-3.0-only

import hashlib
import ipaddress
import json
import mmap
import platform
import re
import shutil
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from zipfile import ZipFile

RELEASES = "https://github.com/XTLS/Xray-core/releases"
DOMAIN_CONTROLS = ("not-in-this-list.invalid", "unlisted-package-probe.example")
IP_CONTROLS = ("192.0.2.183", "198.51.100.191", "2001:db8:ffff::25")


@dataclass(frozen=True)
class Core:
    executable: Path
    version: str
    archive_sha256: str


@dataclass(frozen=True)
class Package:
    category: str
    asset: str
    kind: str
    policy: str
    entries: int
    positives: tuple[str, ...]
    control: str


def fetch(url):
    return urlopen(Request(url, headers={"User-Agent": "hagezi-xray-integration"}), timeout=90)


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def install_latest(runtime):
    with fetch(f"{RELEASES}/latest") as redirect:
        tag_url = urlparse(redirect.geturl())
    match = re.fullmatch(r"/XTLS/Xray-core/releases/tag/(v[0-9.]+)", tag_url.path)
    if tag_url.hostname != "github.com" or not match:
        raise ValueError(f"Unexpected Xray release location: {tag_url.geturl()}")
    version = match[1]
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch = {"amd64": "64", "x86_64": "64", "arm64": "arm64-v8a", "aarch64": "arm64-v8a"}.get(machine)
    if system not in {"windows", "linux"} or not arch:
        raise ValueError(f"No configured Xray release asset for {system}/{machine}")
    asset = f"Xray-{system}-{arch}.zip"
    url = f"{RELEASES}/download/{version}/{asset}"
    with fetch(f"{url}.dgst") as file:
        digest = re.search(rb"(?im)^SHA2?-?256\s*=\s*([a-f0-9]{64})\s*$", file.read(4096))
    if not digest:
        raise ValueError(f"SHA-256 missing from official checksum for {asset}")
    expected = digest[1].decode("ascii").lower()

    directory = runtime / version / f"{system}-{arch}"
    directory.mkdir(parents=True, exist_ok=True)
    archive_path = directory / asset
    if not archive_path.is_file() or sha256(archive_path) != expected:
        with tempfile.TemporaryDirectory(dir=directory) as tmp:
            candidate = Path(tmp) / asset
            with fetch(url) as response, candidate.open("wb") as file:
                shutil.copyfileobj(response, file, 256 * 1024)
            if sha256(candidate) != expected:
                raise ValueError(f"Official archive checksum mismatch for {asset}")
            candidate.replace(archive_path)

    executable = directory / ("xray.exe" if system == "windows" else "xray")
    with ZipFile(archive_path) as archive, archive.open(executable.name) as member, executable.open("wb") as file:
        shutil.copyfileobj(member, file)
    executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
    return Core(executable.resolve(), version, expected)


def read_varint(data, offset):
    number = 0
    for shift in range(0, 70, 7):
        byte = data[offset]
        offset += 1
        number |= (byte & 127) << shift
        if byte < 128:
            return number, offset
    raise ValueError("Malformed GeoData field length")


def inspect_dat(path, category, expected_count):
    with path.open("rb") as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        if data[0] != 10:
            raise ValueError(f"{path.name}: missing GeoData list entry")
        size, position = read_varint(data, 1)
        if position + size != len(data) or data[position] != 10:
            raise ValueError(f"{path.name}: expected one complete GeoData category")
        width, position = read_varint(data, position + 1)
        if data[position : position + width].decode("ascii").casefold() != category:
            raise ValueError(f"{path.name}: category does not match {category}")
        position += width
        count = 0
        while position < len(data):
            if data[position] != 18:
                raise ValueError(f"{path.name}: unexpected GeoData field")
            width, position = read_varint(data, position + 1)
            position += width
            count += 1
        if position != len(data) or count != expected_count:
            raise ValueError(f"{path.name}: expected {expected_count} entries, found {count}")


def load_bundle(directory):
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    data = manifest["packages"]
    names = {package["asset"] for package in data}
    members = {package["source_file"] for package in data}
    if not data or len(names) != len(data) or len(members) != len(data):
        raise ValueError("No packages or duplicate package files in manifest")
    categories = {package["category"] for package in data}
    if len(categories) != len(data) or any(not re.fullmatch(r"[a-z0-9-]+", tag) for tag in categories):
        raise ValueError("Invalid or duplicate Xray categories in manifest")
    if any(not re.fullmatch(r"hagezi-[a-z0-9-]+\.dat", name) for name in names):
        raise ValueError("Unexpected GeoData asset name in manifest")

    checksum_lines = (directory / "checksums.sha256").read_text(encoding="ascii").splitlines()
    checksums = {}
    for line in checksum_lines:
        digest, filename = line.split()
        if filename in checksums or not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise ValueError(f"Invalid checksum entry for {filename}")
        checksums[filename] = digest
    if set(checksums) != names | {"sources.zip"}:
        raise ValueError("Checksum list and package manifest differ")
    for filename, digest in checksums.items():
        if sha256(directory / filename) != digest:
            raise ValueError(f"SHA-256 differs for {filename}")

    packages = []
    with ZipFile(directory / "sources.zip") as sources:
        if set(sources.namelist()) != members or len(sources.namelist()) != len(members):
            raise ValueError("Source archive and package manifest differ")
        for entry in data:
            if (entry["kind"] not in {"domain", "ip"} or entry["policy"] not in {"block", "allow"}
                    or not isinstance(entry["entry_count"], int) or entry["entry_count"] < 1):
                raise ValueError(f"Bad metadata for {entry['asset']}")
            if checksums[entry["asset"]] != entry["asset_sha256"]:
                raise ValueError(f"Manifest SHA-256 differs for {entry['asset']}")
            inspect_dat(directory / entry["asset"], entry["category"], entry["entry_count"])
            with sources.open(entry["source_file"]) as source:
                samples, control, digest = sample_source(source, entry["kind"], entry["entry_count"])
            if digest != entry["source_sha256"]:
                raise ValueError(f"Source SHA-256 differs for {entry['source_file']}")
            packages.append(Package(entry["category"], entry["asset"], entry["kind"], entry["policy"],
                                    entry["entry_count"], samples, control))
    return manifest["version"], packages


def sample_source(source, kind, expected_count):
    digest = hashlib.sha256()
    picks = {1, (expected_count + 1) // 2, expected_count}
    count = 0
    chosen = []
    controls = list(DOMAIN_CONTROLS if kind == "domain" else IP_CONTROLS)
    suffixes = {
        host: {b".".join(host.encode("ascii").split(b".")[i:]) for i in range(len(host.split(".")))}
        for host in DOMAIN_CONTROLS
    }
    addresses = {address: ipaddress.ip_address(address) for address in IP_CONTROLS}
    for raw in source:
        digest.update(raw)
        line = raw.removeprefix(b"\xef\xbb\xbf") if count == 0 else raw
        line = line.strip()
        if not line or line.startswith(b"#"):
            continue
        count += 1
        if kind == "ip":
            prefix = ipaddress.ip_network(line.decode("ascii"), strict=False)
            controls = [address for address in controls if addresses[address] not in prefix]
            if count in picks:
                chosen.extend((str(prefix.network_address), str(prefix.broadcast_address)))
        else:
            domain = line.lower().rstrip(b".")
            if count in picks:
                chosen.append(domain.decode("ascii"))
            controls = [host for host in controls if domain not in suffixes[host]]
    if count < expected_count or not chosen or not controls:
        raise ValueError(f"Source has {count} rows and no usable set of samples for {expected_count} entries")
    if kind == "domain":
        host = next((name for name in chosen if len(name) <= 247), None)
        if host is not None:
            chosen.append(f"probe.{host}")
    return tuple(dict.fromkeys(chosen)), controls[0], digest.hexdigest()
