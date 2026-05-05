#!/usr/bin/env python3
"""Generate a local weekly Telegram knowledge-map digest from the user-search SQLite index.

Safe by default: read-only local DB and markdown artifact only. Publishing/sending is handled by the caller.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_DB = Path(os.environ.get('TELEGRAM_SEARCH_DB', Path.home() / '.openclaw' / 'workspace' / 'data' / 'telegram-search' / 'messages.sqlite'))
URL_RE = re.compile(r'https?://[^\s)\]>"\']+')
TOPIC_KEYWORDS = {
    'AI agents / coding agents': ['agent', 'агент', 'claude', 'codex', 'openclaw', 'qwen', 'pi ', 'skills', 'mcp'],
    'Local LLM / inference': ['llm', 'ollama', 'llama.cpp', 'q4', 'qwen', 'local'],
    'Browser / web automation': ['playwright', 'browser', 'web_fetch', 'snitchmd', 'cloak', 'scrape'],
    'Product UX / agent reliability': ['ux', 'doorDash', 'support', 'ошибка агента', 'пульт', 'workflow'],
    'Tools / repositories': ['github.com', 'repo', 'framework', 'cli'],
    'Writing / content quality': ['текст', 'gpt', 'воняет', 'статья', 'habr.com'],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db', type=Path, default=DEFAULT_DB)
    p.add_argument('--days', type=int, default=7)
    p.add_argument('--limit', type=int, default=300)
    p.add_argument('--chat', action='append', help='Optional chat title/username/id fragment; repeatable')
    p.add_argument('--out', type=Path, required=True)
    return p.parse_args()


def fetch_messages(db: Path, days: int, limit: int, chat_filters: list[str] | None) -> list[sqlite3.Row]:
    since = (dt.datetime.now(dt.UTC) - dt.timedelta(days=days)).isoformat()
    conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    where = ['m.date >= ?', "COALESCE(m.text, '') != ''"]
    params: list[object] = [since]
    if chat_filters:
        parts = []
        for f in chat_filters:
            like = f'%{f}%'
            parts.append('(CAST(m.chat_id AS TEXT) LIKE ? OR COALESCE(c.title,\'\') LIKE ? OR COALESCE(c.username,\'\') LIKE ?)')
            params.extend([like, like, like])
        where.append('(' + ' OR '.join(parts) + ')')
    sql = f'''
      SELECT m.date, m.chat_id, m.message_id, m.sender_name, m.text, m.link,
             COALESCE(c.title, CAST(m.chat_id AS TEXT)) AS chat_title,
             c.username
      FROM messages m LEFT JOIN chats c ON c.chat_id=m.chat_id
      WHERE {' AND '.join(where)}
      ORDER BY m.date DESC
      LIMIT ?
    '''
    params.append(limit)
    return list(conn.execute(sql, params))


def short(text: str, n: int = 220) -> str:
    text = re.sub(r'\s+', ' ', text or '').strip()
    return text if len(text) <= n else text[: n - 1].rstrip() + '…'


def classify(text: str) -> set[str]:
    low = text.lower()
    hits = set()
    for topic, words in TOPIC_KEYWORDS.items():
        if any(w.lower() in low for w in words):
            hits.add(topic)
    return hits or {'Misc / needs human scan'}


def main() -> int:
    args = parse_args()
    rows = fetch_messages(args.db, args.days, args.limit, args.chat)
    now = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    by_topic: dict[str, list[sqlite3.Row]] = defaultdict(list)
    url_counter: Counter[str] = Counter()
    chat_counter: Counter[str] = Counter()
    for r in rows:
        chat_counter[r['chat_title']] += 1
        for u in URL_RE.findall(r['text'] or ''):
            url_counter[u.rstrip('.,;')] += 1
        for topic in classify(r['text'] or ''):
            by_topic[topic].append(r)

    lines = [
        '# Weekly Telegram knowledge map digest', '',
        f'Generated: {now}',
        f'Window: last {args.days} days · messages sampled: {len(rows)}', '',
        '## 5–7 knowledge-map bullets', ''
    ]
    for topic, items in sorted(by_topic.items(), key=lambda kv: len(kv[1]), reverse=True)[:7]:
        lines.append(f'### {topic} ({len(items)})')
        for r in items[:3]:
            source = r['link'] or f"chat={r['chat_title']} msg={r['message_id']}"
            lines.append(f"- {r['date']} · {r['chat_title']}: {short(r['text'])}  ")
            lines.append(f"  Source: {source}")
        lines.append('')

    lines += ['## Top sources/chats', '']
    for chat, count in chat_counter.most_common(10):
        lines.append(f'- {chat}: {count}')
    lines += ['', '## Top URLs', '']
    for url, count in url_counter.most_common(20):
        lines.append(f'- {url}' + (f' ({count} mentions)' if count > 1 else ''))
    lines += ['', '## Next step', '', 'Review the recurring themes and decide what should become a concrete Cockpit task or deeper research thread.']

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(args.out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
