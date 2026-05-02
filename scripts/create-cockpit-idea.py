#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

WORKSPACE = Path('/home/clever/.openclaw/workspace')
COCKPIT = WORKSPACE / 'github' / 'clever-cockpit'
TOKEN_FILE = COCKPIT / 'data' / 'token'


def post(base_url: str, token: str, path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        base_url.rstrip('/') + path,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main() -> int:
    ap = argparse.ArgumentParser(description='Create a Clever Cockpit idea, optionally with a human decision approval request.')
    ap.add_argument('--base-url', default='http://127.0.0.1:8765')
    ap.add_argument('--token')
    ap.add_argument('--id')
    ap.add_argument('--title', required=True)
    ap.add_argument('--body', default='')
    ap.add_argument('--source', default='schedule')
    ap.add_argument('--approval', action='store_true', help='Also create a pending approval request asking Vadim to review this idea')
    ap.add_argument('--priority', default='normal')
    args = ap.parse_args()

    token = args.token or TOKEN_FILE.read_text(encoding='utf-8').strip()
    idea_payload = {'title': args.title, 'body': args.body, 'source': args.source}
    if args.id:
        idea_payload['id'] = args.id
    idea_result = post(args.base_url, token, '/api/ideas', idea_payload)
    ideas = idea_result.get('state', {}).get('ideas', []) or idea_result.get('ideas', [])
    idea = next((i for i in ideas if i.get('title') == args.title), ideas[0] if ideas else {})
    idea_id = idea.get('id') or args.id or ''
    print(f'idea_created id={idea_id} title={args.title!r}')

    if args.approval:
        approval = {
            'title': f'Review idea: {args.title}',
            'kind': 'idea_review',
            'priority': args.priority,
            'body': f'{args.body}\n\nIdea id: {idea_id}'.strip(),
            'handler': 'record_only',
            'payload': {'note': f'Idea review acknowledged: {idea_id}', 'idea_id': idea_id},
        }
        approval_result = post(args.base_url, token, '/api/approvals', approval)
        item = approval_result.get('approval', {})
        print(f"approval_created id={item.get('id')} handler={item.get('handler')} status={item.get('status')}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
