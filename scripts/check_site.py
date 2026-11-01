#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

EXPECTED = {
    "car-trip", "car", "drifting", "gjovik", "levanger-loop", "oppdal-hike",
    "oppdal-round", "poland-trip", "police-chase", "prague", "sicily",
    "suspension-lab", "vev-vind", "wheels",
}
REQUIRED = {
    "index.html", "styles.css", "app.js", "apps.json", "icon.svg",
    "manifest.webmanifest",
}

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, default=Path("."))
args = parser.parse_args()
root = args.root.resolve()
public = root / "public"

missing = sorted(name for name in REQUIRED if not (public / name).is_file())
assert not missing, f"missing public files: {missing}"
assert (root / "Dockerfile").is_file()
assert (root / "nginx.conf").is_file()

apps = json.loads((public / "apps.json").read_text())
assert isinstance(apps, list)
assert len(apps) == 14
assert {app["slug"] for app in apps} == EXPECTED
assert len({app["url"] for app in apps}) == len(apps)

for app in apps:
    assert set(app) == {"slug", "title", "description", "category", "url", "symbol", "accent"}
    assert app["title"].strip()
    assert len(app["description"]) >= 35
    assert app["category"] in {"Trips", "Playgrounds", "Workshop", "Studio"}
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", app["accent"])
    parsed = urlparse(app["url"])
    expected_path = {"drifting": "/game-drifting/", "sicily": "/sicily/planner/"}.get(app["slug"], f"/{app['slug']}/")
    assert parsed.scheme == "https" and parsed.hostname == "kibk.net"
    assert parsed.path == expected_path

html = (public / "index.html").read_text()
for asset in ("/styles.css", "/app.js", "/icon.svg", "/manifest.webmanifest"):
    assert asset in html
assert 'href="https://kibk.net"' in html
assert 'heimdall.kibk.net' not in html
assert "noindex, nofollow" in html

js = (public / "app.js").read_text()
assert "innerHTML" in js
assert "fetch(\"/apps.json\"" in js
assert "target=\"_blank\"" not in html

nginx = (root / "nginx.conf").read_text()
assert "location = /healthz" in nginx
assert "Content-Security-Policy" in nginx

print("Gallery checks passed: 14 exact applications and required assets validated.")
