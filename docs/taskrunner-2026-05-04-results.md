# TaskRunner results — 2026-05-04 01:30 UTC

## OpenClaw Telegram/mobile UX affordances

1. **Pinned session card** — one durable Telegram message per active agent/session with model, cwd/repo, state, last activity, and next action. Priority: high.
2. **Live log tail on demand** — `logs` / button shows last 30–80 lines with a clear “open full thread/resume” action instead of dumping everything into chat.
3. **Approval inbox with exact command preview** — approvals grouped in one place, with the exact shell/external action and one-tap accept/deny when supported.
4. **Resume/reconnect affordance** — mobile-friendly “continue this run” and “attach to existing session” controls, not just new-chat continuation.
5. **Pinning and quiet modes** — important runs/results can be pinned; noisy background progress stays silent unless blocked/done/decision-needed.
6. **Mobile command palette** — compact buttons/selects for status, stop, steer, artifacts, recent sessions, approvals; avoid remembering slash syntax.
7. **Artifact/result card** — after work completes, show concise evidence + links/files/tests, with “confirm done / return to work” actions.

Recommended first priorities: pinned session card + approval inbox, because they reduce mobile uncertainty and prevent missed decisions.

## AI Architecture Drift Guardrails proposal

Problem: AI-assisted changes can quickly introduce architecture drift when design decisions live only in PR comments, chats, or implicit maintainer memory. The guardrail should be lightweight: it asks for explicit intent on high-impact changes without slowing small fixes.

Minimal ADR template:
- Context: what architecture pressure or repeated decision triggered this?
- Decision: what invariant/pattern/API boundary are we choosing?
- Alternatives considered: 1–3 rejected options and why.
- Scope: where this applies and where it does not.
- Consequences: migration cost, operational risk, future constraints.
- Owner/review date: who can revise it and when to revisit.

PR checklist:
- Does this change introduce or change a subsystem boundary, persistence model, public API, auth/security path, background runner, or cross-cutting dependency?
- If yes: link ADR or write “no ADR because …”.
- Does generated code create a new pattern where an existing project pattern exists?
- Are tests/docs updated for the chosen architecture invariant?
- Is rollback/migration path clear?

Optional automation later: a repo-local script/lint that flags large diffs touching configured paths (`server/`, `db/`, `auth/`, `jobs/`, public API files) and asks for an ADR link or explicit waiver in the PR template.

Risks: over-bureaucracy, stale ADRs, and agents writing boilerplate ADRs without real decisions. Mitigation: small template, path/size trigger only, waivers allowed, review stale ADRs monthly.

Do not apply for tiny bug fixes, copy/wording/UI-only tweaks, test-only changes, experiments behind a throwaway flag, or refactors fully contained in one module with no new invariant.

Decision for Vadim: start with a PR-template checklist only, then add lint after 2–3 real examples prove the trigger rules.

## Knowledge map next actions

### Telegram bookmarks knowledge map for Cockpit
Next executable action: create a read-only prototype that clusters the last 7–14 days of MyBookmarks + selected Telegram index hits into 5–8 topics (`agent runtime`, `browser`, `memory`, `evals`, `UI`, `MCP/tools`, `ops`) and saves one markdown artifact with source links. Done when Vadim can see whether clustering is useful before any UI/database integration.

### Weekly Telegram knowledge map digest
Decision needed before activation: whether to run weekly, and which day/time. Proposed default: Monday 10:30 Europe/Moscow, private/pinned digest only, no SourceCraft publication at first.

## Blockers / not completed

### Telegram `/idea` command
Blocked for safe local execution: this repo exposes `/api/ideas` and `scripts/create-cockpit-idea.py`, but I did not find the Telegram command routing/hook in `clever-cockpit`. Marking done would require evidence from an actual Telegram `/idea` message creating a Cockpit Idea; that external integration point needs to be identified or configured.

### Fetch/SNITCHMD/CloakBrowser benchmark
Blocked on input source and scope: the task asks for up to 20 problematic links from bookmarks/Telegram. I found review docs and past digest references, but not a stable local list of the intended problematic URLs inside this repo. Need either a saved URL list or permission to sample from the Telegram index/bookmarks and run external fetches.
