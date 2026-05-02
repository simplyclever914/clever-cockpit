# Local Validation: Initial Clever Cockpit / clever-cockpit

## Unit tests

No JS unit test framework in MVP. Use static assertions in `scripts/validate.py`.

## Integration tests

- Serve `app/index.html` via `python3 -m http.server`.
- Open in browser and verify navigation and action controls.
- Optional: publish static artifact and verify HTTP 200.

## Manual checks

- Approvals is the first navigation item.
- Pending approvals are highlighted.
- Approval cards have OK and Deny buttons.
- Ideas have examples and lifecycle actions.
- Projects and Tasks are primary sections.
- Architecture section is absent.

## Evidence

Run:

```bash
python3 scripts/validate.py
```

## Archive readiness

Archive when:

- MVP prototype is reviewed by Вадим;
- the next implementation slice is created for persistent data / OpenClaw integration;
- validation passes.
