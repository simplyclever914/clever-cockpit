## Why

The current cockpit looks right but most controls are mock interactions. Development should start by making the prototype behavior real locally, so approving requests and triaging ideas visibly changes state and proves the product loop.

## What Changes

- Add LocalStorage-backed state for approvals, ideas, projects, tasks, and activity.
- Make approval OK/Deny buttons remove pending approvals and update counts/highlights.
- Make idea OK/Deny/Make Task buttons move ideas through lifecycle lanes.
- Create project/task follow-ups when ideas are converted.
- Add a lightweight reset/demo-data path for repeatable prototype testing.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cockpit-mvp`: Existing static prototype requirements become interactive local-state behavior.

## Impact

- `app/index.html`: replace mock rendering with stateful rendering and action handlers.
- `scripts/validate.py`: add static checks for LocalStorage/action markers.
- No backend, dependencies, or external writes.
