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
- The page is PUBLIC and has the text inbox. The inbox API is open to anyone, so
  its limits (honeypot, 5/hour per visitor, 100/day, 20 KB) are load-bearing. Do not loosen them.

## Inbox (paste box)
Paste text on the public page → `POST /p/ideal-government/api/inbox` (Caddy strips the prefix) →
`server/inbox_api.py` on 127.0.0.1:8089 → `~/agent-box/ideal-government/inbox/`.
Read and process with `~/agents/venv/bin/python server/ingest.py list|show <id>|done <id>`. Nothing is deleted;
`done` moves an item to `processed/`. Unit: `deploy/ideal-government-inbox-api.service`.

## Hosting
Published to kunzhub as a **public** page at `/p/ideal-government/`. Source of truth for
the kunzhub copy is `ideal_government.html` in this repo (the only built page). Publish steps are in
`Self-Host/sites/kunzhub` (`scripts/add-page.sh`).

## Exception: public inbox (owner-approved 2026-10-04)
The v2 design brief says the inbox must stay tailnet-only and never go through Caddy or Funnel.
The owner has approved an exception: the inbox is served publicly through Caddy at
`/p/ideal-government/api/*`, because the content is innocuous. The controls are the rate limits
in `server/inbox_api.py` (honeypot, 5/hour per visitor, 100/day, 20 KB). Do not remove them.
