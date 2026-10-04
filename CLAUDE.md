# Ideal Government — CLAUDE.md

## What this is
A design repo, not an app. `data/layers.json` holds the design; the builder
turns it into one HTML page in the persona-dossier style.

## Key commands
    python3 src/build_ideal_government.py --check
    python3 src/build_ideal_government.py

## Rules
- Edit `data/layers.json`, never the generated HTML. Rebuild, then commit both.
- Statuses are one of: `resolved`, `inprogress`, `notstarted`, `flagged`.
- Item and sub-item text is the design's own wording. Do not paraphrase it while
  editing structure; change statuses and add to it deliberately.
- Visual system copies the persona dossier tokens (see `src/build_ideal_government.py`
  CSS). Change the dossier's design in `web/persona-system` first, then mirror here.
- Stdlib only. No build dependencies.

## Hosting
Published to kunzhub as a **private** page (basicauth). Source of truth for the
kunzhub copy is `ideal_government.html` in this repo. Publish steps are in
`Self-Host/sites/kunzhub` (`scripts/add-page.sh`).
