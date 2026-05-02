## MODIFIED Requirements

### Requirement: Workflow map

The cockpit SHALL provide a dedicated Workflow view that explains how Ideas, Projects, Tasks, Approvals, Schedules, and Activity relate.

#### Scenario: User opens Workflow

- **GIVEN** the user does not understand the Ideas → Projects → Tasks relationship
- **WHEN** they open the Workflow view
- **THEN** the cockpit SHALL show a lifecycle map from idea capture through decision, draft project, task execution, scheduled work, and feedback
- **AND** the map SHALL state that approved ideas create draft projects/tasks, not automatically active projects
- **AND** the map SHALL state that schedules execute directly by default and create approvals only for separate decisions or explicitly gated actions
