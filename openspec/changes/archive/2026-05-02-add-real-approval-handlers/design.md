# Design

## Typed approvals

Approvals receive two optional fields:

- `handler`: an allowlisted handler name.
- `payload_json`: a JSON object consumed by that handler.

The browser/API never accepts shell commands. The runner maps handler names to local Python functions.

## Handlers

Initial real handlers:

- `sourcecraft_publish`: publishes a static artifact via the existing SourceCraft publisher script.
- `telegram_send_and_pin_digest`: sends a digest text file to Telegram and pins the first message via the existing send-and-pin script.
- `record_only`: records approval completion for policy-only confirmations.

## Path safety

Handlers validate paths before execution. Telegram digest text may come from the workspace or `/tmp`; SourceCraft artifacts must come from the workspace. Secrets are loaded from existing local env files and are not stored in Cockpit payloads.
