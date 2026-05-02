## Context

Вадиму понравился BentoBoard-style UX, но исходный BentoBoard слишком ранний и заточен под другого пользователя. Для Clever важнее не операционный dashboard, а память идей, проектов и задач: хорошие мысли из Telegram-чата должны превращаться в решения и действия.

Current repository state:
- static prototype exists in `app/index.html`;
- no runtime/backend integration exists yet;
- SourceCraft can publish static previews;
- OpenClaw already handles real approvals, cron jobs, sessions, and messaging elsewhere.

## Goals / Non-Goals

**Goals:**
- Preserve the BentoBoard feel: glass UI, sidebar, cards, lanes, calm cockpit experience.
- Make Approvals visually impossible to miss when pending.
- Make Ideas the default workspace.
- Show how approved ideas become Projects and Tasks.
- Keep MVP dependency-free and easy to publish statically.

**Non-Goals:**
- Implement production persistence.
- Add Supabase, Next.js, or authentication.
- Integrate with OpenClaw runtime APIs in this first change.
- Recreate the removed Architecture page.

## Decisions

1. **Use vanilla OpenSpec `spec-driven` schema.**
   - Rationale: user explicitly requested Fission-AI/OpenSpec, not local cross-repo SDD.
   - Alternative considered: local `repo-implementation-slice`; rejected because it is not the requested upstream workflow.

2. **Keep MVP as static HTML.**
   - Rationale: validates product/UX before backend choice.
   - Alternative: Next.js/Supabase fork of BentoBoard; rejected as too much surface area and security work for MVP.

3. **Use Ideas as the default active view.**
   - Rationale: the product goal is to prevent ideas/tasks from disappearing in chat.
   - Alternative: Inbox/ops-first dashboard; rejected after user feedback.

4. **Keep operational sections secondary.**
   - Rationale: Runs/Health/Artifacts are useful, but they should not dominate the product.

## Risks / Trade-offs

- Static local state can make interactions feel real while hiding persistence complexity → Mitigation: next change should define the data model and OpenClaw integration contracts before adding a backend.
- Too many sections can dilute the idea/project/task focus → Mitigation: keep Approvals, Ideas, Projects, and Tasks first; leave Ops secondary.
- OK/Deny without backend is only a prototype interaction → Mitigation: label this as MVP and validate future API contracts separately.

## Migration Plan

No production migration. This change updates the prototype and OpenSpec structure only.

Rollback:
- revert the commit or restore previous `app/index.html` from git.

## Open Questions

- Should persistent storage be SQLite/local files inside OpenClaw workspace, or a small web backend?
- What should the first real capture command look like: `/idea`, message reaction, or automatic extraction from chat?
- Should approved ideas create tasks immediately or require a second confirmation?
