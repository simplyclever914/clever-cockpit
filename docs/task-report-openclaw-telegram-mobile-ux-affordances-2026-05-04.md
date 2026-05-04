# OpenClaw Telegram/mobile UX affordances

## Что сделано

Подготовлен список из 7 UX affordances для OpenClaw Telegram/mobile agent control. Цель — уменьшить неопределённость на мобильном, не потерять активные runs/approvals и сделать управление агентами понятным без знания внутренних команд.

## Рекомендованные affordances

1. **Pinned session card** — одно устойчивое Telegram-сообщение на активную agent/session с model, cwd/repo, state, last activity и next action. Priority: high.
2. **Live log tail on demand** — кнопка/команда `logs` показывает последние 30–80 строк и action “open full thread/resume”, вместо дампа всего лога в чат.
3. **Approval inbox with exact command preview** — approvals собраны в одном месте; показывают точную shell/external-команду и дают one-tap accept/deny, где это поддерживается.
4. **Resume/reconnect affordance** — mobile-friendly “continue this run” и “attach to existing session”, а не только новый чат/новая сессия.
5. **Pinning and quiet modes** — важные runs/results можно pin; noisy background progress молчит до done/blocked/decision-needed.
6. **Mobile command palette** — компактные buttons/selects для status, stop, steer, artifacts, recent sessions, approvals; не заставлять помнить slash syntax.
7. **Artifact/result card** — после завершения показывать concise evidence + links/files/tests, с actions “confirm done / return to work”.

## Приоритет

Начать с двух вещей:

- **Pinned session card** — снижает мобильную неопределённость: что сейчас работает, где, что ожидает.
- **Approval inbox** — предотвращает пропущенные решения и делает external/destructive actions проверяемыми.

## Почему задача не закрыта автоматически

Отчёт был подготовлен, но первоначальная доставка через `sessions_send` из isolated task runner не дошла из-за `tools.sessions.visibility=tree`. Это ошибка workflow доставки, а не отсутствие результата. Теперь отчёт опубликован отдельно на SourceCraft, а ссылка должна быть сохранена в карточке задачи.

## Что требуется от Вадима

Подтвердить, считать ли этот список достаточным, и выбрать 1–2 affordances для следующей реализации/проработки.
