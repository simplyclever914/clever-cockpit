## ADDED Requirements

### Requirement: Idea review approvals update idea lifecycle

The runner SHALL update the linked idea status when an accepted idea review approval is processed.

#### Scenario: Idea review approval is accepted

- **GIVEN** an idea review approval payload contains `idea_id`
- **WHEN** the user accepts the approval and the runner processes it
- **THEN** the linked idea SHALL move out of the initial captured/proposed lane
- **AND** the activity log SHALL record the lifecycle update
