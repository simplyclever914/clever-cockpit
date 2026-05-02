#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

WORKSPACE = Path('/home/clever/.openclaw/workspace')
COCKPIT = WORKSPACE / 'github' / 'clever-cockpit'
TOKEN_FILE = COCKPIT / 'data' / 'token'


def request_json(base_url: str, token: str, payload: dict) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        base_url.rstrip('/') + '/api/approvals',
        data=body,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json; charset=utf-8',
        },
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))


def ensure_file(path: str, *, allow_tmp: bool = True) -> str:
    p = Path(path).expanduser().resolve()
    allowed = [WORKSPACE.resolve()]
    if allow_tmp:
        allowed.append(Path('/tmp').resolve())
    if not any(p == root or root in p.parents for root in allowed):
        raise SystemExit(f'path outside allowed roots: {p}')
    if not p.exists():
        raise SystemExit(f'path does not exist: {p}')
    return str(p)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Create a typed Clever Cockpit approval for workflow output.')
    ap.add_argument('--base-url', default='http://127.0.0.1:8765')
    ap.add_argument('--token', default=None)
    ap.add_argument('--id')
    ap.add_argument('--title', required=True)
    ap.add_argument('--body', default='')
    ap.add_argument('--priority', default='high')
    ap.add_argument('--kind', default='workflow')
    ap.add_argument('--handler', required=True, choices=['record_only', 'telegram_send_and_pin_digest', 'sourcecraft_publish', 'digest_publish_and_send'])
    ap.add_argument('--job-key', choices=['reflection', 'ai_wrapup', 'telegram_radar'])
    ap.add_argument('--text-file')
    ap.add_argument('--source')
    ap.add_argument('--slug')
    ap.add_argument('--date')
    ap.add_argument('--message')
    ap.add_argument('--payload-json', help='Extra payload JSON object merged last')
    args = ap.parse_args(argv)

    token = args.token or TOKEN_FILE.read_text(encoding='utf-8').strip()
    payload: dict = {}
    if args.job_key:
        payload['job_key'] = args.job_key
    if args.text_file:
        payload['text_file'] = ensure_file(args.text_file, allow_tmp=True)
    if args.source:
        payload['source'] = ensure_file(args.source, allow_tmp=False)
    if args.slug:
        payload['slug'] = args.slug
    if args.date:
        payload['date'] = args.date
    if args.message:
        payload['message'] = args.message
    if args.payload_json:
        extra = json.loads(args.payload_json)
        if not isinstance(extra, dict):
            raise SystemExit('--payload-json must be a JSON object')
        payload.update(extra)

    approval = {
        'title': args.title,
        'kind': args.kind,
        'priority': args.priority,
        'body': args.body,
        'handler': args.handler,
        'payload': payload,
    }
    if args.id:
        approval['id'] = args.id

    result = request_json(args.base_url, token, approval)
    item = result.get('approval', {})
    print(f"approval_created id={item.get('id')} handler={item.get('handler')} status={item.get('status')}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
