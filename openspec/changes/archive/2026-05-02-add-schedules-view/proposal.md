# add-schedules-view

## Why

Inbox duplicates Activity/Approvals and confuses the cockpit model. Scheduled cron jobs need a dedicated operational view that shows what exists, when each job last ran, whether it succeeded, and when it will run next.

## What changes

- Remove Inbox from navigation and UI.
- Add a Schedules section backed by `/api/state`.
- Server reads OpenClaw cron `jobs.json` and `jobs-state.json` and returns job name, schedule, enabled state, last run, next run, and last status.

## Impact

Clarifies cockpit navigation and exposes live schedule status without approvals.
