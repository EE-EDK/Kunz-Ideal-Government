"""Ideal Government inbox: paste text on the kunzhub page, retrieve it later.

Routes only. Caddy serves this under the PUBLIC page at
/p/ideal-government/api/* (prefix stripped), so this service sees /api/inbox.
Anyone can post, so writes are limited: a honeypot field, a per-visitor hourly
cap, a daily total, and a body-size cap (same limits as the Shadowshining form).

Storage (never deleted; processed items are moved, not removed):
    $IG_INBOX_DIR/<id>.json            pending
    $IG_INBOX_DIR/processed/<id>.json  ingested (ingest.py done)
Default IG_INBOX_DIR is ~/agent-box/ideal-government/inbox (0700).
"""
import hashlib
import json
import os
import re
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

MAX_TEXT_CHARS = 20_000
MAX_SOURCE_CHARS = 200
HOURLY_PER_CLIENT = 5
DAILY_TOTAL = 100
ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$")
DEFAULT_DIR = Path.home() / "agent-box" / "ideal-government" / "inbox"

app = FastAPI(title="Ideal Government inbox", docs_url=None, redoc_url=None, openapi_url=None)


def inbox_dir() -> Path:
    # Read per call so tests and the CLI can point elsewhere.
    return Path(os.environ.get("IG_INBOX_DIR", DEFAULT_DIR))


def _ensure_dirs(root: Path) -> None:
    for d in (root, root / "processed"):
        d.mkdir(parents=True, exist_ok=True)
        os.chmod(d, 0o700)


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _summary(data: dict) -> dict:
    return {
        "id": data["id"],
        "received_at": data["received_at"],
        "source": data["source"],
        "chars": len(data["text"]),
    }


class NewItem(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_TEXT_CHARS)
    source: str = Field(default="", max_length=MAX_SOURCE_CHARS)
    website: str = ""  # honeypot: real visitors never see or fill this


@app.get("/healthz")
def healthz():
    return {"ok": True}


def client_ip(request: Request) -> str:
    """Caddy's X-Forwarded-For first hop, else the socket peer. Only Caddy can
    reach this service (127.0.0.1), so the header is Caddy's to set."""
    xff = request.headers.get("x-forwarded-for", "").strip()
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _client_hash(ip: str) -> str:
    # Salted with the service's own secret-free constant: enough to keep the
    # raw address out of the store, not a security boundary.
    return hashlib.sha256(("ig-inbox:" + ip).encode()).hexdigest()[:16]


def _recent_counts(root: Path, client: str) -> tuple[int, int]:
    """(this client's posts in the last hour, all posts in the last 24 hours)."""
    now = datetime.now(timezone.utc)
    hour_ago, day_ago = now - timedelta(hours=1), now - timedelta(days=1)
    mine = total = 0
    for folder in (root, root / "processed"):
        if not folder.exists():
            continue
        for path in folder.glob("*.json"):
            data = _read(path)
            when = datetime.fromisoformat(data["received_at"])
            if when >= day_ago:
                total += 1
                if when >= hour_ago and data.get("client") == client:
                    mine += 1
    return mine, total


@app.post("/api/inbox", status_code=201)
def create_item(item: NewItem, request: Request):
    if item.website.strip():
        # Looks like success to a bot; stores nothing.
        return {"id": "accepted", "received_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    text = item.text
    if not text.strip():
        raise HTTPException(status_code=422, detail="empty text")
    root = inbox_dir()
    _ensure_dirs(root)
    client = _client_hash(client_ip(request))
    mine, total = _recent_counts(root, client)
    if mine >= HOURLY_PER_CLIENT:
        raise HTTPException(status_code=429, detail="hourly limit reached; try again later")
    if total >= DAILY_TOTAL:
        raise HTTPException(status_code=429, detail="daily limit reached; try again tomorrow")
    now = datetime.now(timezone.utc)
    item_id = f"{now:%Y%m%dT%H%M%S}Z-{secrets.token_hex(4)}"
    data = {
        "id": item_id,
        "received_at": now.isoformat(timespec="seconds"),
        "source": item.source.strip(),
        "text": text,
        "client": client,
    }
    target = root / f"{item_id}.json"
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, target)  # atomic: a half-written file never looks pending
    return {"id": item_id, "received_at": data["received_at"]}


@app.get("/api/inbox")
def list_pending():
    root = inbox_dir()
    if not root.exists():
        return {"pending": []}
    items = [_summary(_read(p)) for p in sorted(root.glob("*.json"))]
    return {"pending": items}


@app.get("/api/inbox/{item_id}")
def get_item(item_id: str):
    if not ID_RE.match(item_id):
        raise HTTPException(status_code=404)
    root = inbox_dir()
    for path in (root / f"{item_id}.json", root / "processed" / f"{item_id}.json"):
        if path.exists():
            data = _read(path)
            data["processed"] = path.parent.name == "processed"
            return data
    raise HTTPException(status_code=404)
