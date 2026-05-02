## ADDED Requirements

### Requirement: Approval runner consumption

The local service SHALL expose accepted approvals to an automation runner with at-most-once claim semantics.

#### Scenario: Runner claims accepted approvals

- **GIVEN** an approval with status `accepted` and no run status
- **WHEN** the runner requests ready approvals
- **THEN** the service SHALL mark the approval as `running`
- **AND** the same approval SHALL NOT be returned again while it is running

#### Scenario: Runner completes approval

- **GIVEN** a claimed approval
- **WHEN** the runner reports completion
- **THEN** the service SHALL persist the completion status and activity entry

#### Scenario: Unknown approved action

- **GIVEN** an approval that has no local handler
- **WHEN** the runner processes it
- **THEN** the approval SHALL be marked `needs_handler`
- **AND** the activity log SHALL explain that Clever must handle it deliberately
