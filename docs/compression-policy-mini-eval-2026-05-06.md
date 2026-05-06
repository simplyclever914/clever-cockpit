# Mini-eval: lite/ultra compression policy для MEMORY/skill/tool описаний — 2026-05-06

## Цель
Проверить, стоит ли применять Wenyan/caveman-style compression к системным описаниям памяти, skills и tool/process rules.

## Сэмплы
1. `MEMORY.md` tooling preferences/report rule — высокорисковые пользовательские ограничения.
2. `weather/SKILL.md` — низкорисковый skill с понятной внешней командой.
3. `docs/architecture-guardrails.md` — методический документ для code review.
4. TaskRunner instruction — строгий procedural contract с SQLite/reporting правилами.
5. Telegram Review extraction script comments/rules — workflow hints и filters.

## Варианты сжатия

### Lite
Сохраняет MUST/NEVER, условия применения, команды и исключения; убирает повторы и prose.

Пример для per-task report rule:
> Scheduled/Cockpit tasks: every done task needs per-task Russian report. Short => append task `user_notes`; long => SourceCraft page + Report URL. Group summary does not replace task report. Blockers => Inbox attention with done/problem/needed. Do not use sessions_send from isolated runner.

### Ultra / caveman
Оставляет только телеграфные опорные слова.

Пример:
> Task done? Russian report. Short notes. Long SourceCraft URL. No group substitute. Blocked? Inbox attention. No sessions_send isolated.

## Проверка на 5 реальных задач

| Задача | Full | Lite | Ultra | Риск потери |
|---|---:|---:|---:|---|
| Scheduled task finalization/report | ✅ | ✅ | ⚠️ | Ultra легко теряет exact commands/fields и “do nothing else” для NO_TASKS. |
| Weather forecast | ✅ | ✅ | ✅ | Низкий риск: intent простой, tool narrow. |
| Architecture review guardrails | ✅ | ✅ | ⚠️ | Ultra теряет критерии “architecture drift” и когда нужен ADR. |
| Telegram Review candidate extraction | ✅ | ✅ | ⚠️ | Ultra может превратить watchlist в noisy auto-create tasks. |
| Permission/OAuth audit reminder | ✅ | ✅ | ❌ | Ultra теряет контекст риска и scope; опасно для security tasks. |

## Экономия контекста (приближённо по символам)
- Full sample excerpts: ~900 chars each.
- Lite: обычно 35–55% от full.
- Ultra: 12–25% от full.

## Вывод
Lite compression полезна для длинных вспомогательных описаний, если сохранять императивы (`MUST/NEVER`), exact commands, blockers и safety constraints. Ultra/caveman можно использовать только для **индексов, labels, quick reminders**, но не как единственный источник инструкций.

## Рекомендация
- `MEMORY.md`, TaskRunner, safety/permission rules: full или lite-with-verbatim-critical-blocks.
- Skills: lite summary допустим как prefilter, но перед применением читать полный `SKILL.md`.
- Tool descriptions: не сжимать поля схем/команды; можно сжимать prose вокруг.
- Digest topics/watchlists: lite labels ок; ultra только для taxonomy aliases.

Следующий шаг: ничего автоматически не внедрять. Если Вадим захочет, создать follow-up “compression prefilter for low-risk skill summaries” с eval gate на точность инструкций.
