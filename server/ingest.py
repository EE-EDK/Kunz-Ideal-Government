#!/usr/bin/env python3
"""Retrieve pasted inbox text and mark it processed.

    python3 server/ingest.py list              # pending items
    python3 server/ingest.py show <id>         # print one item's text
    python3 server/ingest.py done <id> [...]   # move to processed/ after applying it

Nothing is deleted. `done` moves the file to processed/ and stamps processed_at.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inbox_api import ID_RE, inbox_dir  # noqa: E402


def _load(root: Path, item_id: str) -> tuple[Path, dict]:
    if not ID_RE.match(item_id):
        raise SystemExit(f"not an inbox id: {item_id}")
    path = root / f"{item_id}.json"
    if not path.exists():
        raise SystemExit(f"no pending item {item_id} in {root}")
    return path, json.loads(path.read_text(encoding="utf-8"))


def cmd_list(root: Path) -> int:
    paths = sorted(root.glob("*.json")) if root.exists() else []
    if not paths:
        print("inbox empty")
        return 0
    for p in paths:
        d = json.loads(p.read_text(encoding="utf-8"))
        print(f"{d['id']}  {d['received_at']}  {len(d['text']):>7} chars  {d['source'] or '-'}")
    return 0


def cmd_show(root: Path, item_id: str) -> int:
    _, d = _load(root, item_id)
    print(d["text"])
    return 0


def cmd_done(root: Path, ids: list[str]) -> int:
    processed = root / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    os.chmod(processed, 0o700)
    for item_id in ids:
        path, d = _load(root, item_id)
        d["processed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        target = processed / path.name
        target.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        os.chmod(target, 0o600)
        path.unlink()  # the data now lives in processed/; this is a move, not a delete of content
        print(f"processed {item_id}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p_show = sub.add_parser("show")
    p_show.add_argument("id")
    p_done = sub.add_parser("done")
    p_done.add_argument("ids", nargs="+")
    args = parser.parse_args(argv)

    root = inbox_dir()
    if args.cmd == "list":
        return cmd_list(root)
    if args.cmd == "show":
        return cmd_show(root, args.id)
    return cmd_done(root, args.ids)


if __name__ == "__main__":
    sys.exit(main())
