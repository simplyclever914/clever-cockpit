# local-service Specification

## Purpose
TBD - created by archiving change add-local-sqlite-lan. Update Purpose after archive.
## Requirements
### Requirement: LAN-capable local service

The system SHALL provide a local HTTP service that can serve the Cockpit UI on localhost or LAN, and SHALL require a token when listening on non-localhost interfaces.

#### Scenario: Localhost development

- **WHEN** the user starts the service with default settings
- **THEN** the UI is available on a local HTTP port
- **AND** the service can read and write local SQLite state

#### Scenario: LAN access

- **WHEN** the user starts the service bound to `0.0.0.0`
- **THEN** other devices on the LAN can open the UI
- **AND** API requests require the configured token

### Requirement: SQLite persistence

The system SHALL persist approvals, ideas, projects, tasks, and activity in SQLite.

#### Scenario: State survives restart

- **WHEN** an approval is decided or an idea is converted
- **AND** the service restarts
- **THEN** the updated state remains visible in the UI

### Requirement: Status-only approvals

The system SHALL record approval decisions as status changes in Cockpit without directly continuing external OpenClaw actions.

#### Scenario: Approval accepted

- **WHEN** the user selects OK for an approval
- **THEN** Cockpit records the approval as accepted
- **AND** OpenClaw/Clever can later check that status before continuing work
- **AND** the UI itself does not execute the external action

### Requirement: Idea capture API

The system SHALL expose an API that lets the UI or Clever create ideas with source and note metadata.

#### Scenario: User tells Clever an idea

- **WHEN** Clever receives a user instruction like “this is interesting” or “I have an idea, write it down”
- **THEN** Clever can create an idea through the Cockpit API or local store
- **AND** the idea appears in the Ideas workflow for later decision

