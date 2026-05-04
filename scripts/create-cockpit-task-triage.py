#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'cockpit.sqlite'


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def main() -> int:
    ap = argparse.ArgumentParser(description='Create/update one Inbox triage card for open/idle Cockpit tasks.')
    ap.add_argument('--db', default=str(DB))
    ap.add_argument('--limit', type=int, default=30)
    args = ap.parse_args()
    con = sqlite3.connect(args.db); con.row_factory = sqlite3.Row
    tasks = con.execute("""
        select id,title,project,created_at,updated_at,trigger from tasks
        where status='open' and coalesce(run_status,'idle')='idle'
        order by updated_at asc
        limit ?
    """, (args.limit,)).fetchall()
    t = now()
    approval_id = 'task-triage-open-idle'
    if not tasks:
        con.execute("update approvals set status='rejected', run_status=null, last_error=null, updated_at=? where id=? and status='pending'", (t, approval_id))
        con.commit()
        print('no open/idle tasks')
        return 0
    by_project: dict[str, list[sqlite3.Row]] = {}
    for row in tasks:
        by_project.setdefault(row['project'] or 'Inbox', []).append(row)
    lines = []
    for project, rows in by_project.items():
        lines.append(f"{project}:")
        for row in rows:
            lines.append(f"- `{row['id']}` — {row['title']} (updated {row['updated_at']})")
    body = (
        f"Найдено {len(tasks)} задач в тихом состоянии `open/idle`: они не scheduled, не queued и не видны Вадиму как отдельные решения.\n\n"
        "Что требуется от Вадима/Клевера:\n"
        "- выбрать 1–3 задачи, которые надо поставить в run/queue;\n"
        "- остальное оставить в backlog/park, schedule или cancel;\n"
        "- не держать новые задачи в `open/idle` как скрытый долг.\n\n"
        + "\n".join(lines)
    )
    payload = {'task_ids': [r['id'] for r in tasks], 'count': len(tasks), 'source': 'open_idle_triage'}
    existing = con.execute('select 1 from approvals where id=?', (approval_id,)).fetchone()
    if existing:
        con.execute("""
            update approvals set title=?,kind='task_triage',priority='high',body=?,status='pending',handler='record_only',payload_json=?,run_status=null,claimed_at=null,completed_at=null,last_error=null,updated_at=? where id=?
        """, ('Разобрать open/idle задачи', body, json.dumps(payload, ensure_ascii=False), t, approval_id))
        action = 'updated'
    else:
        con.execute("""
            insert into approvals(id,title,kind,priority,body,status,handler,payload_json,run_status,claimed_at,completed_at,last_error,created_at,updated_at)
            values (?,?,?,?,?,'pending','record_only',?,null,null,null,null,?,?)
        """, (approval_id, 'Разобрать open/idle задачи', 'task_triage', 'high', body, json.dumps(payload, ensure_ascii=False), t, t))
        action = 'created'
    con.execute('insert into activity(title,kind,status,priority,body,created_at) values (?,?,?,?,?,?)', ('Open/idle task triage requested', 'TaskTriage', 'pending', 'high', body, t))
    con.commit()
    print(f'{action} {approval_id} count={len(tasks)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
