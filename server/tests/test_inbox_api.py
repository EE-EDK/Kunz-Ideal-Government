import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

SERVER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER))

import inbox_api  # noqa: E402


@pytest.fixture
def inbox(tmp_path, monkeypatch):
    root = tmp_path / "inbox"
    monkeypatch.setenv("IG_INBOX_DIR", str(root))
    return root


@pytest.fixture
def client(inbox):
    return TestClient(inbox_api.app)


def test_post_then_list_then_get(client, inbox):
    r = client.post("/api/inbox", json={"text": "Make Layer 2 start with the coordination body.", "source": "chat 2026-10-04"})
    assert r.status_code == 201
    item_id = r.json()["id"]
    assert inbox_api.ID_RE.match(item_id)

    pending = client.get("/api/inbox").json()["pending"]
    assert [p["id"] for p in pending] == [item_id]
    assert pending[0]["source"] == "chat 2026-10-04"
    assert pending[0]["chars"] == len("Make Layer 2 start with the coordination body.")

    got = client.get(f"/api/inbox/{item_id}").json()
    assert got["text"] == "Make Layer 2 start with the coordination body."
    assert got["processed"] is False


def test_file_modes_are_private(client, inbox):
    item_id = client.post("/api/inbox", json={"text": "x"}).json()["id"]
    assert oct(inbox.stat().st_mode & 0o777) == "0o700"
    assert oct((inbox / f"{item_id}.json").stat().st_mode & 0o777) == "0o600"


def test_rejects_empty_and_oversize(client):
    assert client.post("/api/inbox", json={"text": ""}).status_code == 422
    assert client.post("/api/inbox", json={"text": "   "}).status_code == 422
    too_big = "a" * (inbox_api.MAX_TEXT_CHARS + 1)
    assert client.post("/api/inbox", json={"text": too_big}).status_code == 422
    assert client.post("/api/inbox", json={"text": "ok", "source": "s" * 201}).status_code == 422


def test_get_rejects_path_traversal(client):
    assert client.get("/api/inbox/..%2F..%2Fetc%2Fpasswd").status_code == 404
    assert client.get("/api/inbox/not-an-id").status_code == 404


def test_traversal_cannot_reach_a_file_outside_the_inbox(client, inbox):
    # A decoy that a missing ID guard would happily serve: sits beside the inbox.
    decoy = inbox.parent / "decoy.json"
    decoy.write_text(json.dumps({"id": "decoy", "received_at": "x", "source": "", "text": "SECRET"}))
    assert client.get("/api/inbox/..%2Fdecoy").status_code == 404
    assert client.get("/api/inbox/../decoy").status_code == 404


def test_missing_item_is_404(client):
    assert client.get("/api/inbox/20000101T000000Z-deadbeef").status_code == 404


def test_empty_inbox_lists_nothing(client):
    assert client.get("/api/inbox").json() == {"pending": []}


def test_cli_done_moves_item_and_keeps_content(client, inbox):
    item_id = client.post("/api/inbox", json={"text": "keep me", "source": "t"}).json()["id"]
    env = {**os.environ, "IG_INBOX_DIR": str(inbox)}
    script = str(SERVER / "ingest.py")

    listed = subprocess.run([sys.executable, script, "list"], env=env, capture_output=True, text=True)
    assert item_id in listed.stdout

    subprocess.run([sys.executable, script, "done", item_id], env=env, check=True, capture_output=True)
    assert not (inbox / f"{item_id}.json").exists()
    moved = json.loads((inbox / "processed" / f"{item_id}.json").read_text(encoding="utf-8"))
    assert moved["text"] == "keep me"
    assert "processed_at" in moved

    got = client.get(f"/api/inbox/{item_id}").json()
    assert got["processed"] is True
    assert client.get("/api/inbox").json() == {"pending": []}


def test_cli_show_prints_text(client, inbox):
    item_id = client.post("/api/inbox", json={"text": "line one\nline two"}).json()["id"]
    env = {**os.environ, "IG_INBOX_DIR": str(inbox)}
    out = subprocess.run([sys.executable, str(SERVER / "ingest.py"), "show", item_id],
                         env=env, capture_output=True, text=True, check=True)
    assert out.stdout == "line one\nline two\n"


def test_honeypot_looks_accepted_and_stores_nothing(client, inbox):
    r = client.post("/api/inbox", json={"text": "spam", "website": "http://x"})
    assert r.status_code == 201
    assert not inbox.exists() or not any(inbox.glob("*.json"))


def test_hourly_limit_per_client(client, inbox):
    for _ in range(inbox_api.HOURLY_PER_CLIENT):
        assert client.post("/api/inbox", json={"text": "x"}, headers={"x-forwarded-for": "198.51.100.7"}).status_code == 201
    r = client.post("/api/inbox", json={"text": "x"}, headers={"x-forwarded-for": "198.51.100.7"})
    assert r.status_code == 429
    # A different visitor is not blocked by the first one's count.
    other = client.post("/api/inbox", json={"text": "x"}, headers={"x-forwarded-for": "203.0.113.9"})
    assert other.status_code == 201


def test_daily_total_cap(client, inbox, monkeypatch):
    monkeypatch.setattr(inbox_api, "DAILY_TOTAL", 2)
    assert client.post("/api/inbox", json={"text": "a"}, headers={"x-forwarded-for": "1.1.1.1"}).status_code == 201
    assert client.post("/api/inbox", json={"text": "b"}, headers={"x-forwarded-for": "2.2.2.2"}).status_code == 201
    assert client.post("/api/inbox", json={"text": "c"}, headers={"x-forwarded-for": "3.3.3.3"}).status_code == 429


def test_raw_ip_is_not_stored(client, inbox):
    client.post("/api/inbox", json={"text": "x"}, headers={"x-forwarded-for": "198.51.100.77"})
    stored = next(inbox.glob("*.json")).read_text(encoding="utf-8")
    assert "198.51.100.77" not in stored
