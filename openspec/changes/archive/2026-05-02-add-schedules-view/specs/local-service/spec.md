## ADDED Requirements

### Requirement: Cron schedule state API

The local service SHALL include schedule state in `/api/state` by reading OpenClaw cron job definitions and scheduler state.

#### Scenario: Cron files exist

- **GIVEN** OpenClaw cron `jobs.json` and `jobs-state.json` exist
- **WHEN** `/api/state` is requested
- **THEN** the response SHALL include a `schedules` array with job identity, schedule description, enabled flag, last run time, next run time, and last status
