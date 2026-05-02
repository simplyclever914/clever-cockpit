# Local Specification: Clever Cockpit MVP

## Parent requirement

N/A. Initial local product slice.

## Requirement: approvals-first-navigation

This repository SHALL display approvals as the first navigation item and visually highlight non-empty pending approvals.

### Scenario: pending approvals exist

GIVEN there is at least one pending approval
WHEN the cockpit loads
THEN Approvals appears at the top of navigation
AND a hot badge shows the pending count
AND the main Ideas view shows a visible approvals alert with a Review action.

## Requirement: explicit-approval-actions

This repository SHALL provide explicit OK and Deny controls on approval cards.

### Scenario: user decides approval

GIVEN an approval card is visible
WHEN the user chooses OK or Deny
THEN the approval is removed from the pending queue
AND an activity entry records the decision.

## Requirement: idea-lifecycle

This repository SHALL make the next step for each idea explicit.

### Scenario: idea is approved

GIVEN an idea is in Inbox or Needs Decision
WHEN the user approves it
THEN the idea moves to Converted
AND a project or task follow-up is created or suggested.

### Scenario: idea is denied

GIVEN an idea is in Inbox or Needs Decision
WHEN the user denies it
THEN the idea moves to Done / Parked
AND the UI records that it was parked or rejected.

## Requirement: projects-and-tasks-focus

This repository SHALL prioritize Ideas, Projects, and Tasks over operational monitoring.

### Scenario: user opens cockpit

GIVEN the cockpit loads
WHEN the user sees the default screen
THEN Ideas is the active view
AND Projects and Tasks are primary navigation items
AND Runs/Health are secondary system sections.
