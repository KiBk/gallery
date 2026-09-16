# Gallery

A private, static catalogue for the small websites hosted under `apps.kibk.net`.
It contains no analytics, accounts, external assets, or application secrets.

## Development

```sh
make check
make serve
```

Open `http://127.0.0.1:8080`. Application metadata lives in
`public/apps.json`; the checker requires the catalogue to contain the exact
inventoried set.

## Release

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
