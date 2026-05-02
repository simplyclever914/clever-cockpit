# Clever Cockpit

BentoBoard-inspired local cockpit for OpenClaw/Clever focused on **ideas, projects, tasks, and approvals** so useful thoughts do not disappear in chat.

This repository is intentionally SDD-first using vanilla Fission-AI/OpenSpec: product/UX decisions live in OpenSpec artifacts before implementation details grow.

## Current MVP

- Static dependency-free prototype in `app/index.html`.
- LocalStorage-backed interactions:
  - approvals can be `OK`/`Deny`/`Details`;
  - ideas can be approved, denied/parked, or converted into tasks;
  - approved ideas become project/task material rather than dead chat notes.
- Vanilla OpenSpec `spec-driven` change in `openspec/changes/initial-cockpit/`.

## Run locally

```bash
python3 -m http.server 8765 --directory app
# open http://127.0.0.1:8765/
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
