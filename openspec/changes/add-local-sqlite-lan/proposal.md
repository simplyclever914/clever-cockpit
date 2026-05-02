## Why

Clever Cockpit needs to move from a browser-only demo to a real local system. Вадим confirmed the UI should be local but accessible on LAN immediately, with SQLite persistence from the start, and idea capture should work both by explicit command-style input and by Clever creating ideas when the user says something is interesting or worth recording.

## What Changes

- Add a local Python HTTP service that serves the UI and JSON API.
- Bind to LAN-capable host/port when requested, with token protection by default.
- Add SQLite persistence for approvals, ideas, projects, tasks, and activity.
- Add API endpoints for listing state and mutating approvals/ideas/tasks.
- Keep approval actions status-only for MVP; Clever/OpenClaw will check status rather than the UI directly continuing actions.
- Add idea capture paths for manual UI entry and future Telegram/OpenClaw commands such as `/idea` or “this is interesting / I have an idea, write it down”.

## Capabilities

### New Capabilities

- `local-service`: Local LAN-capable HTTP service and SQLite persistence for Cockpit state.

### Modified Capabilities

- `cockpit-mvp`: UI state should be loaded from/persisted to the local service when available, while retaining demo fallback behavior.

## Impact

- `server/`: new Python standard-library server and SQLite store.
- `app/index.html`: API-backed state loading and mutations.
- `scripts/validate.py`: validate server syntax and API markers.
- `README.md`: local/LAN run instructions and token guidance.
