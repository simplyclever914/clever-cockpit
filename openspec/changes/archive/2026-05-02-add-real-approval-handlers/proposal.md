# add-real-approval-handlers

## Why

The approval runner can consume accepted approvals, but it only records policy approvals. To make Cockpit useful as a real human-in-the-loop console, approvals need typed payloads and explicit safe handlers for approved actions.

## What changes

- Add handler and JSON payload fields to approvals.
- Add an API endpoint for creating pending approvals from Clever/workflows.
- Add allowlisted runner handlers for SourceCraft publishing and Telegram send-and-pin digest delivery.
- Keep unknown or malformed approvals safe by marking them `needs_handler` or `failed`.

## Impact

- Extends SQLite approval schema.
- Adds `/api/approvals` creation endpoint.
- Extends `scripts/approval_runner.py` with real local handlers.
