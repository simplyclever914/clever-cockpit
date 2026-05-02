## ADDED Requirements

### Requirement: Scheduled jobs execute by default

Scheduled jobs SHALL execute their intended publish, send, sync, or review work without Cockpit approval unless the user explicitly configured that schedule/action as approval-gated.

#### Scenario: Schedule discovers a new idea

- **GIVEN** a scheduled job finds a new potential idea or project while doing its normal work
- **WHEN** the idea is not part of the schedule's direct deliverable
- **THEN** the job MAY create a Cockpit Idea
- **AND** MAY create a separate approval request if human decision is needed
- **BUT** the scheduled deliverable SHALL NOT be blocked by that idea approval
