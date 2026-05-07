# Отчёт по scheduled задачам — 7 мая, утро

Сводка: done — 4 / waiting — 0 / blocked — 0 / not run — 1.

## Выполнено

- **Добавить watchlist тем в Telegram Review workflow** — done, last_run_at 2026-05-06 09:11 МСК. Evidence: добавлен watchlist в `create-cockpit-ideas-from-review.py`, `py_compile`/dry-run/validate прошли.
- **Проверить SKOS-like taxonomy для тем памяти и дайджестов** — done. Evidence: создан `docs/skos-like-memory-digest-taxonomy-2026-05-06.md`, validate прошёл.
- **Провести mini-spike Lazyweb/design-agent stack** — done. Evidence: отчёт `docs/lazyweb-design-agent-mini-spike-2026-05-06.md` + research artifacts по 3 UI-сценариям.
- **Проверить lite/ultra compression policy** — done. Evidence: создан `docs/compression-policy-mini-eval-2026-05-06.md`, validate прошёл.

## Требует внимания

- **Сравнить Hermes Kanban с Cockpit/TaskFlow UI** — Inbox: создано.
  - Что сделано: карточка переписана понятным русским языком; Hermes сохранён как будущий критерий сравнения для board/handoff UI.
  - Проблема: сейчас нет активной board/handoff/stale-work UI-задачи, сравнение было бы преждевременным.
  - Нужно от Вадима: когда появится реальная board/handoff/stale-work UI-задача, вернуть карточку в работу и решить — переносим Hermes-паттерн в Cockpit/TaskFlow или явно отказываемся.

## Не запускалось / аномалии

- **Добавить source-health smoke для Reddit RSS и Telegram channels…** — scheduled_for 2026-05-07 04:30 МСК, last_run_at пустой, run_status=scheduled, last_error нет. На момент утреннего отчёта задача выглядела не запущенной.

## Follow-up вечером 2026-05-07

Аномалия разобрана: host-side scheduled gate запускался cron-ом в 04:35, но падал до enqueue из-за `FileNotFoundError: 'openclaw'` — у cron не было нужного PATH. Исправлены `scripts/cockpit-scheduled-task-runner-gate.py` и `scripts/cockpit-queued-task-runner-gate.py`: теперь они вызывают `/home/clever/.npm-global/bin/openclaw` напрямую.

Также проверен source-health smoke в `scripts/schedule-watchdog.py`:

- Reddit RSS smoke: `r/LocalLLaMA`, posts=1;
- Telegram channel smoke: `@countwithsasha`, channels=1, posts=1.

Задача `source-health smoke` закрыта в Cockpit как done, создан Inbox confirmation. Evidence: `python3 scripts/schedule-watchdog.py --json`, `python3 -m py_compile ...`, `python3 github/clever-cockpit/scripts/validate.py`.
