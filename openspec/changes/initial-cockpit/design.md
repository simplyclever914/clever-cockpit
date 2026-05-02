# Local Design: Initial Clever Cockpit / clever-cockpit

## Approach

Build a dependency-free static app that preserves the BentoBoard feel while proving the information architecture:

1. Approvals first: if approvals exist, they are highlighted above the main work area and first in navigation.
2. Ideas are the main object: captured ideas move through decision states.
3. Approved ideas create downstream project/task records.
4. Operations/health exist, but are secondary to idea/project/task memory.

State is stored in LocalStorage using a versioned key. This keeps MVP setup trivial and avoids premature backend choice.

## Code areas

- `app/index.html` — UI, CSS, sample data, local state, interactions.
- `scripts/validate.py` — static checks for required UX markers and no local/secret leaks.
- `openspec/changes/initial-cockpit/` — SDD artifacts.

## Contract dependencies

None for MVP. Future OpenClaw integration will need explicit contracts for:

- creating an idea from a chat message;
- listing pending approvals;
- converting an idea into a task/project;
- reading cron/subagent/job health.

## Compatibility

- Works as static HTML on SourceCraft/GitHub Pages/local server.
- No build step.
- No external JS/CSS CDN dependency.

## Tests

- OpenSpec required artifact validation.
- Static HTML marker validation.
- Manual browser checks for navigation and action buttons.

## Risks

- Static MVP may hide complexity of real sync/conflict handling.
- LocalStorage is not durable enough for production.
- Too many operational widgets can dilute the main goal; keep ideas/projects/tasks primary.
