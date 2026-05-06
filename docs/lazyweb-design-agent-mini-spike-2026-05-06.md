# Mini-spike Lazyweb/design-agent stack — 2026-05-06

## Вопрос
Стоит ли подключать Lazyweb/design-agent stack в рабочий UI workflow Вадима/OpenClaw сейчас?

## Что проверено
- Web evidence по Lazyweb: EveryDev.ai описывает Lazyweb как agent-first design research platform с 257k+ real app screens, 6 opinionated agent skills, MCP server для Claude Code/Codex/Cursor и HTML/Markdown report output. Source: https://www.everydev.ai/tools/lazyweb
- GitHub repo `aboul3ata/lazyweb-skill`: packaged as Codex plugin/Claude plugin; uses hosted MCP `https://www.lazyweb.com/mcp`, `mcp-remote`, token in `~/.lazyweb/lazyweb_mcp_token` or `LAZYWEB_MCP_TOKEN`; skills include design research, quick references, design improve, brainstorm. Source: https://github.com/aboul3ata/lazyweb-skill
- Local fallback: existing Cockpit/OpenClaw UX specs already work as `DESIGN.md`-like artifacts (`docs/ux-specs/openclaw-telegram-*.md`) with clear flows, buttons, risks, next steps.

## 2–3 воспроизводимых UI сценария

1. **Telegram mobile command palette**  
   Input: current UX spec + screenshot/result card context.  
   Expected Lazyweb use: quick references for mobile command palette/action sheets; compare destructive confirmation patterns.  
   Fallback: spec-first implementation with tests for stale callback/wrong user/destructive confirmation.

2. **Cockpit task board / stale work handoff**  
   Input: current Cockpit tasks states (`open`, `waiting`, `done`, `stale`) and Hermes/Kanban backlog signal.  
   Expected Lazyweb use: research kanban/handoff/status affordances from real products.  
   Fallback: small HTML mock in `app/index.html` + evidence from current task filters.

3. **Artifact/result card for Telegram**  
   Input: existing artifact/result card UX spec.  
   Expected Lazyweb use: references for compact mobile cards with status, actions and provenance.  
   Fallback: reuse existing OpenClaw presentation blocks/buttons and validate payload length.

## Требования к контексту
- Use Lazyweb only after a concrete UI task exists, with current screenshot/spec and target user flow.
- Keep downloaded screenshots/reports local and gitignored unless intentionally committed.
- Do not store MCP token in repo; treat `~/.lazyweb/lazyweb_mcp_token` as local ignored secret/config.
- For implementation, require normal tests: callback routing, stale/wrong-user, destructive confirmation.

## Ограничения
- Hosted MCP/token setup is an external integration, so scheduled runner should not install/connect it automatically without Vadim’s explicit approval.
- Lazyweb can improve references, but it does not replace product decisions or tests.
- Claude plugin path is not useful here because Vadim has forbidden Claude Code; Codex plugin path is the relevant one.

## Рекомендация
**Повторить позже / conditional adoption.** Do not connect Lazyweb globally now. For the next concrete UI implementation, create a safe follow-up: install/configure Lazyweb for Codex only if Vadim approves external MCP/token setup; otherwise use the local fallback (`DESIGN.md`/UX spec + screenshots + tests). This keeps UI quality gains possible without adding external surface area prematurely.
