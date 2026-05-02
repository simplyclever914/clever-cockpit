# fix-schedule-approval-semantics

## Why

Schedules should perform their scheduled work without approval unless the user explicitly marks a run/action as approval-gated. The previous digest approval routing over-applied approval gates and delayed normal scheduled delivery.

## What changes

- Clarify that scheduled jobs execute directly by default.
- Keep approvals for explicit gates and new idea decisions.
- Add a helper for schedules to capture ideas into Cockpit and optionally create review approval requests.

## Impact

Restores expected schedule behavior while preserving Cockpit as a decision surface for new ideas.
