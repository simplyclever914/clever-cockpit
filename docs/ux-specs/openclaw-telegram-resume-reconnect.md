# OpenClaw Telegram/mobile UX spec: resume/reconnect

## Что сделано

Сформулирована UX-спецификация для `resume/reconnect`: кнопки `Продолжить`, `Подключиться`, `Открыть заново` возвращают Вадима в существующую session/run без потери контекста и без создания лишних чатов.

## Зачем это нужно / как влияет на UX Вадима

На мобильном главный провал — потеря ориентации: «где мой run?» и «я случайно создам новый контекст?». Resume/reconnect снижает тревожность, уменьшает дубли sessions и делает OpenClaw похожим на устойчивый пульт управления, а не на поток одноразовых сообщений.

## User flow

1. Вадим открывает карточку активной или недавней session.
2. Карточка показывает state: `running`, `waiting approval`, `done`, `failed`, `stale`, `archived`.
3. Основное действие зависит от состояния:
   - `running`: `Подключиться` + `Последние логи`;
   - `waiting`: `Открыть approval` + `Подключиться`;
   - `done`: `Открыть результат` + `Продолжить в этой session`;
   - `failed/stale`: `Открыть заново` + `Создать follow-up`.
4. Reply/steer в thread или bound chat продолжает существующую session, если session id валиден.

## Telegram UI / mock buttons

```text
🧭 Session: clever-cockpit / task-runner
State: waiting approval · last: 04:27 UTC
Context: github/clever-cockpit · model: gpt-5.5

[Подключиться] [Последние логи]
[Открыть approval] [Создать follow-up]
```

Для completed run:

```text
✅ Run завершён: weekly digest dry-run
Artifacts: docs/weekly-digests/...md

[Открыть результат] [Продолжить в этой session]
[Вернуть в работу] [Подтвердить done]
```

## Backend/API данные

- `session_id`, `run_id`, `channel_binding`, `thread_id/chat_id`, `repo/cwd`, `model`, `state`, `last_activity_at`.
- `resume_token`/capability scoped to user+channel, TTL for stale sessions.
- Idempotent `resumeSession(session_id, intent)` that never creates a new thread unless `intent=new_followup`.

## Edge cases / риски

- Session already completed: show result card, not blank resume.
- Session expired: offer `Открыть заново` with copied context summary.
- Multiple matching sessions: show recent picker, not silent attach.
- Privacy: never attach a session to a chat/user that does not match original visibility policy.

## Что дальше

Follow-up should be created for implementation after selecting priority with pinned session card. Suggested dev tasks:

1. Add session lookup + Telegram action payloads for `attach/resume/reopen`.
2. Add recent session picker with state-aware primary actions.
3. Add tests for idempotent resume and cross-chat visibility denial.

## Доказательства

Artifact: `docs/ux-specs/openclaw-telegram-resume-reconnect.md`. Scope intentionally design-only; no production code changed.
