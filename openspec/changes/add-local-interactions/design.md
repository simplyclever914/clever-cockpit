## Context

`initial-cockpit` established the vanilla OpenSpec structure and static UX. The next useful development step is to make the single-file prototype behave like a tiny product without adding backend complexity.

## Goals / Non-Goals

**Goals:**
- Keep dependency-free static HTML.
- Persist demo state in LocalStorage.
- Make approval and idea lifecycle buttons visibly change state.
- Keep the app resettable for demos/review.

**Non-Goals:**
- No OpenClaw runtime API integration.
- No authentication or multi-device sync.
- No framework migration.

## Decisions

1. **Use LocalStorage with a versioned key.**
   - Rationale: enough durability for browser prototype review.
   - Alternative: JSON file or SQLite; postponed until OpenClaw integration design.

2. **Use event delegation and data attributes.**
   - Rationale: simple and robust for a single-file app with re-rendered lists.

3. **Generate project/task follow-ups automatically on idea conversion.**
   - Rationale: validates the core promise that ideas become actions, not just labels.

## Risks / Trade-offs

- LocalStorage can diverge from shipped demo defaults → Mitigation: add Reset demo data button.
- Single-file JS will become hard to maintain → Mitigation: acceptable for MVP; next slice can split modules if needed.
- Automatic project creation may be too aggressive → Mitigation: prototype makes this visible for feedback before real backend.

## Migration Plan

No migration. Existing users can reset demo data if old LocalStorage shape is incompatible.

## Open Questions

- Should approved ideas create both a project and task, or just a task under an existing project by default?
- What exact data should `/idea` capture from Telegram: message link, quote, sender, tags, suggested project?
