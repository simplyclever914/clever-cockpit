#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JOBS = Path.home() / ".openclaw" / "cron" / "jobs.json"

SILENT_RE = re.compile(
    r"(silent|quiet|тих|no_reply|no-reply|watchdog|dirty reminder|sync|index|task runner|grooming|triage)",
    re.I,
)
LOCAL_SCRIPT_RE = re.compile(r"(~/.openclaw/|\.openclaw/|\bcd\s+\$?HOME|\bscripts/|\bpython3\s+scripts/|\.sh\b|\.py\b|\.mjs\b)")
NO_REPLY_RE = re.compile(r"\bNO_REPLY\b")
NO_TASKS_RE = re.compile(r"\bNO_TASKS\b")
FAILURE_RE = re.compile(r"\b(fail|failure|error|ошиб|упал|причин|alert|blocked|блок)\b", re.I)
USER_FACING_RE = re.compile(r"(notify Vadim|Telegram-facing|отч[её]т Вадиму|сообщи Вадиму|short Telegram-facing alert|send Vadim)", re.I)
DIGEST_SENDER_RE = re.compile(r"telegram-send-and-pin-digest\.mjs")


def load_jobs(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    jobs = data.get("jobs", [])
    if not isinstance(jobs, list):
        raise ValueError("jobs.json must contain a jobs array")
    return [job for job in jobs if isinstance(job, dict)]


def payload_message(job: dict) -> str:
    payload = job.get("payload") or {}
    if isinstance(payload, dict):
        return str(payload.get("message") or "")
    return ""


def delivery_mode(job: dict) -> str:
    delivery = job.get("delivery") or {}
    if isinstance(delivery, dict):
        return str(delivery.get("mode") or "")
    return ""


def is_silent_local(job: dict, msg: str) -> bool:
    haystack = "\n".join([str(job.get("name") or ""), str(job.get("description") or ""), msg])
    if USER_FACING_RE.search(haystack):
        return False
    return bool(SILENT_RE.search(haystack) and (LOCAL_SCRIPT_RE.search(msg) or NO_REPLY_RE.search(msg) or NO_TASKS_RE.search(msg)))


def audit_job(job: dict) -> list[str]:
    issues: list[str] = []
    name = job.get("name") or job.get("id") or "<unnamed>"
    if not job.get("enabled", True):
        return issues
    msg = payload_message(job)
    mode = delivery_mode(job)
    silent_local = is_silent_local(job, msg)

    if silent_local:
        if mode != "none":
            issues.append(f"{name}: silent/local success path must use delivery.mode='none' (found {mode or 'missing'})")
        if not (NO_REPLY_RE.search(msg) or NO_TASKS_RE.search(msg)):
            issues.append(f"{name}: silent/local success path must explicitly finish with NO_REPLY or NO_TASKS")
        if not (job.get("failureAlert") or FAILURE_RE.search(msg)):
            issues.append(f"{name}: silent/local job needs a failureAlert or explicit failure/blocker reporting path")

    # If the prompt says NO_REPLY and the job is otherwise silent/local, final delivery must be disabled;
    # user-facing jobs can still deliberately use final delivery for the non-success branch.
    if silent_local and NO_REPLY_RE.search(msg) and mode and mode != "none":
        issues.append(f"{name}: silent/local prompt requests NO_REPLY but delivery.mode is {mode!r}, expected 'none'")

    # Digest jobs may send through the deterministic sender, but should not also rely on cron final delivery.
    if DIGEST_SENDER_RE.search(msg) and mode != "none":
        issues.append(f"{name}: digest sender job should have delivery.mode='none' so only the deterministic sender posts")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit OpenClaw cron jobs for low-noise finalization contracts.")
    ap.add_argument("--jobs", type=Path, default=DEFAULT_JOBS, help="Path to OpenClaw cron jobs.json")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    jobs = load_jobs(args.jobs)
    issues: list[str] = []
    checked = 0
    silent_local_count = 0
    for job in jobs:
        if not job.get("enabled", True):
            continue
        checked += 1
        msg = payload_message(job)
        if is_silent_local(job, msg):
            silent_local_count += 1
        issues.extend(audit_job(job))

    result = {"ok": not issues, "checked": checked, "silent_local_checked": silent_local_count, "issues": issues}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif issues:
        print("Cron finalization audit found issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print(f"OK cron finalization audit checked={checked} silent_local={silent_local_count}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
