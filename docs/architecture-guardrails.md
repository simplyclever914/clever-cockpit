# Lightweight architecture guardrails for AI-generated code

Use these guardrails when a PR may create architecture drift: a locally working AI-generated change that quietly changes system structure, contracts, or ownership without a durable decision record.

The goal is not bureaucracy. The goal is to keep architecture decisions searchable and reviewable after the chat context is gone.

## When an ADR / decision note is required

Create a short ADR from `docs/adr/0000-template.md`, or link an equivalent decision note, when a change does any of the following:

- changes module boundaries, ownership, or responsibility splits;
- changes public API contracts, data schema, persistence model, or compatibility expectations;
- introduces a new infrastructure/deployment/security pattern;
- creates a new abstraction layer or bypasses an existing one;
- performs a large AI-generated refactor across multiple subsystems;
- changes an invariant future agents/reviewers must know.

## When an ADR is not required

Do not require an ADR for:

- bug fixes with no contract or architectural boundary change;
- small UI/UX changes;
- local refactors that preserve public behavior;
- tests, docs, comments, formatting, or dependency bumps without architecture impact;
- experiments/spikes that are clearly not on the production path.

## Review rule

If a PR touches architecture-sensitive areas, the author should either:

1. link an ADR / decision note; or
2. explicitly state why the change is local, reversible, and not architectural.

For AI-generated significant changes, prompts and agent transcripts are supporting context only. The durable source of truth must be the ADR, issue, or PR explanation.

## Later automation

Do not add CI/lint enforcement yet. Revisit after 2–3 real examples. If reviewers keep missing the checklist, add warning-only automation first.
