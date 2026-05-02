# add-digest-approval-workflows

## Why

Digest cron jobs currently publish/send directly after generation. Now that Cockpit has typed approvals, real digest workflows should create pending approvals and let the runner execute approved external actions.

## What changes

- Add a composite `digest_publish_and_send` handler that publishes to SourceCraft then sends/pins the prepared Telegram summary.
- Add a workspace helper script for cron jobs to create typed Cockpit approvals without embedding API details in prompts.
- Update digest workflow docs and cron prompts to create approvals instead of directly sending/pinning.

## Impact

- Human approval becomes the final gate before digest publication/delivery.
- Runner remains the durable executor after approval.
