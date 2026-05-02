# Local Proposal: Initial Clever Cockpit / clever-cockpit

## Parent product change

N/A for MVP. This is the first repository and product slice for Clever Cockpit. If the work later touches OpenClaw core/runtime, create a parent product change and link it here.

## Implements requirements

- Capture ideas from chat so they do not disappear.
- Promote approved ideas into projects and concrete tasks.
- Surface pending approvals at the top and highlight them when non-empty.
- Provide a BentoBoard-like cockpit UX without depending on Supabase/Next for the first MVP.

## Local scope

- Static clickable prototype in `app/index.html`.
- LocalStorage-backed state for ideas, projects, tasks, approvals, and activity.
- OpenSpec docs and validation scripts.
- No external service writes from the app.

## Out of scope

- Real OpenClaw API integration.
- Authentication/multi-user permissions.
- Supabase or persistent server database.
- Telegram command integration.
- Production deployment hardening.

## Dependencies

- Browser with LocalStorage.
- Python 3 for local static serving and validation.
