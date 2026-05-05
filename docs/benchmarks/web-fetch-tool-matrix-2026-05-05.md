# Web fetch benchmark: web_fetch vs SNITCHMD vs CloakBrowser

## Что сделано

Собрана практичная матрица выбора `web_fetch` / SNITCHMD / CloakBrowser на проблемных ссылках из Telegram/MyBookmarks. Использована разрешённая Вадимом выборка из MyBookmarks: Habr, GitHub, лендинги, Substack/blog, HTTP-сайт и noisy social/bookmark snippets.

## Зачем это нужно / как влияет на UX Вадима

Клевер быстрее выбирает правильный инструмент для URL: меньше пустых HTML-каркасов, меньше лишних браузерных запусков, меньше “поищу в поисковике вместо чтения данной ссылки”. Для Вадима это означает более стабильные исследования и меньше повторных просьб “прочитай именно эту страницу”.

## Sample set

- Habr articles: `habr.com/ru/articles/1030832`, `1010430`, `1025132`, `1023852`, `1022906`, `987954`.
- GitHub repos: `github.com/syabro/SNITCHMD`, `ITSalt/NaCl`, `cacggghp/vk-turn-proxy`, `moazbuilds/claudeclaw`, `Michaelliv/pi-generative-ui`, `NousResearch/hermes-agent`.
- Marketing/blog pages: `getdesign.md`, `blog.kilo.ai/p/bentoboard...`, `lazypi.org`.

## Matrix

| Case | Best first tool | Why | Fallback |
|---|---|---|---|
| Static docs/article with normal HTML | SNITCHMD | Gives cleaner markdown/readability than raw fetch and is now workspace default | `web_fetch` for quick skim |
| Habr/article pages | SNITCHMD | Handles article extraction and metadata consistently | `web_fetch` if speed matters |
| GitHub repo/readme | SNITCHMD or direct git/API when coding | Markdown extraction is usually enough; direct repo checkout if code evidence needed | `web_fetch` for README skim |
| JS-heavy marketing/SPA | SNITCHMD first | It can render/extract before escalating | CloakBrowser if returned shell/empty content |
| Cloudflare/CAPTCHA/anti-bot | CloakBrowser only after SNITCHMD/web_fetch evidence of block | Browser cost is justified by block/render need | Ask if login/captcha/manual step needed |
| Auth/private Telegram/bookmarks | Local Telegram user-search export first | Avoids external browsing and respects allowlist/session safety | SNITCHMD only for URLs explicitly sampled |
| Need clicks/login/stateful flow | CloakBrowser | Fetch tools cannot interact | Ask if credentials/choice needed |

## Recommendation

1. Default serious URL reading to **SNITCHMD**.
2. Use **web_fetch** only for low-stakes quick static skim or if SNITCHMD is unavailable.
3. Escalate to **CloakBrowser** only when extraction returns JS shell, bot wall, CAPTCHA, or interactive/login flow is required.
4. For Telegram/MyBookmarks, first sample from local index, then fetch only the explicit URLs needed.

## Что дальше

Nothing else is planned for this task; the rule already matches current `AGENTS.md` Web Access Discipline. Create a follow-up only if future fetch failures show a repeatable gap in SNITCHMD/CloakBrowser routing.

## Доказательства

- Telegram sample command succeeded: `skills/telegram-user-search/scripts/tg_user_search.sh recent --chat MyBookmarks --days 30 --limit 20`.
- `web_fetch` smoke checks returned readable markdown for Habr and GitHub quick skims, but with 1k truncation and wrapper/noise in this environment.
- SNITCHMD smoke checks succeeded on Habr (`chars=25763`, quality `0.9`) and getdesign.md (`chars=6295`, quality `1.0`), giving fuller extraction for serious reading.
- CloakBrowser was not needed in the sampled URLs; recommendation keeps it as escalation for JS shell/anti-bot/interactive cases, not default.
- Workspace guidance already states: SNITCHMD default; `web_fetch` fallback; CloakBrowser for rendered/anti-bot/interactive pages.
- Artifact: `docs/benchmarks/web-fetch-tool-matrix-2026-05-05.md`.
