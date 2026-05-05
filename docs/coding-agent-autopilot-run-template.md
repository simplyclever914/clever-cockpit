# Coding-agent autopilot run template

Use this only for bounded, reversible work where the repo can be left clean and a human can review the diff before merge/deploy. Do not assume a specific harness; use only agents/tools that are authorized in the current environment.

## 1. Pilot selection

- Repo:
- Task:
- Why this is safe to let run:
- Explicit non-goals / out-of-scope changes:

Default pilot constraints:
- no secrets, credential changes, deploys, billing, or external irreversible writes;
- small code or documentation change;
- easy rollback via branch/worktree deletion or revert;
- local verification command is known before launch.

## 2. Isolation

- Base branch / commit:
- Branch name:
- Worktree path:
- Rollback point:
- Allowed files/directories:
- Forbidden files/directories:

Start condition: the source worktree is clean and the autopilot run happens in an isolated branch/worktree, not in shared dirty state.

## 3. Autopilot brief

Give the agent:

```text
Goal: <one concrete outcome>
Allowed scope: <files/dirs and behavior boundaries>
Stop if: <ambiguity, test failure outside scope, secret/external/destructive action, large unexpected diff>
Verification gate: <exact command(s)>
Expected final report: summary, changed files, verification output, residual risks, cleanup status.
```

## 4. CI / local gate

- Required command(s):
- Acceptable warnings:
- Failure policy:
  - If failure is inside task scope: one fix pass is allowed.
  - If failure is outside task scope or unclear: stop and ask.

The run is not done until the declared gate is green or the remaining failure is explicitly recorded as an agreed blocker.

## 5. Review loop

Reviewer checks:
- diff matches the brief and allowed scope;
- no secrets, generated junk, unrelated refactors, or hidden behavior changes;
- tests/lint/build/smoke evidence is present;
- final report names risks and follow-up work.

Allow at most one autonomous fix pass for review comments unless the human explicitly extends the run.

## 6. Cleanup

Before closing:
- remove temp files and scratch artifacts;
- leave git status understandable;
- record branch/worktree path and cleanup command;
- label/close the task with summary, gate output, and remaining risks.

## 7. Let-it-run checklist

Allow autopilot to continue only if all are true:

- [ ] Task is bounded and reversible.
- [ ] Worktree/branch isolation is in place.
- [ ] Allowed and forbidden scopes are explicit.
- [ ] Local verification gate is known.
- [ ] Stop conditions are explicit.
- [ ] No secrets, deploys, billing, or irreversible external writes are required.
- [ ] Human review happens before merge/deploy.

If any checkbox is false, do not let the agent “ехать самому”; switch to a smaller manual step or ask Vadim.
