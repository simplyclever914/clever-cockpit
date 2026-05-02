# fix-idea-review-approval

## Why

Idea review approvals can complete without changing the linked idea status. This leaves the idea in Inbox/captured with OK/Deny buttons even after the approval has been accepted and processed.

## What changes

- Add an explicit `idea_review` approval handler.
- When accepted, the handler updates the linked idea to `review` by default or to a payload-provided target status.
- Update the idea capture helper to use `idea_review` instead of `record_only`.

## Impact

Accepted idea review approvals now visibly move the idea lifecycle forward.
