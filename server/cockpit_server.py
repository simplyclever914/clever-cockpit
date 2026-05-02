#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"
DATA_DIR = ROOT / "data"
DB_PATH = Path(os.environ.get("CLEVER_COCKPIT_DB", DATA_DIR / "cockpit.sqlite"))
TOKEN_FILE = DATA_DIR / "token"
CRON_DIR = Path(os.environ.get("OPENCLAW_CRON_DIR", Path.home() / ".openclaw" / "cron"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(text: str) -> str:
    out = []
    prev_dash = False
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            prev_dash = False
        elif not prev_dash:
            out.append("-")
            prev_dash = True
    value = "".join(out).strip("-")[:60]
    return value or f"item-{secrets.token_hex(4)}"


SCHEMA = """
create table if not exists approvals (
  id text primary key,
  title text not null,
  kind text not null default 'approval',
  priority text not null default 'normal',
  body text not null default '',
  status text not null default 'pending',
  handler text,
  payload_json text,
  run_status text,
  claimed_at text,
  completed_at text,
  last_error text,
  created_at text not null,
  updated_at text not null
);
create table if not exists ideas (
  id text primary key,
  title text not null,
  body text not null default '',
  status text not null default 'proposed',
  source text,
  created_at text not null,
  updated_at text not null
);
create table if not exists projects (
  id text primary key,
  title text not null,
  status text not null default 'draft',
  body text not null default '',
  source_idea_id text,
  created_at text not null,
  updated_at text not null
);
create table if not exists tasks (
  id text primary key,
  title text not null,
  project text not null default 'Inbox',
  status text not null default 'open',
  body text not null default '',
  source_idea_id text,
  created_at text not null,
  updated_at text not null
);
create table if not exists activity (
  id integer primary key autoincrement,
  title text not null,
  kind text not null default 'Activity',
  status text not null default 'done',
  priority text not null default 'normal',
  body text not null default '',
  created_at text not null
);
"""

SEED = {
    "approvals": [
        ("publish-page", "Publish new external page", "external_action", "urgent", "Public SourceCraft page requires explicit approval unless already requested."),
        ("send-pin", "Send/pin digest to Telegram", "messaging", "high", "Allowed only after successful generation, publication, and verification."),
    ],
    "ideas": [
        ("cockpit-memory", "Clever Cockpit as idea/task memory", "Decision needed: build local MVP so good ideas from chat become tracked projects/tasks. Next: define datastore.", "review", "chat"),
        ("telegram-idea-command", "Telegram command: /idea", "Capture current message/thread into Ideas with source link, tags, and suggested next action.", "proposed", "chat"),
        ("auto-convert", "Auto-convert approved idea to project", "When Вадим clicks OK: create project card + first 2-3 tasks + review date.", "approved", "chat"),
        ("digest-gate", "Digest quality gate", "Before publish: required sections, source count, stale index, local path leak, HTTP 200.", "approved", "chat"),
        ("oauth-audit", "OAuth/app permission audit", "Periodic checklist for GitHub/Cursor/Claude/Codex access hygiene.", "done", "chat"),
    ],
    "projects": [
        ("clever-cockpit", "Clever Cockpit", "active", "Outcome: единый локальный cockpit для идей, задач, approvals и activity. Focus: UX, связи idea→project→task, Telegram /idea capture и понятная очередь задач.", "cockpit-memory"),
        ("telegram-command-idea", "Telegram /idea Capture", "planning", "Outcome: сообщения и replies из Telegram быстро попадают в Cockpit Ideas с source context. Scope: синтаксис команды, обработка reply, создание идеи/API и понятные ошибки. Next: финализировать контракт и реализовать command handler.", "telegram-idea-command"),
        ("daily-reviews", "Daily Reviews & Publishing", "active", "Outcome: ежедневные AI/Agentic Dev и Telegram reviews публикуются и доставляются с quality gates. Scope: сбор источников, редактура, SourceCraft publish, Telegram send/pin, проверка ссылок.", None),
        ("telegram-knowledge-index", "Telegram Knowledge Index", "maintenance", "Outcome: reader account поддерживает локальный searchable архив Telegram channels/groups. Scope: allowlist, auto-detect новых dialogs, incremental sync, SQLite FTS, safe logs без секретов.", None),
        ("tooling-sync", "OpenClaw Tools & Skills", "maintenance", "Outcome: workspace-authored skills/scripts/docs синхронизированы в GitHub и не теряются. Scope: safe projection, autosync, dirty reminders, секреты вне repo.", None),
        ("personal-ops", "Personal Ops & Reflection", "maintenance", "Outcome: регулярный reflection loop и операционные проверки помогают улучшать работу Вадима и Clever без лишнего шума. Scope: cron health, memory notes, конкретные предложения и follow-up ideas.", None),
    ],
    "tasks": [
        ("schema", "Описать жизненный цикл идеи", "Clever Cockpit", "open", "Результат: зафиксирован понятный цикл идея → решение → проект/задача → готово/отложено. Объём: статусы, обязательные связи и правила переходов. Готово когда: UI и API используют одни и те же термины жизненного цикла.", None),
        ("local-store", "Создать локальное SQLite-хранилище", "Clever Cockpit", "open", "Результат: состояние Cockpit сохраняется локально. Объём: SQLite-схема и state API; Supabase не входит в MVP. Готово когда: идеи, проекты и задачи переживают перезапуск сервера.", None),
        ("telegram-capture", "Описать контракт Telegram-команды /idea", "Clever Cockpit", "waiting", "Результат: выбран точный синтаксис захвата идей из Telegram. Объём: /idea text, захват reply-сообщения, опциональные теги/проект и сообщения об ошибках. Готово когда: реализацию можно делать без догадок о пользовательском синтаксисе. Блокер: выбрать финальную грамматику команды.", None),
    ],
    "activity": [
        ("Clever Cockpit local service initialized", "System", "done", "normal", "SQLite-backed LAN-capable cockpit service is ready."),
    ],
}


def connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    migrate(conn)
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    approval_columns = {row[1] for row in conn.execute("pragma table_info(approvals)")}
    approval_migrations = {
        "run_status": "alter table approvals add column run_status text",
        "handler": "alter table approvals add column handler text",
        "payload_json": "alter table approvals add column payload_json text",
        "claimed_at": "alter table approvals add column claimed_at text",
        "completed_at": "alter table approvals add column completed_at text",
        "last_error": "alter table approvals add column last_error text",
    }
    for column, sql in approval_migrations.items():
        if column not in approval_columns:
            conn.execute(sql)
    task_columns = {row[1] for row in conn.execute("pragma table_info(tasks)")}
    task_migrations = {
        "trigger": "alter table tasks add column trigger text not null default 'manual'",
        "run_status": "alter table tasks add column run_status text not null default 'idle'",
        "scheduled_for": "alter table tasks add column scheduled_for text",
        "last_run_at": "alter table tasks add column last_run_at text",
        "last_error": "alter table tasks add column last_error text",
    }
    for column, sql in task_migrations.items():
        if column not in task_columns:
            conn.execute(sql)
    conn.commit()


def seed(conn: sqlite3.Connection, force: bool = False) -> None:
    if force:
        conn.executescript("delete from approvals; delete from ideas; delete from projects; delete from tasks; delete from activity;")
    if conn.execute("select count(*) from ideas").fetchone()[0]:
        return
    t = now()
    conn.executemany("insert or ignore into approvals(id,title,kind,priority,body,status,handler,payload_json,created_at,updated_at) values (?,?,?,?,?,?,?,?,?,?)", [(a,b,c,d,e,"pending","record_only",json.dumps({"note": e}, ensure_ascii=False),t,t) for a,b,c,d,e in SEED["approvals"]])
    conn.executemany("insert or ignore into ideas values (?,?,?,?,?,?,?)", [(a,b,c,d,e,t,t) for a,b,c,d,e in SEED["ideas"]])
    conn.executemany("insert or ignore into projects values (?,?,?,?,?,?,?)", [(a,b,c,d,e,t,t) for a,b,c,d,e in SEED["projects"]])
    conn.executemany("insert or ignore into tasks(id,title,project,status,body,source_idea_id,created_at,updated_at) values (?,?,?,?,?,?,?,?)", [(a,b,c,d,e,f,t,t) for a,b,c,d,e,f in SEED["tasks"]])
    conn.executemany("insert into activity(title,kind,status,priority,body,created_at) values (?,?,?,?,?,?)", [(a,b,c,d,e,t) for a,b,c,d,e in SEED["activity"]])
    conn.commit()


def rows(conn: sqlite3.Connection, table: str, where: str = "", args: tuple = ()) -> list[dict]:
    order = "created_at desc"
    if table == "ideas":
        order = "updated_at desc"
    return [dict(r) for r in conn.execute(f"select * from {table} {where} order by {order}", args)]


def next_msk_0430() -> str:
    # Europe/Moscow is UTC+3 without DST at the moment; store as UTC ISO for simple comparisons.
    msk = timezone(timedelta(hours=3))
    dt = datetime.now(msk)
    target = dt.replace(hour=4, minute=30, second=0, microsecond=0)
    if dt >= target:
        target += timedelta(days=1)
    return target.astimezone(timezone.utc).isoformat(timespec="seconds")


def transition_task(conn: sqlite3.Connection, task_id: str, action: str) -> dict | None:
    task = conn.execute("select * from tasks where id=?", (task_id,)).fetchone()
    if not task:
        return None
    t = now()
    if action == "run":
        conn.execute("update tasks set status='waiting', trigger='manual', run_status='queued', scheduled_for=null, last_error=null, updated_at=? where id=?", (t, task_id))
        add_activity(conn, f"Task queued: {task['title']}", task["body"], "Task", "queued", "high")
    elif action == "schedule":
        scheduled_for = next_msk_0430()
        conn.execute("update tasks set status='scheduled', trigger='schedule', run_status='scheduled', scheduled_for=?, last_error=null, updated_at=? where id=?", (scheduled_for, t, task_id))
        add_activity(conn, f"Task scheduled: {task['title']}", f"Scheduled for next 04:30 MSK ({scheduled_for}).", "Task", "scheduled", "normal")
    elif action == "reset":
        conn.execute("update tasks set status='open', trigger='manual', run_status='idle', scheduled_for=null, last_error=null, updated_at=? where id=?", (t, task_id))
        add_activity(conn, f"Task reset: {task['title']}", task["body"], "Task", "open", "normal")
    elif action == "done":
        conn.execute("update tasks set status='done', run_status='done', last_run_at=?, last_error=null, updated_at=? where id=?", (t, t, task_id))
        add_activity(conn, f"Task completed: {task['title']}", task["body"], "Task", "done", "normal")
    elif action == "waiting":
        conn.execute("update tasks set status='waiting', run_status='idle', last_error=?, updated_at=? where id=?", ("Waiting/blocker set from UI", t, task_id))
        add_activity(conn, f"Task waiting: {task['title']}", "Waiting/blocker set from UI", "Task", "waiting", "warn")
    else:
        raise ValueError("action must be run, schedule, reset, done, or waiting")
    conn.commit()
    updated = conn.execute("select * from tasks where id=?", (task_id,)).fetchone()
    return dict(updated) if updated else None


def read_json_file(path: Path, default: object) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def ms_to_iso(ms: int | float | None) -> str | None:
    if not ms:
        return None
    return datetime.fromtimestamp(float(ms) / 1000, timezone.utc).isoformat(timespec="seconds")


def describe_schedule(schedule: dict) -> str:
    kind = schedule.get("kind")
    if kind == "cron":
        tz = schedule.get("tz") or "host local time"
        return f"cron {schedule.get('expr', '?')} ({tz})"
    if kind == "every":
        every_ms = schedule.get("everyMs")
        if isinstance(every_ms, (int, float)) and every_ms > 0:
            minutes = every_ms / 60000
            if minutes.is_integer() and minutes < 120:
                return f"every {int(minutes)} min"
            hours = minutes / 60
            if hours.is_integer():
                return f"every {int(hours)} h"
        return f"every {every_ms} ms"
    if kind == "at":
        return f"at {schedule.get('at', '?')}"
    return kind or "unknown"


def cron_schedules() -> list[dict]:
    jobs_data = read_json_file(CRON_DIR / "jobs.json", {"jobs": []})
    state_data = read_json_file(CRON_DIR / "jobs-state.json", {"jobs": {}})
    jobs = jobs_data.get("jobs", []) if isinstance(jobs_data, dict) else []
    states = state_data.get("jobs", {}) if isinstance(state_data, dict) else {}
    out: list[dict] = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        job_id = job.get("id") or job.get("jobId")
        if not job_id:
            continue
        job_state = states.get(job_id, {}).get("state", {}) if isinstance(states, dict) else {}
        schedule = job.get("schedule") or {}
        last_status = job_state.get("lastRunStatus") or job_state.get("lastStatus")
        out.append({
            "id": job_id,
            "name": job.get("name") or job_id,
            "description": job.get("description") or "",
            "enabled": bool(job.get("enabled", True)),
            "schedule": describe_schedule(schedule if isinstance(schedule, dict) else {}),
            "schedule_kind": schedule.get("kind") if isinstance(schedule, dict) else None,
            "last_run_at": ms_to_iso(job_state.get("lastRunAtMs")),
            "next_run_at": ms_to_iso(job_state.get("nextRunAtMs")),
            "last_status": last_status or "never",
            "last_duration_ms": job_state.get("lastDurationMs"),
            "last_delivery_status": job_state.get("lastDeliveryStatus"),
            "consecutive_errors": job_state.get("consecutiveErrors", 0),
            "consecutive_skipped": job_state.get("consecutiveSkipped", 0),
        })
    return sorted(out, key=lambda x: (x.get("next_run_at") or "9999", x.get("name") or ""))


def add_activity(conn: sqlite3.Connection, title: str, body: str = "", kind: str = "Activity", status: str = "done", priority: str = "normal") -> None:
    conn.execute("insert into activity(title,kind,status,priority,body,created_at) values (?,?,?,?,?,?)", (title, kind, status, priority, body, now()))


SMOKE_ACTIVITY_TITLE_RE = re.compile(r"^Task (scheduled|reset): (Continue Clever Cockpit MVP|Implement: Telegram command: /idea)$")
LOW_SIGNAL_TASK_ACTIVITY_RE = re.compile(r"^Task (scheduled|reset): (.+)$")


def meaningful_activity(items: list[dict], limit: int = 50) -> list[dict]:
    """Keep the Activity view focused on real decisions/results, not smoke-test churn."""
    visible: list[dict] = []
    seen_low_signal: set[tuple[str, str]] = set()
    for item in items:
        title = item.get("title", "")
        if SMOKE_ACTIVITY_TITLE_RE.match(title):
            continue
        match = LOW_SIGNAL_TASK_ACTIVITY_RE.match(title)
        if match:
            key = (match.group(1), match.group(2))
            if key in seen_low_signal:
                continue
            seen_low_signal.add(key)
        visible.append(item)
        if len(visible) >= limit:
            break
    return visible


def state(conn: sqlite3.Connection) -> dict:
    return {
        "approvals": rows(conn, "approvals", "where status='pending'"),
        "held_approvals": rows(conn, "approvals", "where status='hold'"),
        "ideas": rows(conn, "ideas"),
        "projects": rows(conn, "projects"),
        "tasks": rows(conn, "tasks"),
        "activity": meaningful_activity(rows(conn, "activity"), 50),
        "schedules": cron_schedules(),
    }


def ready_approvals(conn: sqlite3.Connection, limit: int = 10) -> list[dict]:
    t = now()
    rows_to_claim = conn.execute(
        """
        select * from approvals
        where status='accepted' and (run_status is null or run_status in ('queued','needs_retry'))
        order by updated_at asc
        limit ?
        """,
        (limit,),
    ).fetchall()
    claimed: list[dict] = []
    for row in rows_to_claim:
        conn.execute(
            "update approvals set run_status='running', claimed_at=?, updated_at=? where id=? and (run_status is null or run_status in ('queued','needs_retry'))",
            (t, t, row["id"]),
        )
        add_activity(conn, f"Approval claimed: {row['title']}", row["body"], "ApprovalRunner", "running", row["priority"])
        claimed.append(dict(row) | {"run_status": "running", "claimed_at": t, "updated_at": t})
    conn.commit()
    return claimed


def complete_approval(conn: sqlite3.Connection, approval_id: str, run_status: str, message: str = "") -> dict | None:
    allowed = {"done", "failed", "needs_handler", "needs_retry"}
    if run_status not in allowed:
        raise ValueError(f"invalid run_status: {run_status}")
    row = conn.execute("select * from approvals where id=?", (approval_id,)).fetchone()
    if not row:
        return None
    t = now()
    conn.execute(
        "update approvals set run_status=?, completed_at=?, last_error=?, updated_at=? where id=?",
        (run_status, t, message if run_status in {"failed", "needs_handler", "needs_retry"} else None, t, approval_id),
    )
    add_activity(conn, f"Approval run {run_status}: {row['title']}", message, "ApprovalRunner", run_status, row["priority"])
    conn.commit()
    updated = conn.execute("select * from approvals where id=?", (approval_id,)).fetchone()
    return dict(updated) if updated else None


def create_approval(conn: sqlite3.Connection, data: dict) -> dict:
    title = (data.get("title") or "").strip()
    if not title:
        raise ValueError("title required")
    approval_id = (data.get("id") or f"{slugify(title)}-{secrets.token_hex(3)}").strip()
    kind = (data.get("kind") or "approval").strip()
    priority = (data.get("priority") or "normal").strip()
    body = (data.get("body") or "").strip()
    handler = (data.get("handler") or "record_only").strip()
    payload = data.get("payload", {})
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    t = now()
    conn.execute(
        """
        insert into approvals(id,title,kind,priority,body,status,handler,payload_json,run_status,claimed_at,completed_at,last_error,created_at,updated_at)
        values (?,?,?,?,?,?,?,?,null,null,null,null,?,?)
        """,
        (approval_id, title, kind, priority, body, "pending", handler, json.dumps(payload, ensure_ascii=False), t, t),
    )
    add_activity(conn, f"Approval requested: {title}", body, "Approval", "pending", priority)
    conn.commit()
    row = conn.execute("select * from approvals where id=?", (approval_id,)).fetchone()
    return dict(row)


TASK_DESCRIPTION_ERROR = "описание задачи должно содержать конкретные разделы: Результат:, Объём:, Готово когда:"
TASK_DESCRIPTION_SECTIONS = (
    ("результат:", "outcome:"),
    ("объём:", "объем:", "scope:"),
    ("готово когда:", "done when:"),
)


def validate_task_description(body: str) -> None:
    normalized = re.sub(r"\s+", " ", body.strip()).lower()
    generic = {"", "todo", "tbd", "fix", "fix stuff", "do it", "later", "placeholder", "next step", "потом", "доделать", "разобраться"}
    if normalized in generic or len(normalized) < 80:
        raise ValueError(TASK_DESCRIPTION_ERROR)
    for aliases in TASK_DESCRIPTION_SECTIONS:
        marker = next((section for section in aliases if section in normalized), None)
        if not marker:
            raise ValueError(TASK_DESCRIPTION_ERROR)
        after = normalized.split(marker, 1)[1].strip()
        if not after or after.split(" ", 5)[0] in generic:
            raise ValueError(TASK_DESCRIPTION_ERROR)


def create_task(conn: sqlite3.Connection, data: dict) -> dict:
    title = (data.get("title") or "").strip()
    if not title:
        raise ValueError("title required")
    body = (data.get("body") or data.get("description") or "").strip()
    validate_task_description(body)
    task_id = (data.get("id") or f"{slugify(title)}-{secrets.token_hex(3)}").strip()
    project = (data.get("project") or "Inbox").strip() or "Inbox"
    status = (data.get("status") or "open").strip() or "open"
    if status not in {"open", "waiting", "scheduled", "done"}:
        raise ValueError("status must be open, waiting, scheduled, or done")
    trigger = (data.get("trigger") or "manual").strip() or "manual"
    run_status = (data.get("run_status") or "idle").strip() or "idle"
    source_idea_id = data.get("source_idea_id")
    t = now()
    conn.execute(
        """
        insert into tasks(id,title,project,status,body,source_idea_id,created_at,updated_at,trigger,run_status)
        values (?,?,?,?,?,?,?,?,?,?)
        """,
        (task_id, title, project, status, body, source_idea_id, t, t, trigger, run_status),
    )
    add_activity(conn, f"Task created: {title}", body, "Task", status)
    conn.commit()
    row = conn.execute("select * from tasks where id=?", (task_id,)).fetchone()
    return dict(row)


def update_task(conn: sqlite3.Connection, data: dict) -> dict | None:
    task_id = (data.get("id") or "").strip()
    if not task_id:
        raise ValueError("id required")
    row = conn.execute("select * from tasks where id=?", (task_id,)).fetchone()
    if not row:
        return None
    title = (data.get("title") if data.get("title") is not None else row["title"]).strip()
    if not title:
        raise ValueError("title required")
    body = (data.get("body") if data.get("body") is not None else row["body"]).strip()
    validate_task_description(body)
    status = (data.get("status") if data.get("status") is not None else row["status"]).strip() or "open"
    if status not in {"open", "waiting", "scheduled", "done"}:
        raise ValueError("status must be open, waiting, scheduled, or done")
    t = now()
    run_status = row["run_status"]
    last_run_at = row["last_run_at"]
    if status == "done" and run_status != "done":
        run_status = "done"
        last_run_at = t
    elif status in {"open", "waiting"} and run_status in {"queued", "scheduled", "running", "done"}:
        run_status = "idle"
    conn.execute(
        "update tasks set title=?, body=?, status=?, run_status=?, last_run_at=?, last_error=null, updated_at=? where id=?",
        (title, body, status, run_status, last_run_at, t, task_id),
    )
    add_activity(conn, f"Task edited: {title}", "Updated task title, description, or status from Cockpit UI.", "Task", status)
    conn.commit()
    updated = conn.execute("select * from tasks where id=?", (task_id,)).fetchone()
    return dict(updated) if updated else None


def ensure_token() -> str:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.get("CLEVER_COCKPIT_TOKEN")
    if env:
        return env.strip()
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    token = secrets.token_urlsafe(24)
    TOKEN_FILE.write_text(token)
    try:
        TOKEN_FILE.chmod(0o600)
    except OSError:
        pass
    return token


class Handler(SimpleHTTPRequestHandler):
    server_version = "CleverCockpit/0.1"

    def __init__(self, *args, token: str, require_token: bool, **kwargs):
        self.token = token
        self.require_token = require_token
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        safe_args = tuple(redact_token(str(arg)) for arg in args)
        super().log_message(format, *safe_args)

    def auth_ok(self) -> bool:
        if not self.require_token:
            return True
        parsed = urlparse(self.path)
        query_token = parse_qs(parsed.query).get("token", [None])[0]
        header = self.headers.get("Authorization", "")
        bearer = header.removeprefix("Bearer ").strip() if header.startswith("Bearer ") else None
        return query_token == self.token or bearer == self.token

    def send_json(self, data: object, status_code: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            if not self.auth_ok():
                self.send_json({"error": "unauthorized"}, 401)
                return
            with connect() as conn:
                seed(conn)
                if parsed.path == "/api/state":
                    self.send_json(state(conn))
                elif parsed.path == "/api/approvals/ready":
                    qs = parse_qs(parsed.query)
                    limit = min(int(qs.get("limit", ["10"])[0]), 50)
                    self.send_json({"approvals": ready_approvals(conn, limit)})
                else:
                    self.send_json({"error": "not found"}, 404)
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            self.send_json({"error": "not found"}, 404)
            return
        if not self.auth_ok():
            self.send_json({"error": "unauthorized"}, 401)
            return
        data = self.read_json()
        try:
            with connect() as conn:
                seed(conn)
                if parsed.path == "/api/reset":
                    seed(conn, force=True)
                elif parsed.path == "/api/approvals/decide":
                    approval_id = data["id"]
                    decision = data.get("decision", "accepted")
                    if decision not in {"accepted", "rejected", "hold", "pending"}:
                        self.send_json({"error": "invalid approval decision"}, 400); return
                    row = conn.execute("select * from approvals where id=?", (approval_id,)).fetchone()
                    if not row:
                        self.send_json({"error": "approval not found"}, 404); return
                    run_status = "queued" if decision == "accepted" else None
                    conn.execute(
                        "update approvals set status=?, run_status=?, claimed_at=null, completed_at=null, last_error=null, updated_at=? where id=?",
                        (decision, run_status, now(), approval_id),
                    )
                    add_activity(conn, f"Approval {decision}: {row['title']}", row["body"], "Approval", decision, row["priority"])
                    conn.commit()
                elif parsed.path == "/api/approvals/complete":
                    approval_id = data["id"]
                    run_status = data.get("run_status", "done")
                    message = (data.get("message") or "").strip()
                    updated = complete_approval(conn, approval_id, run_status, message)
                    if not updated:
                        self.send_json({"error": "approval not found"}, 404); return
                    self.send_json({"approval": updated, "state": state(conn)})
                    return
                elif parsed.path == "/api/approvals":
                    try:
                        approval = create_approval(conn, data)
                    except ValueError as exc:
                        self.send_json({"error": str(exc)}, 400); return
                    self.send_json({"approval": approval, "state": state(conn)}, 201)
                    return
                elif parsed.path == "/api/ideas":
                    title = (data.get("title") or "").strip()
                    if not title:
                        self.send_json({"error": "title required"}, 400); return
                    body = (data.get("body") or "").strip()
                    source = data.get("source") or "manual"
                    item_id = data.get("id") or f"{slugify(title)}-{secrets.token_hex(3)}"
                    t = now()
                    conn.execute("insert into ideas values (?,?,?,?,?,?,?)", (item_id, title, body, "proposed", source, t, t))
                    add_activity(conn, f"Captured idea: {title}", body, "Idea", "proposed")
                    conn.commit()
                elif parsed.path == "/api/ideas/transition":
                    idea_id = data["id"]
                    action = data.get("action", "ok")
                    idea = conn.execute("select * from ideas where id=?", (idea_id,)).fetchone()
                    if not idea:
                        self.send_json({"error": "idea not found"}, 404); return
                    t = now()
                    if action == "deny":
                        conn.execute("update ideas set status='done', updated_at=? where id=?", (t, idea_id))
                        add_activity(conn, f"Parked idea: {idea['title']}", idea["body"], "Idea", "done")
                    else:
                        conn.execute("update ideas set status='approved', updated_at=? where id=?", (t, idea_id))
                        project_id = slugify(idea["title"])
                        task_id = f"{project_id}-next"
                        conn.execute("insert or ignore into projects values (?,?,?,?,?,?,?)", (project_id, idea["title"], "draft", "Draft project created from approved idea. Confirm before making active.", idea_id, t, t))
                        task_title = f"Реализовать: {idea['title']}" if action == "task" else f"Определить следующий шаг: {idea['title']}"
                        task_body = "Результат: одобренная идея превращена в одно понятное следующее действие. Объём: уточнить владельца, ожидаемый артефакт и критерии готовности перед запуском. Готово когда: связь проект/задача явная, а следующий шаг исполнения не требует догадок. По умолчанию задача запускается вручную через Run или планируется на 04:30 MSK."
                        if not conn.execute("select 1 from tasks where id=?", (task_id,)).fetchone():
                            create_task(conn, {"id": task_id, "title": task_title, "project": idea["title"], "status": "open", "body": task_body, "source_idea_id": idea_id, "trigger": "manual", "run_status": "idle"})
                        add_activity(conn, f"Converted idea: {idea['title']}", "Created draft project/task follow-up with manual trigger.", "Idea", "approved", "high")
                    conn.commit()
                elif parsed.path == "/api/projects/transition":
                    project_id = data["id"]
                    action = data.get("action", "archive")
                    project = conn.execute("select * from projects where id=?", (project_id,)).fetchone()
                    if not project:
                        self.send_json({"error": "project not found"}, 404); return
                    t = now()
                    if action == "archive":
                        status = "archived"
                    elif action == "restore":
                        status = "maintenance"
                    else:
                        self.send_json({"error": "invalid project action"}, 400); return
                    conn.execute("update projects set status=?, updated_at=? where id=?", (status, t, project_id))
                    add_activity(conn, f"Project {status}: {project['title']}", project["body"], "Project", status)
                    conn.commit()
                elif parsed.path == "/api/tasks":
                    try:
                        task = create_task(conn, data)
                    except ValueError as exc:
                        self.send_json({"error": str(exc)}, 400); return
                    self.send_json({"task": task, "state": state(conn)}, 201)
                    return
                elif parsed.path == "/api/tasks/update":
                    try:
                        task = update_task(conn, data)
                    except ValueError as exc:
                        self.send_json({"error": str(exc)}, 400); return
                    if not task:
                        self.send_json({"error": "task not found"}, 404); return
                    self.send_json({"task": task, "state": state(conn)})
                    return
                elif parsed.path == "/api/tasks/transition":
                    task_id = data["id"]
                    action = data.get("action", "run")
                    updated = transition_task(conn, task_id, action)
                    if not updated:
                        self.send_json({"error": "task not found"}, 404); return
                else:
                    self.send_json({"error": "not found"}, 404); return
                self.send_json(state(conn))
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--token", default=None)
    ap.add_argument("--no-token", action="store_true", help="Disable token check; only safe on localhost")
    ap.add_argument("--reset", action="store_true", help="Reset SQLite demo data before serving")
    args = ap.parse_args(argv)

    with connect() as conn:
        seed(conn, force=args.reset)
    token = args.token or ensure_token()
    require_token = not args.no_token and args.host not in {"127.0.0.1", "localhost", "::1"}
    if args.no_token and args.host not in {"127.0.0.1", "localhost", "::1"}:
        print("WARNING: token disabled on LAN bind; this exposes private data", file=sys.stderr)
    handler = lambda *h_args, **h_kwargs: Handler(*h_args, token=token, require_token=require_token, **h_kwargs)
    httpd = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Clever Cockpit serving http://{args.host}:{args.port}/")
    if require_token:
        print(f"LAN token required. Open with: http://<host>:{args.port}/?token={token}")
    else:
        print("Token check disabled for localhost/default mode." if args.no_token else "Localhost mode: API token not required.")
    httpd.serve_forever()
    return 0


def redact_token(text: str) -> str:
    text = re.sub(r"([?&]token=)[^\s&]+", r"\1***", text)
    text = re.sub(r"(Bearer\s+)[A-Za-z0-9._~+\-/=]+", r"\1***", text)
    return text


if __name__ == "__main__":
    raise SystemExit(main())
