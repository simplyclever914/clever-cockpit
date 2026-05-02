# Clever Cockpit

BentoBoard-inspired local cockpit for OpenClaw/Clever focused on **ideas, projects, tasks, and approvals** so useful thoughts do not disappear in chat.

This repository is intentionally SDD-first using vanilla Fission-AI/OpenSpec: product/UX decisions live in OpenSpec artifacts before implementation details grow.

## Current MVP

- Static dependency-free cockpit UI in `app/index.html`.
- SQLite-backed local service in `server/cockpit_server.py` with LocalStorage fallback for static previews.
- Interactions:
  - approvals can be `OK`/`Deny`/`Details`;
  - ideas can be approved, denied/parked, or converted into tasks;
  - approved ideas become project/task material rather than dead chat notes.
- Approval runner:
  - `scripts/approval_runner.py` polls accepted approvals;
  - approvals are claimed at most once and marked `done`, `failed`, or `needs_handler`;
  - only allowlisted handlers run (`record_only`, `sourcecraft_publish`, `telegram_send_and_pin_digest`).
- Vanilla OpenSpec `spec-driven` specs are archived into `openspec/specs/` with completed changes under `openspec/changes/archive/`.


## Run as local/LAN app

Localhost (API token not required):

```bash
python3 server/cockpit_server.py --host 127.0.0.1 --port 8765
# open http://127.0.0.1:8765/
```

LAN mode (token required by default):

```bash
python3 server/cockpit_server.py --host 0.0.0.0 --port 8765
# the server prints: http://<host>:8765/?token=<token>
```

State is stored in `data/cockpit.sqlite`. The LAN token is stored in `data/token` with local-only permissions when possible. Do not expose this service to the public internet.

Approval semantics are intentionally status-only: OK/Deny updates Cockpit state. OpenClaw/Clever must check that status before continuing any external action.

Run the approval runner alongside the server:

```bash
python3 scripts/approval_runner.py --base-url http://127.0.0.1:8765 --interval 10
```

Create a typed approval from a workflow:

```bash
scripts/create-cockpit-approval.py \
  --title "Send digest" \
  --handler telegram_send_and_pin_digest \
  --job-key ai_wrapup \
  --text-file /tmp/digest.txt
```

Important: schedules execute their normal work directly by default. Use typed approvals only for explicit gates or separate idea decisions.

Task hygiene rule: every task must be concrete before it is created or run. Write a clear description with outcome, scope, done criteria, and any blocker/trigger. Avoid umbrella titles like “Continue MVP”; split them into executable next actions. In the UI, task descriptions are intentionally hidden under a spoiler (`<details>`) so lists stay scannable without losing definition.

Schedules that discover follow-up ideas can record them without blocking delivery:

```bash
scripts/create-cockpit-idea.py \
  --title "Evaluate new source" \
  --body "Found during Telegram Review" \
  --source schedule \
  --approval
```


## Validate

```bash
python3 scripts/validate.py
```

## SDD / OpenSpec stance

We use Fission-AI/OpenSpec default `spec-driven` flow:

```text
proposal → specs → design → tasks → apply → sync/archive
```

OpenSpec is intentionally fluid: artifacts can be updated as we learn. Human decisions own scope and tradeoffs; agents draft, critique, implement, and gather evidence.
