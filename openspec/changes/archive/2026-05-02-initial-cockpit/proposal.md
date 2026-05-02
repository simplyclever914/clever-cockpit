## Why

Useful ideas, approvals, and follow-up tasks are currently scattered across chat and ad hoc notes. Clever Cockpit should become the lightweight place where ideas are captured, decided, converted into projects/tasks, and not forgotten.

## What Changes

- Add an Ideas-first cockpit UI based on the BentoBoard visual style.
- Place Approvals at the top of navigation and highlight them when pending.
- Add explicit OK/Deny controls for approval decisions.
- Add Projects and Tasks as primary sections so approved ideas have an obvious destination.
- Keep Runs, Health, and Artifacts as secondary supporting views.
- Keep the first MVP static and local-state only; no backend or OpenClaw runtime integration yet.

## Capabilities

### New Capabilities

- `cockpit-mvp`: Captures the initial user-facing Clever Cockpit behavior for approvals, ideas, projects, tasks, and secondary operational views.

### Modified Capabilities

None. This is the first vanilla OpenSpec change in the repository.

## Impact

- `app/index.html`: static prototype UI and local interaction model.
- `openspec/`: vanilla OpenSpec config, change artifacts, and delta specs.
- `scripts/validate.py`: repository validation should use vanilla OpenSpec validation plus static HTML checks.
- GitHub Actions: validation should run OpenSpec and static checks.
