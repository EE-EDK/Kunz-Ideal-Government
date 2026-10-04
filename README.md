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

v1 content carried over from the Drive file `government_web_v1.html` (2026-06-03).
Content is verbatim; the 3D graph is not carried over. 25 of 50 items resolved.

## Publishing

Served privately through kunzhub (`pages/private/ideal-government/`), behind
basicauth. See `CLAUDE.md` for the publish steps.
