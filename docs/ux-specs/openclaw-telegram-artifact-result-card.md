# OpenClaw Telegram/mobile UX spec: artifact/result card

## Что сделано

Сформулирована UX-спецификация artifact/result card после завершения run: concise evidence, links/files/tests и actions `confirm done`, `return to work`, `create follow-up tasks`.

## Зачем это нужно / как влияет на UX Вадима

Сейчас завершение работы легко превращается в длинный текст без явного решения. Result card помогает быстро понять: что изменилось, почему это полезно, можно ли закрывать, какие доказательства есть, и что нажать дальше. Это напрямую поддерживает замечание Вадима: после `OK` задача не должна исчезать без понятного follow-up/возврата.

## User flow

1. Run завершился или перешёл в waiting/partial.
2. Telegram показывает одну итоговую карточку с обязательными секциями: сделано, impact/UX, дальше, доказательства.
3. Вадим выбирает действие: подтвердить, вернуть с комментарием, создать follow-up, открыть артефакт.
4. Cockpit/task runner обновляет task status только после подтверждённого состояния и сохраняет per-task report.

## Telegram UI / mock buttons

```text
✅ Task result: Artifact/result card spec
Что сделано: UX spec + dev tasks
UX effect: меньше потерянных результатов и непонятных OK
Что дальше: нужен выбор — делать MVP или отложить
Доказательства: docs/ux-specs/...md

[Confirm done] [Send back with comment]
[Create follow-up] [Open artifact]
```

For waiting:

```text
⚠️ Нужен выбор Вадима
Сделано: dry-run готов
Проблема: неизвестен delivery target для pinned announce
Нужно: выбрать чат/channel

[Reply with decision] [Snooze]
```

## Backend/API данные

- `result_summary`: done/impact/next/evidence fields.
- `artifact_links`: local path, SourceCraft URL, test output, PR/commit if any.
- `next_actions`: confirm, return_with_comment, create_followup, open_artifact.
- Idempotent confirmation/attention Inbox item linked to task id.

## Edge cases / риски

- Do not mark done without evidence.
- If `impact` or `next` is unclear, create attention instead of done.
- Long reports should be SourceCraft pages; short reports can be appended to task notes.

## Что дальше

Follow-up should be created for Cockpit/OpenClaw result-card MVP because it fixes a live workflow pain. Suggested dev tasks:

1. Normalize result summary schema across task runner confirmations/attention.
2. Add Telegram action `Send back with comment` and route it to task notes/status.
3. Render result cards from per-task reports and keep task visible until confirmed.

## Доказательства

Artifact: `docs/ux-specs/openclaw-telegram-artifact-result-card.md`. Design reflects Vadim feedback saved in parent task notes.
