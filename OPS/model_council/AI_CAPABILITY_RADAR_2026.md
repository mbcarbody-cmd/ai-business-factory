# AI Capability Radar 2026

Owner: CTO-1 Product Factory Architect + PMO-3 Strategic Prioritization Officer
Status: active
Updated: 2026-06-13

## Purpose

Track external AI system capabilities and convert them into repo actions. The goal is not to copy every tool. The goal is to extract operating principles that improve revenue, build speed, safety, delivery and marketplace automation.

## Sources checked on 2026-06-13

- OpenAI Agents SDK documentation: agents, tools, handoffs, guardrails, sessions, MCP, tracing, sandbox agents.
- Anthropic Claude Code documentation: codebase reading, file edits, command execution, IDE/terminal/web surfaces, recurring/cloud sessions.
- Google Agent Development Kit documentation: graph workflows, multi-agent workflows, model routing, evaluation, observability, deployment, MCP/A2A.
- Microsoft AutoGen documentation: AgentChat, Core event-driven agents, Studio, MCP workbench, Docker code execution.
- Recent AI-agent research: agent systems need permission control, context management, memory, tool execution, and verifiable artifacts.

## Capabilities to adopt

| Capability | Why it matters | Repo action |
|---|---|---|
| Agent memory / sessions | Prevent repeated weak work | `OPS/agent_memory/` |
| Tool calling / MCP | Let agents use repo, files, pipelines and marketplace data safely | Future local MCP server for OPS files |
| Guardrails | Block bad outputs, unsafe changes and false done states | `OPS/qa/bug_board.json`, `OPS/security/` |
| Human approval | Keep destructive, money, deploy and customer actions controlled | `OPS/security/AI_AGENT_SECURITY_POLICY_LT.md` |
| Tracing / observability | Know why work moved or failed | Future `OPS/telemetry/agent_runs.json` |
| Sandbox coding | Let coding agents work without risking production | Cursor/Claude Code style local branches and PRs |
| Graph workflows | Use deterministic flow for predictable business processes | Marketplace seller OS workflow graph |
| Evaluation / simulation | Test agents before client delivery | `OPS/qa/critic_checklist.md` future task |
| Cost routing | Use cheaper models for simple tasks and stronger models for hard tasks | `OPS/cfo/pricing_logic.md` |
| Verifiable artifacts | Every agent output must leave visible proof | `OPS/task_board.json`, product demos, tests |

## Tool-positioning rule

- OpenAI Agents SDK style: best for production agent runtime, guardrails, tracing, handoffs, sessions and MCP.
- Claude Code / Cursor style: best for repo coding, refactor, tests, PRs, and multi-file implementation.
- Google ADK style: best for graph workflows, deployment architecture, model routing and evaluation patterns.
- AutoGen style: best for experimental multi-agent patterns and event-driven prototypes.

## Next repo actions

1. Keep Cursor as the first coding execution layer.
2. Add local OPS audit script and CI guardrail.
3. Build CEO Cockpit as the first proof dashboard.
4. Design future local MCP server only after OPS files stabilize.
5. Add AI cost-per-task tracker before scaling paid pilots.
6. Use graph workflow thinking for Parts Seller OS, not free-form marketplace sprawl.

## Adoption rule

No new AI tool is adopted just because it is new. It must improve one of:

- speed to revenue,
- product proof,
- delivery reliability,
- QA/security,
- model cost per task,
- marketplace data quality,
- owner visibility.
