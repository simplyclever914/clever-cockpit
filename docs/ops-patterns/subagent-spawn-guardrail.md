# Subagent spawn guardrail

## Что сделано

Добавлен короткий self-check перед spawn/subagent: **role, context, artifact, stop criterion**. Он нужен перед созданием отдельной сессии, чтобы не запускать расплывчатых “помощников” ради модного multi-agent.

## Зачем это нужно / как влияет на UX Вадима

Вадим получает меньше фонового шума, меньше незакрытых child tasks и более проверяемые результаты: каждый subagent заранее знает роль, входной контекст, ожидаемый артефакт и момент остановки.

## Правило

Перед `sessions_spawn`/ACP/subagent быстро проверить:

1. **Role** — какая отдельная роль реально нужна? scout, reviewer, implementer, researcher, tester.
2. **Context** — какой минимальный вход дать: repo/path, issue, constraints, prior artifacts. Не fork контекст без нужды.
3. **Artifact** — что вернётся: plan, patch, test result, review notes, matrix, report.
4. **Stop criterion** — когда subagent должен остановиться: файл создан, tests passed/failed with logs, top 3 findings, blocker found.

Если любой пункт пустой — не spawn; сделать самому или сначала уточнить задачу.

## Примеры проверки

- Хорошо: “Role=scout; Context=repo + failing test; Artifact=ranked root-cause plan; Stop=top 3 hypotheses with file refs, no code changes.”
- Плохо: “Посмотри код где-нибудь и помоги” — нет артефакта и stop criterion.
- Хорошо: “Role=reviewer; Context=patch diff; Artifact=blocking/non-blocking findings; Stop=after one pass with line refs.”

## Что дальше

Nothing else is planned for this task; future subagent prompts should include these four fields when a spawn is warranted.

## Доказательства

Artifact: `docs/ops-patterns/subagent-spawn-guardrail.md`; workspace guidance also references the guardrail in `AGENTS.md`.
