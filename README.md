# Ideal Government — Design Web

A constitutional core and six design layers for an "ideal government" system,
each open question tracked as a file with a status. Rendered as a single
self-contained page styled after the Persona Dossier.

## Layout

- `data/layers.json` — the design: layers, items, sub-items, statuses (source of truth)
- `src/build_ideal_government.py` — stdlib-only builder → `ideal_government.html`
- `ideal_government.html` — generated; committed so the kunzhub page can be published from it

## Build

    python3 src/build_ideal_government.py --check   # validate data
    python3 src/build_ideal_government.py           # write ideal_government.html

## Status

v2.3 (2026-10-04): 54 items, 30 resolved. All 30 constitutional items are resolved;
1A is partly done. The v1 content of 2026-06-03 is carried over, then the v2 master
decisions and the owner's master synthesis of 2026-10-04 are applied. The 3D graph is
not carried over. Source records are in `catalog/`.

## Publishing

Published publicly on kunzhub at `/p/ideal-government/`, with the text inbox. The
public exception and the publish steps are in `CLAUDE.md`.
