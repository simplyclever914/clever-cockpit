# Cron finalization hardening for silent jobs

Silent/local OpenClaw cron jobs should be deterministic on success and actionable on failure:

- success path uses the local script/deterministic sender as the source of truth;
- cron final delivery is disabled (`delivery.mode = none`);
- the agent final response is exactly `NO_REPLY` for quiet success;
- real failures remain visible through `failureAlert` or an explicit wake/internal queue item;
- dirty/tooling signals that are not user-facing emergencies route to Clever via wake/internal queue, not direct Telegram delivery.

`scripts/audit_cron_finalization.py` checks the current `~/.openclaw/cron/jobs.json` for these invariants. It intentionally does not mutate cron config; it is a safe local gate for review/CI/manual runs.

Run:

```bash
python3 scripts/audit_cron_finalization.py
python3 scripts/audit_cron_finalization.py --json
```

Current evidence from 2026-05-04: the audit checked enabled cron jobs and silent/local jobs without finding a finalization/delivery mismatch.
