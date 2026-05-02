## MODIFIED Requirements

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

The cockpit SHALL show ideas in lifecycle states that make the next step explicit, and SHALL allow local actions to move ideas between those states.

#### Scenario: Captured idea needs decision

- **WHEN** an idea is captured from chat or created manually
- **THEN** it appears in an Inbox or Needs Decision lane
- **AND** the user can choose OK, Deny, or Make Task

#### Scenario: Approved idea is converted

- **WHEN** the user approves an idea
- **THEN** the idea moves to a Converted state
- **AND** the cockpit creates or suggests a related project or task follow-up

#### Scenario: Rejected idea is parked

- **WHEN** the user denies an idea
- **THEN** the idea moves to Done or Parked
- **AND** the UI records that it was closed rather than losing it in chat history

#### Scenario: Make task from idea

- **WHEN** the user selects Make Task on an idea
- **THEN** a task is created from the idea
- **AND** the idea moves to Converted
- **AND** the task appears in the Tasks section

### Requirement: Projects and tasks are primary work surfaces

The cockpit SHALL prioritize Ideas, Projects, and Tasks over operational monitoring, and SHALL update project/task lists when ideas are converted locally.

#### Scenario: Default workspace focus

- **WHEN** the cockpit opens
- **THEN** Ideas is the active default view
- **AND** Projects and Tasks are primary navigation items
- **AND** Runs and Health are secondary system sections

#### Scenario: Approved idea becomes actionable

- **WHEN** an idea is converted
- **THEN** the user can see which project or task will carry it forward
- **AND** the idea is not only marked liked or approved without a next action
