# Design

## Digest approval pattern

Cron jobs still generate drafts/artifacts and perform local validation. Instead of executing external publish/send directly, they create a Cockpit approval:

- AI wrap-up: `digest_publish_and_send` publishes static artifact and sends/pins prepared Telegram text.
- Reflection / Telegram review: `telegram_send_and_pin_digest` sends/pins prepared Telegram text.

## Why composite for AI wrap-up

Publishing and Telegram delivery are coupled because the Telegram message links to the page. A single composite approval prevents approving send before publish.

## Delivery behavior

Cron delivery remains `none`; Cockpit becomes the approval surface. Failure alerts still fire if generation or approval creation fails.
