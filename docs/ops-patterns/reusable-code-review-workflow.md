# Reusable workflow for complex code tasks

## Что сделано

Оформлен reusable review workflow для сложных кодовых задач: **scout plan → test fork → implementation → deep review**. Шаблон не заменяет быстрый path для простых исправлений.

## Зачем это нужно / как влияет на UX Вадима

Для сложных изменений Вадим получает меньше “сразу закодил и сломал” и больше управляемости: сначала разведка и критерии, потом изолированная проверка, потом реализация, потом независимый review. Для маленьких задач не добавляем бюрократию.

## Когда применять

Применять, если есть хотя бы один пункт:

- изменение затрагивает несколько модулей/интеграций;
- высок риск регрессии, безопасности, данных или внешних side effects;
- непонятна root cause;
- нужен PR-quality патч, а не локальная заметка.

Не применять для очевидных doc edits, маленьких config tweaks, single-file bugfixes с ясным тестом.

## Шаблон

### 1. Scout plan

Artifact: краткий план с файлами, рисками, тестами, критериями успеха.
Stop: есть 1–3 routes или явный blocker; без production edits.

### 2. Test fork

Artifact: минимальный failing/reproducing test или dry-run harness в отдельной ветке/worktree/session.
Stop: test fails for the right reason, or blocker documented.

### 3. Implementation

Artifact: smallest patch + migrations/docs if needed.
Stop: targeted tests/lint/build pass or fail with clear residual blocker.

### 4. Deep review

Artifact: blocking/non-blocking findings with file refs; verify tests and edge cases.
Stop: no blockers, or implementation returned with concrete comments.

## Copy-paste prompt skeleton

```text
Role: <scout|tester|implementer|reviewer>
Context: <repo/path/problem/constraints/prior artifacts>
Artifact: <plan|test|patch|review findings>
Stop criterion: <exact done condition / blocker condition>
Safety: no destructive/external writes unless explicitly approved.
```

## Что дальше

Nothing else is planned for this task; use this pattern only for complex code tasks and keep the fast path for simple ones.

## Доказательства

Artifact: `docs/ops-patterns/reusable-code-review-workflow.md`; workspace guidance references the pattern in `AGENTS.md`.
