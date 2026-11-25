# SPDX-License-Identifier: GPL-3.0-only

import copy
import http.client
import ipaddress
import json
import os
import socket
import struct
import subprocess
import threading
import time
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

LOOPBACK = "127.0.0.1"
TIMEOUT = 15


@dataclass(frozen=True)
class Probe:
    destination: str
    expected: str
    host: str | None = None


class OriginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = self.server.route.encode("ascii")
        self.send_response(200)
        self.send_header("X-Test-Route", self.server.route)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


@contextmanager
def origin(route):
    with ThreadingHTTPServer((LOOPBACK, 0), OriginHandler) as server:
        server.route = route
        worker = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        worker.start()
        try:
            yield server.server_port
        finally:
            server.shutdown()
            worker.join()


def free_ports():
    with socket.socket() as client, socket.socket() as server:
        client.bind((LOOPBACK, 0))
        server.bind((LOOPBACK, 0))
        return client.getsockname()[1], server.getsockname()[1]


def routing_rule(kind, asset, tag, outbound):
    return {"type": "field", kind: [f"ext:{asset}:{tag}"], "outboundTag": outbound}


def receive(sock, size):
    data = b""
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            raise OSError("SOCKS connection closed during handshake")
        data += part
    return data


def socks_destination(target):
    try:
        addr = ipaddress.ip_address(target)
    except ValueError:
        host = target.encode("ascii")
        return b"\x03" + bytes([len(host)]) + host
    return (b"\x01" if addr.version == 4 else b"\x04") + addr.packed


def request(client_port, probe):
    host = probe.host or probe.destination
    if ":" in host:
        host = f"[{host}]"
    with socket.create_connection((LOOPBACK, client_port), timeout=TIMEOUT) as sock:
        sock.sendall(b"\x05\x01\x00")
        if receive(sock, 2) != b"\x05\x00":
            raise ValueError("SOCKS did not accept the loopback client")
        sock.sendall(b"\x05\x01\x00" + socks_destination(probe.destination) + struct.pack("!H", 80))
        version, reply, _, kind = receive(sock, 4)
        if version != 5 or reply != 0:
            raise ValueError(f"SOCKS CONNECT failed with reply {reply}")
        size = {1: 4, 4: 16}.get(kind)
        if kind == 3:
            size = receive(sock, 1)[0]
        if size is None:
            raise ValueError(f"Unknown SOCKS address type {kind}")
        receive(sock, size + 2)
        sock.sendall(f"GET /probe HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode("ascii"))

        with http.client.HTTPResponse(sock) as response:
            response.begin()
            marker = response.getheader("X-Test-Route")
            if response.status == 403 and marker is None:
                return "BLOCK (HTTP 403)"
            if response.status == 200 and marker in {"DIRECT", "ALLOW"} and response.read() == marker.encode("ascii"):
                return f"{marker} (HTTP 200)"
            raise ValueError(f"Unexpected HTTP response: {response.status}, route {marker!r}")


class Lab:
    def __init__(self, executable, work, assets):
        self.executable = executable
        self.work = work
        self.assets = assets
        self.client_port, self.server_port = free_ports()
        templates = Path(__file__).resolve().parent
        self.client = json.loads((templates / "client.json").read_text(encoding="utf-8"))
        self.server = json.loads((templates / "server.json").read_text(encoding="utf-8"))
        self.client["inbounds"][0]["port"] = self.client_port
        self.client["outbounds"][0]["settings"]["port"] = self.server_port
        self.server["inbounds"][0]["port"] = self.server_port
        self.stack = ExitStack()

    def __enter__(self):
        with ExitStack() as stack:
            for outbound in self.server["outbounds"][:2]:
                port = stack.enter_context(origin(outbound["tag"]))
                settings = outbound["settings"]
                settings["redirect"] = f"{LOOPBACK}:{port}"
                settings["finalRules"][0]["port"] = str(port)
            stack.enter_context(self.start("client", self.client, self.client_port, self.assets))
            self.stack = stack.pop_all()
        return self

    def __exit__(self, *exc):
        return self.stack.__exit__(*exc)

    def config_path(self, name, config):
        path = self.work / f"{name}.json"
        path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        return path

    def env(self, assets):
        return {**os.environ, "XRAY_LOCATION_ASSET": str(assets), "xray.location.asset": str(assets)}

    @contextmanager
    def start(self, name, config, port, assets):
        config_path = self.config_path(name, config)
        log_path = self.work / f"{name}.log"
        with log_path.open("wb") as log:
            process = subprocess.Popen(
                [str(self.executable), "run", "-config", str(config_path)],
                cwd=self.work, env=self.env(assets), stdout=log, stderr=subprocess.STDOUT,
            )
            try:
                self.wait_for_listener(process, port)
                yield
            except Exception as error:
                details = log_path.read_text(encoding="utf-8", errors="replace").strip()
                raise RuntimeError(f"{name}: {error}\n{details[-1800:]}".strip()) from error
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()

    def wait_for_listener(self, process, port):
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"Xray stopped before opening loopback port {port} with exit {process.returncode}")
            try:
                with socket.create_connection((LOOPBACK, port), timeout=0.25):
                    return
            except OSError:
                time.sleep(0.05)
        raise TimeoutError(f"Xray did not open loopback port {port}")

    def traffic(self, name, probes, *, rules=None, assets=None, sniff=False, strategy="AsIs", dns=None):
        config = copy.deepcopy(self.server)
        config["routing"]["domainStrategy"] = strategy
        if rules is not None:
            config["routing"]["rules"] = rules
        if sniff:
            config["inbounds"][0]["sniffing"] = {"enabled": True, "destOverride": ["http"], "routeOnly": True}
        if dns is not None:
            config["dns"] = dns

        observations = []
        failures = []
        with self.start(name, config, self.server_port, assets or self.assets):
            for probe in probes:
                label = probe.destination if probe.host is None else f"{probe.destination} with Host {probe.host}"
                try:
                    actual = request(self.client_port, probe)
                except (OSError, ValueError, http.client.HTTPException) as error:
                    failures.append(f"{label} expected {probe.expected}, got {error}")
                    continue
                observations.append(f"{label}: {actual}")
                if not actual.startswith(f"{probe.expected} "):
                    failures.append(f"{label} expected {probe.expected}, got {actual}")
            if failures:
                raise ValueError("\n".join(failures))
        return "\n".join(observations)

    def reject_config(self, name, rules, assets, marker):
        config = copy.deepcopy(self.server)
        config["routing"]["rules"] = rules
        result = subprocess.run(
            [str(self.executable), "run", "-test", "-config", str(self.config_path(name, config))],
            cwd=self.work, env=self.env(assets), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", timeout=60, check=False,
        )
        if result.returncode == 0 or marker.casefold() not in result.stdout.casefold():
            raise ValueError(f"Expected Xray to reject {marker!r}, exit {result.returncode}\n{result.stdout[-1600:]}")
        return f"Rejected by Xray (exit {result.returncode}): {result.stdout.strip().splitlines()[-1]}"
