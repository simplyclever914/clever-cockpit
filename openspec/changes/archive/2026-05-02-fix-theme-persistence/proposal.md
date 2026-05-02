# fix-theme-persistence

## Why

Theme is UI-only state stored in localStorage, but API-backed page loads overwrite state from the API response that does not contain `theme`. After reload, selected light theme returns to dark.

## What changes

- Store theme in a dedicated localStorage key.
- Preserve theme when normalizing API state.
- Save theme immediately on theme button clicks.

## Impact

UI-only fix.
