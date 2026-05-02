# cockpit-mvp Specification

## Purpose
TBD - created by archiving change initial-cockpit. Update Purpose after archive.
## Requirements
### Requirement: Approvals-first attention

The cockpit SHALL display approvals as the first navigation item and visually highlight pending approvals whenever one or more approval decisions are waiting, and SHALL update that highlight as local approval state changes.

#### Scenario: Pending approvals are visible on load

- **WHEN** the cockpit loads with pending approvals
- **THEN** Approvals appears before Ideas, Projects, and Tasks in the navigation
- **AND** the approvals count is shown with a high-visibility badge
- **AND** the main Ideas view shows an approvals alert with a Review action

#### Scenario: No pending approvals

- **WHEN** there are no pending approvals
- **THEN** the cockpit does not show an urgent approvals alert
- **AND** Ideas remains the default primary workspace

#### Scenario: Approval count changes after decision

- **WHEN** the user accepts or denies an approval
- **THEN** the pending approval count updates without reloading the page
- **AND** the urgent highlight disappears when the count reaches zero

### Requirement: Explicit approval decisions

The cockpit SHALL provide explicit OK and Deny actions on approval cards so pending decisions do not remain ambiguous, and SHALL persist local decisions in browser storage.

#### Scenario: Approving a request

- **WHEN** the user selects OK on an approval card
- **THEN** the approval is treated as accepted
- **AND** the pending approval count decreases
- **AND** the decision is reflected in activity or item state

#### Scenario: Denying a request

- **WHEN** the user selects Deny on an approval card
- **THEN** the approval is treated as rejected
- **AND** the pending approval count decreases
- **AND** the decision is reflected in activity or item state

#### Scenario: Decision survives refresh

- **WHEN** the user makes an approval decision and reloads the page
- **THEN** the approval remains removed from the pending queue
- **AND** the updated pending count is preserved

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

### Requirement: Workflow map

The cockpit SHALL provide a dedicated Workflow view that explains how Ideas, Projects, Tasks, Approvals, Schedules, and Activity relate.

#### Scenario: User opens Workflow

- **GIVEN** the user does not understand the Ideas → Projects → Tasks relationship
- **WHEN** they open the Workflow view
- **THEN** the cockpit SHALL show a lifecycle map from idea capture through decision, draft project, task execution, scheduled work, and feedback
- **AND** the map SHALL state that approved ideas create draft projects/tasks, not automatically active projects
- **AND** the map SHALL state that schedules execute directly by default and create approvals only for separate decisions or explicitly gated actions

### Requirement: Activity log view

The cockpit SHALL expose Activity as a first-class view so the workflow feedback loop has a visible UI destination.

#### Scenario: User opens Activity

- **GIVEN** workflow explains that work results become activity
- **WHEN** the user opens Activity
- **THEN** the cockpit SHALL show chronological activity entries and a detail panel
- **AND** Inbox SHALL remain a separate attention/triage concept

### Requirement: Theme persistence

The cockpit SHALL preserve the selected theme across page reloads, including when API-backed state is loaded.

#### Scenario: Light theme persists after reload

- **GIVEN** the user selects the light theme
- **WHEN** the page reloads and fetches API state
- **THEN** the document theme SHALL remain light

