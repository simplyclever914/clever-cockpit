# SKOS-like taxonomy для memory/digest тем — 2026-05-06

## Цель
Проверить, помогает ли маленький словарь `broader/narrower/related/synonyms` связывать реальные темы из memory/digest workflow без тяжёлой RDF-инфры.

## Мини-словарь

| concept | broader | narrower | related | synonyms / aliases |
|---|---|---|---|---|
| agentic-dev | ai-workflows | coding-agents, evals, harness | daily-digests, openclaw-tools | AI agents, agentic engineering |
| coding-agents | agentic-dev | codex, claude, cursor | permissions, tests | coding agent, dev agent |
| codex | coding-agents | codex-desktop, codex-goal | claude, session-management | Codex CLI, Codex App, `/goal` |
| claude | coding-agents | claude-routines, ultrareview | codex, review-workflow | Claude Code, Opus |
| session-management | agentic-dev | persistent-sessions, resume, live-logs | cockpit, taskflow | Agent Sessions, sessions layer |
| taskflow | openclaw-tools | durable-tasks, waits, child-tasks | cockpit, scheduled-runner | TaskFlow, detached tasks |
| cockpit | openclaw-tools | tasks, ideas, inbox, approvals | taskflow, mobile-ux | Clever Cockpit |
| scheduled-runner | cockpit | due-tasks, reports, confirmations | inbox, taskflow | cron runner, TaskRunner |
| telegram-review | daily-digests | watchlist, digest-candidates | telegram-index, cockpit-ideas | Telegram Daily Review |
| watchlist | telegram-review | skill-registry, mcp-lifecycle, lazyweb | digest-candidates | tracked topics, topic watch |
| skill-registry | openclaw-tools | install, update, discovery | skills, watchlist | skill registry/install/update |
| mcp-lifecycle | openclaw-tools | leaks, permissions, cleanup | design-mcp, computer-use | MCP lifecycle leaks |
| lazyweb-design | ui-workflow | design-agent, design-mcp, figma-context | mobile-ux, screenshots | Lazyweb, design-agent stack |
| permissions | safety | oauth-audit, approval-profiles | cursor, github, computer-use | permission profiles, OAuth hygiene |
| evals | quality | mutation-testing, traceability, gates | digests, coding-agents | checks, validation, test gates |
| memory-hygiene | personal-ops | taxonomy, reflection, durable-context | daily-digests, retrieval | memory cleanup, context hygiene |

## Проверка на 3 сценариях

1. **Retrieval: “Codex /goal и Claude routines”**  
   Без словаря это две строковые темы. Со словарём обе попадают в `coding-agents` и связываются с `review-workflow/session-management`; это помогает собрать один digest paragraph вместо двух шумных карточек.

2. **Digest candidates: “skill registry/install/update + MCP lifecycle leaks”**  
   Словарь помечает оба как `openclaw-tools` и `watchlist`, но не делает их action сам по себе. Это полезно как boost/label, а не как автосоздание задач.

3. **Memory lookup: “почему cron runner требует per-task report?”**  
   `scheduled-runner -> cockpit -> inbox/confirmations` связывает правило отчётности с TaskRunner, даже если в тексте встречается “cron”, “scheduled task” или “TaskRunner”.

## Вывод
Маленький SKOS-like файл полезен как **тонкий слой нормализации тем** для memory/digest retrieval и review watchlist. Внедрять RDF/graph DB не нужно: достаточно YAML/JSON/Markdown словаря и одного правила — taxonomy может повышать recall/labels, но не должна сама создавать задачи.

## Рекомендация
Парковать как лёгкий артефакт до следующего улучшения digest/retrieval pipeline. Следующий шаг, если Вадим захочет внедрять: перенести таблицу в machine-readable `memory/topic-taxonomy.json` и использовать только для tagging/boosting candidates.
