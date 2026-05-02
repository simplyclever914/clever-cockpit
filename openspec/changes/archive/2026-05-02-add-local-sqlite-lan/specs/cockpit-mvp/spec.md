## MODIFIED Requirements

### Requirement: Ideas have a visible lifecycle

The cockpit SHALL show ideas in lifecycle states that make the next step explicit, SHALL allow local actions to move ideas between those states, and SHALL persist those transitions through the local service when available.

#### Scenario: Captured idea needs decision

- **WHEN** an idea is captured from chat, command, UI, or Clever-created note
- **THEN** it appears in an Inbox or Needs Decision lane
- **AND** the user can choose OK, Deny, or Make Task

#### Scenario: Approved idea is converted

- **WHEN** the user approves an idea
- **THEN** the idea moves to a Converted state
- **AND** the cockpit creates or suggests a draft project and first task follow-up
- **AND** the project is not treated as an active project until confirmed

### Requirement: Projects and tasks are primary work surfaces

The cockpit SHALL prioritize Ideas, Projects, and Tasks over operational monitoring, SHALL update project/task lists when ideas are converted locally, and SHALL distinguish draft projects from active projects.

#### Scenario: Approved idea creates draft project

- **WHEN** an idea is converted
- **THEN** the user can see a draft project or task that will carry it forward
- **AND** the draft project requires confirmation before becoming active
