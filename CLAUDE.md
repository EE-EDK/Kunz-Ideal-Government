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
- The builder is stdlib only. The inbox service (`server/inbox_api.py`) uses the
  service venv's FastAPI/uvicorn; tests run with `~/agents/venv/bin/python -m pytest server/tests`.
- The paste box posts to the inbox, so the page that has it must stay private.
  A public variant must be built without the paste section and without any API route.

## Inbox (paste box)
Paste text on the private kunzhub page → `POST /priv/ideal-government/api/inbox` (basicauth,
Caddy strips the prefix) → `server/inbox_api.py` on 127.0.0.1:8089 → `~/agent-box/ideal-government/inbox/`.
Read and process with `python3 server/ingest.py list|show <id>|done <id>`. Nothing is deleted;
`done` moves an item to `processed/`. Unit: `deploy/ideal-government-inbox-api.service`.

## Hosting
Published to kunzhub as a **private** page (basicauth). Source of truth for the
kunzhub copy is `ideal_government.html` in this repo. Publish steps are in
`Self-Host/sites/kunzhub` (`scripts/add-page.sh`).
