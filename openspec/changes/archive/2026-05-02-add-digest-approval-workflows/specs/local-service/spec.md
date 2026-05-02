## ADDED Requirements

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
