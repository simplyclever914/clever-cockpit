# OpenClaw Telegram/mobile UX spec: quiet modes + pinning

## Что сделано

Сформулирована UX-спецификация для quiet modes и pinning: background runs молчат до `done/blocked/decision-needed`, а важные sessions/results можно закрепить и снять с закрепления.

## Зачем это нужно / как влияет на UX Вадима

Вадиму нужен контроль без постоянного шума. Quiet mode уменьшает Telegram fatigue, а pinned карточка сохраняет видимыми действительно важные runs и результаты. Это особенно важно ночью/утром и для task runner, где много фоновых шагов.

## User flow

1. При запуске background run можно выбрать режим: `Normal`, `Quiet until done`, `Quiet unless blocked`, `Verbose`.
2. В quiet mode промежуточные heartbeat/status сообщения не отправляются наружу; сохраняются только activity/logs.
3. Если run требует решения, падает или завершился — отправляется compact result/attention card.
4. Вадим может pin/unpin карточку session или итоговый result.

## Telegram UI / mock buttons

```text
🔕 Background run запущен тихо
Notify: done / blocked / decision needed

[Показать статус] [Включить verbose]
[Pin session] [Stop]
```

```text
📌 Pinned: Cockpit task runner
State: running · quiet until blocked/done

[Logs] [Unpin] [Steer] [Stop]
```

## Backend/API данные

- `notification_mode`: `normal|quiet_done|quiet_blocked|verbose`.
- `pin_state`: `none|session|result`, plus provider message id.
- Delivery policy that collapses repeated non-critical updates into activity only.
- Provider adapter support for pin/unpin best-effort + explicit fallback when unsupported.

## Edge cases / риски

- Telegram pin permissions may be missing: show fallback “saved important card” and keep internal pinned list.
- Quiet mode must not suppress approvals, blockers, failures, or security prompts.
- Avoid pin spam: one active pinned session card per task/project unless user pins manually.

## Что дальше

Follow-up should be created after pinned session card MVP. Suggested dev tasks:

1. Add `notification_mode` to run/session metadata and delivery filter tests.
2. Add Telegram `pin/unpin` actions with graceful unsupported-provider fallback.
3. Add UI copy for quiet mode status and unblock notifications.

## Доказательства

Artifact: `docs/ux-specs/openclaw-telegram-quiet-modes-pinning.md`. Design-only; no external pin/send performed.
