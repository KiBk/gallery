# GitHub Pages

Website: https://kibk.net/gallery/

Publishing: `.github/workflows/pages.yml` validates the site and deploys the `_site/` artifact from `main`. `pages.json` describes its public inputs; `scripts/build-pages.py` adapts paths for GitHub Pages.

Any container/homelab publishing instructions below are retained as legacy references, not the current deployment procedure.

---

# Gallery

A public, static catalogue of four retained GitHub Pages sites: Convoy Rally,
Police Chase, Suspension Lab and Wheel Bench. Trip sites, Car and Vev & Vind
were removed from the catalogue on 1 November 2026.
It contains no analytics, accounts, external assets, or application secrets.

## Development

```sh
make check
make serve
```

Open `http://127.0.0.1:8080`. Application metadata lives in
`public/apps.json`; the checker requires the catalogue to contain the exact
inventoried set.

## Legacy container release (retired)

The image is built without a local Docker daemon and deployed through Hebe's
digest-pinned, private publishing workflow:

```sh
make login
make push-crane
make publish
make verify
make logout
```

`make verify` checks `/healthz` and compares every public file byte-for-byte
with `https://gallery.apps.kibk.net`.
