# Design

## Approach

Use polling first, not event notification first. Polling is less elegant, but it is durable: if the browser, server, or agent restarts, accepted approvals remain in SQLite until a runner claims them.

## State machine

Approvals move through:

```text
pending → accepted/denied
accepted → running → done/failed
```

The runner claims accepted approvals by setting `run_status='running'` and `claimed_at`. Completion sets `run_status` to `done`, `failed`, or `needs_handler`.

## Safety

The API never accepts arbitrary shell commands from the browser. The runner dispatches local code based on approval IDs/kinds. Unknown approvals are marked `needs_handler`, surfaced in activity, and left for Clever to handle deliberately.

## Later event option

A later change can add SSE/webhook/OpenClaw wake events on approval changes. The polling runner should remain as the fallback recovery path.
