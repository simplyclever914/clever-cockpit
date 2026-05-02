## ADDED Requirements

### Requirement: Schedules view

The cockpit SHALL provide a Schedules section that lists configured cron activities with last run, next run, and last run success/failure status.

#### Scenario: User reviews cron activities

- **WHEN** the user opens Schedules
- **THEN** each configured cron activity SHALL show its name, schedule, enabled state, last run time, next run time, and last run status
