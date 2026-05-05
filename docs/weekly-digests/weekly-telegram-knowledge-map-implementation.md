# Weekly Telegram knowledge map digest — implementation plan

## Что сделано

Подготовлен и включён weekly Telegram knowledge map digest: суббота 11:00 Europe/Moscow, сбор из существующего Telegram user-search index, локальный markdown artifact, публикация SourceCraft и pinned announcement в Telegram direct chat Вадима.

## Зачем это нужно / как влияет на UX Вадима

Вадим получает не просто дневной поток ссылок, а еженедельную карту повторяющихся тем, новых источников и сильных инсайтов. Публикация SourceCraft даёт устойчивую ссылку, pinned announcement помогает не потерять выпуск в Telegram.

## Schedule

OpenClaw cron: `0 11 * * 6` in `Europe/Moscow`.

Workflow:

```bash
cd "$HOME/.openclaw/workspace"
date=$(TZ=Europe/Moscow date +%F)
md="digests/weekly-telegram-knowledge-map/${date}.md"
site="digests/out/weekly-telegram-knowledge-map-${date}"
python3 github/clever-cockpit/scripts/weekly_telegram_knowledge_map_digest.py --days 7 --limit 300 --out "$md"
python3 scripts/markdown-digest-to-html.py "$md" "$site" --title "Weekly Telegram knowledge map — ${date}" --note "Weekly map from Vadim's local Telegram index."
python3 skills/sourcecraft-publisher/scripts/publish_static.py --source "$site" --slug "weekly-telegram-knowledge-map-${date}" --date "$date"
```

The cron then sends and pins a short Telegram announcement through `scripts/telegram-send-and-pin-digest.mjs weekly_knowledge ...`.

## Data flow

1. Export recent allowlisted Telegram messages using local index; no new chats, no secret printing.
2. Extract URLs, chat titles, dates, and short snippets.
3. Cluster into 5–7 knowledge-map bullets: recurring themes, new sources, useful links.
4. Save local markdown artifact.
5. Publish to SourceCraft only after artifact looks valid.
6. Send pinned announcement using existing Telegram helper and configured target.

## Dry-run result

A local dry-run artifact was generated at `local-artifacts/clever-cockpit/2026-05-05/weekly-telegram-knowledge-map-dry-run-2026-05-05.md` from recent MyBookmarks/index sample.

## Что дальше

Enabled after Vadim confirmed cron is allowed and the delivery target is the current Telegram direct chat.

## Доказательства

- Implementation script: `scripts/weekly_telegram_knowledge_map_digest.py`.
- Dry-run artifact: `artifacts/weekly-telegram-knowledge-map-dry-run-2026-05-05.md`.
- Telegram user-search safety rules followed: local allowlisted index/read only, no sends.
