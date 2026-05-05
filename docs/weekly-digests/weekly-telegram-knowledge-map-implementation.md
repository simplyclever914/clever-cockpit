# Weekly Telegram knowledge map digest — implementation plan

## Что сделано

Подготовлен безопасный runnable implementation path для weekly Telegram knowledge map digest: суббота 11:00 Europe/Moscow, сбор из существующего Telegram user-search index, локальный markdown dry-run, дальнейшая публикация SourceCraft и pinned announcement через существующий send-and-pin helper.

## Зачем это нужно / как влияет на UX Вадима

Вадим получает не просто дневной поток ссылок, а еженедельную карту повторяющихся тем, новых источников и сильных инсайтов. Публикация SourceCraft даёт устойчивую ссылку, pinned announcement помогает не потерять выпуск в Telegram.

## Safe schedule

Cron expression for Europe/Moscow host time:

```cron
0 11 * * 6 cd "$HOME/.openclaw/workspace" && python3 github/clever-cockpit/scripts/weekly_telegram_knowledge_map_digest.py --days 7 --limit 300 --out digests/weekly-telegram-knowledge-map/$(date +\%F).md
```

Publishing/pinning should be a second explicit step after successful local artifact generation:

```bash
# publish markdown/html with SourceCraft flow, then announce/pin the resulting URL
scripts/telegram-send-and-pin-digest.mjs --title "Weekly Telegram knowledge map" --url "$SOURCECRAFT_URL" --pin
```

## Data flow

1. Export recent allowlisted Telegram messages using local index; no new chats, no secret printing.
2. Extract URLs, chat titles, dates, and short snippets.
3. Cluster into 5–7 knowledge-map bullets: recurring themes, new sources, useful links.
4. Save local markdown artifact.
5. Publish to SourceCraft only after artifact looks valid.
6. Send pinned announcement using existing Telegram helper and configured target.

## Dry-run result

A local dry-run artifact was generated at `artifacts/weekly-telegram-knowledge-map-dry-run-2026-05-05.md` from recent MyBookmarks/index sample.

## Что дальше

A human decision is needed before enabling live cron/pinning: confirm the exact Telegram delivery target/channel for the pinned announcement and approve installing the cron entry. Until then, the runnable implementation and dry-run artifact are prepared, but no external delivery was performed.

## Доказательства

- Implementation script: `scripts/weekly_telegram_knowledge_map_digest.py`.
- Dry-run artifact: `artifacts/weekly-telegram-knowledge-map-dry-run-2026-05-05.md`.
- Telegram user-search safety rules followed: local allowlisted index/read only, no sends.
