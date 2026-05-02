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

### Requirement: Digest approval workflows

Digest workflows SHALL create typed Cockpit approvals for external publish/send actions instead of directly publishing or sending after generation.

#### Scenario: AI wrap-up waits for approval

- **GIVEN** an AI wrap-up artifact and Telegram summary have been generated and locally verified
- **WHEN** the cron job creates a `digest_publish_and_send` approval
- **THEN** no SourceCraft publish or Telegram send SHALL happen until the approval is accepted
- **AND** the runner SHALL publish and send/pin only after claiming the accepted approval

#### Scenario: Text-only daily digest waits for approval

- **GIVEN** a reflection or Telegram review message has been generated
- **WHEN** the cron job creates a `telegram_send_and_pin_digest` approval
- **THEN** Telegram delivery SHALL happen only after the approval is accepted

### Requirement: Scheduled jobs execute by default

Scheduled jobs SHALL execute their intended publish, send, sync, or review work without Cockpit approval unless the user explicitly configured that schedule/action as approval-gated.

#### Scenario: Schedule discovers a new idea

- **GIVEN** a scheduled job finds a new potential idea or project while doing its normal work
- **WHEN** the idea is not part of the schedule's direct deliverable
- **THEN** the job MAY create a Cockpit Idea
- **AND** MAY create a separate approval request if human decision is needed
- **BUT** the scheduled deliverable SHALL NOT be blocked by that idea approval

