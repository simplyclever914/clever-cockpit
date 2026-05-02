#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = ROOT / "data" / "token"


def load_token(explicit: str | None) -> str:
    if explicit:
        return explicit
    return TOKEN_FILE.read_text(encoding="utf-8").strip()


def request_json(method: str, base_url: str, token: str, path: str, payload: dict | None = None) -> dict:
    url = base_url.rstrip("/") + path
    body = None
    headers = {"Authorization": f"Bearer {token}"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def handle_approval(approval: dict) -> tuple[str, str]:
    """Return (run_status, message). Keep this registry explicit and safe."""
    approval_id = approval.get("id", "")
    title = approval.get("title", approval_id)

    # These seed approvals are policy confirmations, not executable shell commands.
    # Mark them done so they do not stay stuck, and let future real approvals add
    # explicit local handlers here.
    if approval_id in {"publish-page", "send-pin"}:
        return "done", f"Policy approval recorded: {title}"

    return "needs_handler", f"No local handler registered for approval id={approval_id!r}. Clever must inspect and continue deliberately."


def poll_once(base_url: str, token: str, limit: int) -> int:
    data = request_json("GET", base_url, token, f"/api/approvals/ready?limit={limit}")
    approvals = data.get("approvals", [])
    for approval in approvals:
        try:
            run_status, message = handle_approval(approval)
        except Exception as exc:  # defensive: never silently lose a claimed approval
            run_status, message = "failed", f"Handler crashed: {exc}"
        request_json(
            "POST",
            base_url,
            token,
            "/api/approvals/complete",
            {"id": approval["id"], "run_status": run_status, "message": message},
        )
        print(f"{approval['id']}: {run_status} — {message}", flush=True)
    return len(approvals)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Poll Clever Cockpit approvals and dispatch safe local handlers.")
    ap.add_argument("--base-url", default="http://127.0.0.1:8765")
    ap.add_argument("--token", default=None)
    ap.add_argument("--interval", type=float, default=15.0)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args(argv)

    token = load_token(args.token)
    while True:
        try:
            count = poll_once(args.base_url, token, args.limit)
            if args.once and count == 0:
                print("no ready approvals", flush=True)
        except urllib.error.HTTPError as exc:
            print(f"approval runner HTTP error: {exc.code} {exc.reason}", file=sys.stderr, flush=True)
            if args.once:
                return 1
        except Exception as exc:
            print(f"approval runner error: {exc}", file=sys.stderr, flush=True)
            if args.once:
                return 1
        if args.once:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
