# OpenSpec / SDD notes

Studied source: `openspec-crossrepo-sdd`.

## Ideology used here

- Specs are the source of truth for *what and why*; code is the implementation of an accepted slice.
- Keep the repo-level flow lightweight: proposal, design, specs, tasks, validation.
- Record tradeoffs and non-goals explicitly so future agents do not re-litigate decisions.
- Acceptance criteria must be testable and tied to user-visible behavior.
- Human approval is required for scope, risky actions, and rollout decisions.

## Why not product-crossrepo here?

Clever Cockpit is currently one implementation repository and one product surface. A heavy cross-repo product schema would add ceremony without value. If this later splits into OpenClaw plugin + backend + web UI, create a central product change and repo slices.
