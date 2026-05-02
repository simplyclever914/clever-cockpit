# OpenSpec notes

This repository uses vanilla [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), not the local cross-repo SDD derivative.

## Philosophy applied

- Fluid, not rigid: artifacts can be updated as we learn.
- Iterative, not waterfall: implementation can refine proposal/specs/design.
- Easy, not complex: use the default `spec-driven` schema.
- Brownfield-friendly: future changes should be deltas against `openspec/specs/`.

## Workflow

Default quick path:

```text
/opsx:propose → /opsx:apply → /opsx:sync → /opsx:archive
```

Current active change:

```text
openspec/changes/initial-cockpit/
  proposal.md
  specs/cockpit-mvp/spec.md
  design.md
  tasks.md
```

Specs describe observable behavior. Design explains technical choices. Tasks are the implementation checklist.
