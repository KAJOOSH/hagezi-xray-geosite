#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import gzip
import hashlib
import io
import json
import re
import tarfile
import tempfile
from pathlib import Path


ARCHIVE_NAME = "xray-assets.tar.gz"
ASSET_NAME = re.compile(r"hagezi-[a-z0-9-]+\.dat")


def asset_checksums(manifest):
    packages = json.loads(manifest.read_text(encoding="utf-8"))["packages"]
    assets = {}
    for package in packages:
        name, digest = package["asset"], package["asset_sha256"]
        if not ASSET_NAME.fullmatch(name) or name in assets:
            raise ValueError(f"Invalid or duplicate Xray asset: {name}")
        if not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise ValueError(f"Invalid SHA-256 for {name}")
        assets[name] = digest
    if not assets:
        raise ValueError("The manifest contains no Xray assets")
    return assets


def add_member(archive, name, size, data):
    member = tarfile.TarInfo(name)
    member.size = size
    archive.addfile(member, data)


def bundle(assets_dir, manifest, output_dir):
    checksums = asset_checksums(manifest)
    license_text = (Path(__file__).resolve().parents[1] / "LICENSE").read_bytes()
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(dir=output_dir) as temporary:
        path = Path(temporary) / ARCHIVE_NAME
        with path.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=5, mtime=0) as compressed:
            with tarfile.open(mode="w|", fileobj=compressed) as archive:
                for name, expected in sorted(checksums.items()):
                    asset = assets_dir / name
                    with asset.open("rb") as source:
                        actual = hashlib.file_digest(source, "sha256").hexdigest()
                        if actual != expected or asset.stat().st_size == 0:
                            raise ValueError(f"Unexpected data in {name}")
                        source.seek(0)
                        add_member(archive, name, asset.stat().st_size, source)
                sums = "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())).encode("ascii")
                add_member(archive, "checksums.sha256", len(sums), io.BytesIO(sums))
                add_member(archive, "LICENSE", len(license_text), io.BytesIO(license_text))

        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        sidecar = path.with_suffix(path.suffix + ".sha256")
        sidecar.write_text(f"{digest}  {path.name}\n", encoding="ascii", newline="\n")
        size = path.stat().st_size
        path.replace(output_dir / path.name)
        sidecar.replace(output_dir / sidecar.name)

    print(f"Packaged {len(checksums)} verified Xray assets in {ARCHIVE_NAME} ({size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(description="Bundle an existing Xray release candidate")
    parser.add_argument("assets_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    bundle(args.assets_dir, args.manifest or args.assets_dir / "manifest.json", args.output_dir)


if __name__ == "__main__":
    main()
