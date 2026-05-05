# OpenClaw Telegram/mobile UX spec: mobile command palette

## Что сделано

Сформулирована UX-спецификация mobile command palette: компактные buttons/selects для `status`, `stop`, `steer`, `artifacts`, `recent sessions`, `approvals` вместо запоминания slash-команд.

## Зачем это нужно / как влияет на UX Вадима

На телефоне ввод slash-команд и длинных id ломает flow. Command palette превращает OpenClaw в быстрый мобильный пульт: меньше ошибок, быстрее approvals/status, проще вернуться к нужному run.

## User flow

1. Вадим нажимает `Меню` под любой session/result card или отправляет короткое `menu`.
2. Palette показывает top actions по контексту текущей session.
3. Для глобального контекста показывает recent sessions, approvals, active runs и inbox.
4. Выбор action открывает подменю или выполняет безопасное действие. Опасные действия требуют подтверждения.

## Telegram UI / mock buttons

```text
⚙️ OpenClaw actions
Current: clever-cockpit · running

[Status] [Logs] [Steer]
[Artifacts] [Approvals]
[Recent sessions] [Stop…]
```

Stop submenu:

```text
Stop run? This interrupts current work.
[Cancel] [Stop once]
```

## Backend/API данные

- Context resolver: current inbound message/thread → session/run/project.
- Action registry with labels, safety class, required confirmation, provider capability.
- Compact callback payloads: action id + scoped target id + nonce/TTL.

## Edge cases / риски

- Payload length limits: store state server-side, send short callback ids.
- Stale callbacks: respond with refreshed card instead of failing silently.
- Dangerous actions: stop/delete/external writes need explicit confirmation.

## Что дальше

Follow-up should be created for a small Telegram-only MVP. Suggested dev tasks:

1. Implement context-aware action registry and callback dispatch.
2. Add palette rendering for active session and global home states.
3. Add tests for stale callback, wrong user, and destructive confirmation.

## Доказательства

Artifact: `docs/ux-specs/openclaw-telegram-mobile-command-palette.md`. Design-only; no bot UI changed.
