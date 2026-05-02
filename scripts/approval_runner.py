#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import sqlite3
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
TOKEN_FILE = ROOT / "data" / "token"
SOURCECRAFT_ENV = WORKSPACE / "skills" / "sourcecraft-publisher" / "config" / ".env"
SOURCECRAFT_PUBLISHER = WORKSPACE / "skills" / "sourcecraft-publisher" / "scripts" / "publish_static.py"
TELEGRAM_SEND_AND_PIN = WORKSPACE / "scripts" / "telegram-send-and-pin-digest.mjs"
DB_PATH = Path(os.environ.get("CLEVER_COCKPIT_DB", ROOT / "data" / "cockpit.sqlite"))


class HandlerError(Exception):
    pass


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


def payload_for(approval: dict) -> dict:
    raw = approval.get("payload_json") or "{}"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HandlerError(f"payload_json is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise HandlerError("payload_json must decode to an object")
    return payload


def resolve_path(value: str, *, allow_tmp: bool = False, must_exist: bool = True) -> Path:
    if not value:
        raise HandlerError("path is required")
    path = Path(value).expanduser().resolve()
    allowed_roots = [WORKSPACE.resolve()]
    if allow_tmp:
        allowed_roots.append(Path("/tmp").resolve())
    if not any(path == root or root in path.parents for root in allowed_roots):
        roots = ", ".join(str(r) for r in allowed_roots)
        raise HandlerError(f"path outside allowed roots ({roots}): {path}")
    if must_exist and not path.exists():
        raise HandlerError(f"path does not exist: {path}")
    return path


def load_env_file(path: Path) -> dict[str, str]:
    env = os.environ.copy()
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            env[key] = value
    return env


def run_checked(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None, timeout: int = 300) -> str:
    proc = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout)
    output = "\n".join(part.strip() for part in [proc.stdout, proc.stderr] if part.strip())
    if proc.returncode != 0:
        raise HandlerError(output[-1200:] or f"command failed with exit {proc.returncode}")
    return output[-1200:] or "ok"


def handle_record_only(approval: dict, payload: dict) -> str:
    return str(payload.get("note") or f"Approval recorded: {approval.get('title', approval.get('id'))}")


def handle_idea_review(_approval: dict, payload: dict) -> str:
    idea_id = str(payload.get("idea_id") or "").strip()
    if not idea_id:
        raise HandlerError("idea_id is required")
    target_status = str(payload.get("target_status") or "review").strip()
    if target_status not in {"review", "approved", "done"}:
        raise HandlerError("target_status must be review, approved, or done")
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        idea = conn.execute("select * from ideas where id=?", (idea_id,)).fetchone()
        if not idea:
            raise HandlerError(f"idea not found: {idea_id}")
        t = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
        conn.execute("update ideas set status=?, updated_at=? where id=?", (target_status, t, idea_id))
        conn.execute(
            "insert into activity(title,kind,status,priority,body,created_at) values (?,?,?,?,?,?)",
            (f"Idea review accepted: {idea['title']}", "Idea", target_status, "normal", idea["body"], t),
        )
        conn.commit()
    return f"Idea {idea_id} moved to {target_status}"


def handle_telegram_send_and_pin_digest(_approval: dict, payload: dict) -> str:
    return send_and_pin_digest(payload)


def handle_sourcecraft_publish(_approval: dict, payload: dict) -> str:
    return publish_sourcecraft(payload)


def publish_sourcecraft(payload: dict) -> str:
    source = resolve_path(str(payload.get("source") or ""), allow_tmp=False)
    slug = str(payload.get("slug") or "").strip()
    if not slug:
        raise HandlerError("slug is required")
    cmd = [sys.executable, str(SOURCECRAFT_PUBLISHER), "--source", str(source), "--slug", slug]
    if payload.get("date"):
        cmd += ["--date", str(payload["date"])]
    if payload.get("message"):
        cmd += ["--message", str(payload["message"])]
    env = load_env_file(SOURCECRAFT_ENV)
    missing = [key for key in ["SOURCECRAFT_TOKEN", "SOURCECRAFT_REPO", "SOURCECRAFT_SITE_URL"] if not env.get(key)]
    if missing:
        raise HandlerError(f"missing SourceCraft env: {', '.join(missing)}")
    return run_checked(cmd, cwd=WORKSPACE, env=env, timeout=300)


def send_and_pin_digest(payload: dict) -> str:
    job_key = str(payload.get("job_key") or "").strip()
    text_file = resolve_path(str(payload.get("text_file") or ""), allow_tmp=True)
    if job_key not in {"reflection", "ai_wrapup", "telegram_radar"}:
        raise HandlerError("job_key must be one of reflection, ai_wrapup, telegram_radar")
    if not TELEGRAM_SEND_AND_PIN.exists():
        raise HandlerError(f"send-and-pin script not found: {TELEGRAM_SEND_AND_PIN}")
    return run_checked(["node", str(TELEGRAM_SEND_AND_PIN), job_key, str(text_file)], cwd=WORKSPACE, timeout=120)


def handle_digest_publish_and_send(_approval: dict, payload: dict) -> str:
    publish_out = publish_sourcecraft(payload)
    send_out = send_and_pin_digest(payload)
    return f"publish: {publish_out}\nsend: {send_out}"


HANDLERS: dict[str, Callable[[dict, dict], str]] = {
    "record_only": handle_record_only,
    "idea_review": handle_idea_review,
    "telegram_send_and_pin_digest": handle_telegram_send_and_pin_digest,
    "sourcecraft_publish": handle_sourcecraft_publish,
    "digest_publish_and_send": handle_digest_publish_and_send,
}


def handle_approval(approval: dict) -> tuple[str, str]:
    """Return (run_status, message). Keep this registry explicit and safe."""
    handler_name = (approval.get("handler") or "record_only").strip()
    handler = HANDLERS.get(handler_name)
    if not handler:
        return "needs_handler", f"No local handler registered for handler={handler_name!r}, approval id={approval.get('id')!r}."
    try:
        message = handler(approval, payload_for(approval))
    except HandlerError as exc:
        return "failed", str(exc)
    return "done", message


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
