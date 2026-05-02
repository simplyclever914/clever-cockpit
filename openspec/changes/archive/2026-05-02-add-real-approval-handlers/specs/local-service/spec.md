## ADDED Requirements

### Requirement: Typed executable approvals

The local service SHALL allow Clever/workflows to create pending approvals with an allowlisted handler name and JSON payload, and the runner SHALL execute only registered local handlers after human acceptance.

#### Scenario: Workflow creates typed approval

- **GIVEN** Clever has a prepared external action that needs human approval
- **WHEN** it creates an approval with `handler` and `payload_json`
- **THEN** Cockpit SHALL persist the approval as `pending`
- **AND** the approval SHALL be visible in the pending queue

#### Scenario: Accepted typed approval runs

- **GIVEN** a pending approval with a registered handler
- **WHEN** the user selects OK and the runner claims it
- **THEN** the runner SHALL validate the payload
- **AND** execute the registered local handler
- **AND** persist `done` or `failed` with a human-readable message

#### Scenario: Unregistered handler is safe

- **GIVEN** an accepted approval with an unregistered handler
- **WHEN** the runner processes it
- **THEN** no command SHALL be executed
- **AND** the approval SHALL be marked `needs_handler`
