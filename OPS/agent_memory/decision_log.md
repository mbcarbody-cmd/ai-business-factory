# Decision Log

Owner: PMO-2 Documentation & Memory Keeper
Status: active
Updated: 2026-06-14

## 2026-06-13 — Core OS must never stagnate

Trigger: User explicitly required the AI Business Factory to never stop in one place.

Decision: Every blocked task must immediately create an unblock task and switch the responsible agent to the next highest-value executable task.

Reason: Waiting creates dead work. The operating system must keep revenue, deploy, QA, delivery, and marketplace progress moving even when one path is blocked.

Affected OPS layer: task board, QA, deploy loop, revenue operations, product gates, delivery, marketplace.

Enforcement rule: Every task must have `blocker`, `fallback_next_task`, `deadline`, `proof_status`, and `proof_verified_by` fields. A blocked task without fallback is invalid.

Proof path: `OPS/operating_loops/ANTI_STAGNATION_ENGINE.md`, `OPS/task_board.json`.

## 2026-06-13 — Source of truth is OPS task board, not loose issues

Trigger: GitHub issues contained vague items and duplicated OPS control.

Decision: `OPS/task_board.json` is the source of truth. GitHub Issues may exist only as execution tickets linked to task IDs.

Reason: Two task systems create confusion and allow weak work to hide behind vague issue titles.

Affected OPS layer: task board, governance, PMO.

Enforcement rule: Every GitHub issue title or body must reference a task ID or be closed/merged into the board.

Proof path: `OPS/governance/ISSUE_AND_TASK_SOURCE_OF_TRUTH.md`.

## 2026-06-13 — AI capability strategy is tool-agnostic

Trigger: User asked to use all AI possibilities and learn from other AI systems.

Decision: The system will use a model/tool council instead of depending on one vendor. Cursor/Claude Code-style coding, OpenAI Agents-style guardrails/sessions/MCP, Google ADK-style graph workflows/evaluation/deploy, and AutoGen-style multi-agent experimentation are tracked as capabilities, not religious choices.

Reason: AI tools change fast. The repo needs stable operating principles: memory, tools, sandbox, guardrails, evals, cost tracking, and proof artifacts.

Affected OPS layer: model council, security, deploy, QA, CFO.

Enforcement rule: New AI tool adoption must create a capability entry, a security note, a CFO cost note, and one small repo proof.

Proof path: `OPS/model_council/AI_CAPABILITY_RADAR_2026.md`.

## 2026-06-13 — Demo proof beats strategy documents

Trigger: Core OS had many active layers but not enough working artifacts.

Decision: CEO Cockpit becomes the first internal proof product. It must read the operating layers conceptually and show tasks, blockers, revenue, CFO, QA, and next actions.

Reason: A dashboard turns hidden OPS JSON into visible management. It also creates a sellable internal-control demo for future SMB offers.

Affected OPS layer: product gates, deploy loop, QA, revenue operations, CFO.

Enforcement rule: Product maturity cannot advance on documents alone when a demo is possible.

Proof path: `products/ceo-cockpit/`.

## 2026-06-14 — Content intelligence must turn winning ads into our own mechanisms

Trigger: User provided a social screenshot where a micro-SaaS Telegram funnel used a developer-native pseudo-code post to sell the idea that small SaaS can beat job hopping.

Decision: Competitor intelligence expands from company/price tracking into content-funnel intelligence. Agents must collect strong ads, posts and funnels, deconstruct the mechanism, and convert it into our own hooks, page copy, short videos, outreach and product UX ideas.

Reason: Good social posts are not random content; they are sales mechanisms. The system must learn the formula and create revenue-linked variants without copying protected assets.

Affected OPS layer: competitor intelligence, agent memory, revenue operations, content factory, marketplace roadmap.

Enforcement rule: Every captured content pattern must record audience, pain/contrast, dream outcome, visual pattern, CTA, risk, reusable formula, our converted variants and output paths.

Proof path: `OPS/competitor_intelligence/content_funnel_patterns.md`, `OPS/agent_memory/competitor_findings.md`.
