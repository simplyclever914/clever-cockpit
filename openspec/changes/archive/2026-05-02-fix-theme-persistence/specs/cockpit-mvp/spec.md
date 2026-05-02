## ADDED Requirements

### Requirement: Theme persistence

The cockpit SHALL preserve the selected theme across page reloads, including when API-backed state is loaded.

#### Scenario: Light theme persists after reload

- **GIVEN** the user selects the light theme
- **WHEN** the page reloads and fetches API state
- **THEN** the document theme SHALL remain light
