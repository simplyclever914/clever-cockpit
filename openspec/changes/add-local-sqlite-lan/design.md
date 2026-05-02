## Context

Вадим confirmed key product decisions:

1. UI should be local, but LAN access is needed immediately.
2. SQLite should be used from the start.
3. Ideas should be capturable through natural language to Clever (“это интересно”, “у меня идея, запиши”), a `/idea` command, and Clever-initiated entries.
4. Approval buttons only update Cockpit status; Clever checks status before continuing work.
5. Approved ideas should become draft projects + first tasks, not active projects without confirmation.

## Goals / Non-Goals

**Goals:**
- Python standard-library local server.
- SQLite database in local workspace/repo data directory.
- Token-protected API for LAN mode.
- JSON API for state, approvals, ideas, projects, tasks.
- UI uses API when served by the local service, with LocalStorage demo fallback for static preview.

**Non-Goals:**
- Full OpenClaw runtime integration in this slice.
- Multi-user auth, OAuth, or internet exposure.
- Supabase/Next.js migration.

## Decisions

1. **Python standard library over Node/Next.**
   - Rationale: no dependency install, easy sqlite3, predictable local service.
   - Alternative: Node/Express; rejected for MVP dependency overhead.

2. **Token required for LAN API.**
   - Rationale: LAN still exposes private data; token is minimal necessary protection.
   - Alternative: open LAN server; rejected as unsafe.

3. **SQLite schema with generic item tables.**
   - Rationale: keeps persistence simple while matching the product model.

4. **Status-only approval semantics.**
   - Rationale: avoids UI accidentally executing external/destructive actions. Clever remains responsible for checking approval status and continuing.

## Risks / Trade-offs

- Token in URL/localStorage can leak on shared devices → keep LAN private and document it; later add session auth if needed.
- Python stdlib server is not a hardened production web server → LAN/local only, not internet-facing.
- API and UI in one HTML file can get messy → acceptable until core workflow is proven.

## Migration Plan

- New installs create `data/cockpit.sqlite` automatically.
- Existing static preview continues working via fallback seed data.

## Open Questions

- Exact Telegram command syntax and routing will be defined in a later OpenClaw integration slice.
- Whether Clever should write directly to SQLite or call the HTTP API locally.
