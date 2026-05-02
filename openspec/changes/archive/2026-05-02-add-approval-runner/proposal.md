# add-approval-runner

## Why

Cockpit approvals currently update SQLite state, but nothing automatically resumes or executes the approved workflow. This creates a gap: the human clicks OK, then Clever still needs to manually inspect state.

## What changes

- Add durable approval consumption semantics so accepted approvals can be claimed exactly once.
- Add a polling runner that periodically checks accepted approvals and dispatches registered handlers.
- Track execution state in activity and approval metadata.
- Keep arbitrary command execution out of the UI/API; only local allowlisted handler code may run.

## Impact

- Adds SQLite migration columns to approvals.
- Adds `/api/approvals/ready` and `/api/approvals/complete` for runner integration.
- Adds `scripts/approval_runner.py` for periodic checking.
