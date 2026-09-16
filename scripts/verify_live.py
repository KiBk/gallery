#!/usr/bin/env python3
import argparse
import hashlib
import ssl
import urllib.request
from pathlib import Path

FILES = ["index.html", "styles.css", "app.js", "apps.json", "icon.svg", "manifest.webmanifest"]

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, default=Path("."))
parser.add_argument("--url", required=True)
args = parser.parse_args()
public = args.root.resolve() / "public"
base = args.url.rstrip("/")
context = ssl.create_default_context()

def fetch(path: str) -> tuple[int, bytes]:
    request = urllib.request.Request(f"{base}/{path.lstrip('/')}", headers={"User-Agent": "gallery-live-verifier/1"})
    with urllib.request.urlopen(request, timeout=20, context=context) as response:
        return response.status, response.read()

health_status, health = fetch("healthz")
assert health_status == 200 and health == b"ok\n", (health_status, health)

for name in FILES:
    status, live = fetch(name)
    local = (public / name).read_bytes()
    assert status == 200, f"{name}: HTTP {status}"
    assert live == local, f"{name}: live bytes differ ({hashlib.sha256(live).hexdigest()} != {hashlib.sha256(local).hexdigest()})"

print(f"Live verification passed: health and {len(FILES)} files match {base} byte-for-byte.")
