# Findings: Lazyweb / design-agent stack for UI workflows

_Date: 2026-05-06_

## Bottom line

There **is** a practical Lazyweb option to install/connect: the `aboul3ata/lazyweb-skill` repo packages Lazyweb as a Codex/Claude plugin plus hosted MCP server. It is directly aimed at UI/design research for coding agents, not generic browser automation. Recommendation: **try Lazyweb as the first external design-research layer**, then keep a local fallback workflow based on `DESIGN.md` + screenshots/vision + Figma MCP when project-specific source-of-truth matters more than public inspiration.

## Evidence

### 1. Lazyweb is currently positioned as an agent-first design research MCP

- Lazyweb home page says it provides “agent-first design research,” “257k+ real screens,” “research-backed best practices,” and “opinionated workflows,” with MCP support for “Claude Code, Codex & Cursor.” Source: https://www.lazyweb.com/
- Secondary coverage describes it as “Mobbin meets an AI agent” connected via MCP, with “257,000+ real app screens from 25,000+ companies,” free for humans and agents. Source: https://mindwiredai.com/2026/05/05/lazyweb-is-free-the-tool-that-fixes-ais-biggest-design-problem/
- Directory/listing sources also identify it as a “Design Research MCP for Agents.” Source: https://www.everydev.ai/tools/lazyweb

### 2. Practical install/connect path exists

Primary repo: https://github.com/aboul3ata/lazyweb-skill

Key implementation details from the repo README:

- Packaged as a **Codex plugin** with plugin source, skills, MCP config, and marketplace entry.
- Uses hosted MCP endpoint `https://www.lazyweb.com/mcp` through `mcp-remote`.
- Auth can be a free no-login token stored in `LAZYWEB_MCP_TOKEN` or `~/.lazyweb/lazyweb_mcp_token`.
- Claude Code install path:
  ```bash
  claude plugin marketplace add https://github.com/aboul3ata/lazyweb-skill
  claude plugin install lazyweb@lazyweb
  ```
- Token generation path:
  ```bash
  mkdir -p ~/.lazyweb
  curl -sS -X POST https://www.lazyweb.com/api/mcp/install-token \
    -H "content-type: application/json" \
    -d '{}' | node -e "let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>require('fs').writeFileSync(process.env.HOME+'/.lazyweb/lazyweb_mcp_token', JSON.parse(s).token))"
  ```
- Verification suggested by the repo: list MCP tools, run `lazyweb_health`, then run `lazyweb_search` with e.g. `{ "query": "pricing page", "limit": 3 }`.

Public MCP tools / aliases listed by the repo:

- `lazyweb_search` — find screenshots matching a description; supports filters like category, company, platform.
- `lazyweb_compare_image` — find visually similar screenshots from an image URL/base64.
- `lazyweb_find_similar` — find screenshots similar to a previously found one.
- Canonical tools include `search_screenshots`, `list_filters`, `vision_screenshots`, `metadata_screenshots`.

Skills listed by Lazyweb plugin:

- `lazyweb-design-research` — competitor/design research with examples, patterns, anti-patterns, recommendations.
- `lazyweb-quick-references` — fast reference screenshot lookup.
- `lazyweb-design-improve` — screenshot current app, find similar best-app references, suggest improvements.
- `lazyweb-design-brainstorm` — cross-category pattern search.
- plus inspiration-source connect/remove helpers.

### 3. Figma MCP is the stronger source-of-truth path for actual product designs

Official Figma docs say the Figma MCP server lets agents:

- get design context/code from Figma, FigJam, and Make files;
- create/modify native Figma content;
- capture live UI as design layers;
- improve component workflows with Code Connect.

Sources:

- Figma help guide: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server
- Figma MCP guide repo: https://github.com/figma/mcp-server-guide/

Important practical notes:

- Remote Figma MCP server is available on all seats/plans; desktop server requires Dev or Full seat on paid plans.
- Figma MCP supports clients including VS Code, Cursor, Windsurf, Claude Code, and Codex.
- The official guide gives MCP config using `https://mcp.figma.com/mcp` and says Claude Code can install `figma@claude-plugins-official` or add the HTTP MCP manually.
- Rate limits apply. The guide says Starter/View/Collab seats are limited to up to 6 read-tool calls/month; paid Dev/Full seats have per-minute limits similar to Figma REST API Tier 1.
- Useful tools include `get_design_context`, `get_screenshot`, `get_metadata`, `create_design_system_rules`, and Code Connect mapping tools.

### 4. DESIGN.md is a lightweight fallback / guardrail layer

DesignMD positions `DESIGN.md` as a single markdown design-system file an AI coding tool reads to build consistent UI. Usage is intentionally simple: download a `DESIGN.md`, drop it at repo root next to README, then tell the agent to use it. Source: https://designmd.ai/

Practical role:

- Good for style guardrails when no Figma file exists.
- Works well as a repo-local artifact that any agent can read.
- Less suitable for exact UI fidelity than Figma MCP or screenshots, because it encodes design rules rather than concrete frames.

### 5. Screenshot/vision loop is the essential fallback for iteration

A current example workflow is `app-screenshots`, which uses Vercel’s `agent-browser` to let agents capture annotated screenshots and generate markdown visual guides. The post says it works with Claude Code, Cursor, Windsurf, Codex, Gemini CLI, and other skill-capable agents. Source: https://alexop.dev/posts/app-screenshots-claude-code-skill/

Useful pattern:

1. Run local dev server.
2. Capture page/flow screenshots with browser automation.
3. Use vision analysis to compare actual UI against `DESIGN.md`, Figma frame screenshots, or Lazyweb references.
4. Patch UI.
5. Repeat until screenshot diffs/visual review pass.

## Recommended stack for UI agent workflows

### Option A — Best quick win: Lazyweb + local screenshot loop

Use when starting from a blank UI, redesigning a page, or needing competitive references.

- Connect Lazyweb MCP/plugin.
- Ask for `lazyweb-design-research` or `lazyweb-quick-references` for the target screen type.
- Store generated reports/references under `.lazyweb/...` or project docs.
- Build UI using those references plus local constraints.
- Screenshot local app and use `lazyweb-design-improve` / vision review for iteration.

### Option B — Best source-of-truth: Figma MCP + screenshots

Use when the product has actual Figma designs or design system components.

- Connect Figma MCP.
- Pull `get_design_context` and `get_screenshot` for selected frames.
- Generate `create_design_system_rules` into project rules/instructions.
- Implement with Code Connect mappings where available.
- Validate by screenshot comparison against Figma frame.

### Option C — Lowest-friction fallback: `DESIGN.md` + screenshots + human refs

Use when no MCP setup is available or rate limits/secrets block external tools.

- Put `DESIGN.md` in repo root.
- Add `docs/design/references.md` with screenshots/URLs and short notes.
- Use browser screenshot capture after each UI pass.
- Require the agent to cite which `DESIGN.md` rule or screenshot reference each visual decision follows.

## Caveats / confidence

- Confidence is **high** that Lazyweb is a practical current tool to try: multiple sources and the GitHub README show a concrete MCP/plugin/token path.
- Confidence is **medium** on long-term stability: Lazyweb appears newly launched/free; validate endpoint availability, MCP config compatibility with OpenClaw/Codex, and any future pricing/rate-limit changes before depending on it.
- Figma MCP is official and more durable, but seat/rate-limit constraints can make it less frictionless than Lazyweb for quick design inspiration.
- `DESIGN.md` is useful as a local convention, but it should not replace visual evidence when fidelity matters.
