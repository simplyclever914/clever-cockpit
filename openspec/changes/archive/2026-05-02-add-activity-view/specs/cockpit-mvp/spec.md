## ADDED Requirements

### Requirement: Activity log view

The cockpit SHALL expose Activity as a first-class view so the workflow feedback loop has a visible UI destination.

#### Scenario: User opens Activity

- **GIVEN** workflow explains that work results become activity
- **WHEN** the user opens Activity
- **THEN** the cockpit SHALL show chronological activity entries and a detail panel
- **AND** Inbox SHALL remain a separate attention/triage concept
