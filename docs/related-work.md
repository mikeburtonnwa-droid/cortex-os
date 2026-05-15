# Related Work

Cortex-OS sits in a maturing ecosystem of Claude Code reference patterns, agent orchestration frameworks, and cross-tool standards. This document acknowledges adjacent work and names what cortex-os adds beyond it.

## Claude Code reference patterns

[`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official). Anthropic's curated plugin marketplace, launched February 2026. The plugin marketplace is a curated distribution channel for first-class extensions; cortex-os is an opinionated reference pattern. Different concerns. A future cortex-os release may publish a plugin into the marketplace for the runtime utilities.

[`VILA-Lab/Dive-into-Claude-Code`](https://github.com/VILA-Lab/Dive-into-Claude-Code). Architectural analysis of Claude Code v2.1.88 following the March 2026 source release. Backward-looking documentation of how Claude Code works internally (1.6% AI decision logic, 98.4% deterministic infrastructure per their analysis). Cortex-OS is forward-looking pattern guidance for operators building on top of those primitives.

[`nateherkai/AIS-OS`](https://github.com/nateherkai/AIS-OS). MIT-licensed "AI Operating System" starter kit organized around a 3Ms/4Cs framework. Different architectural shape than cortex-os; both are valid expressions of the broader "AI OS" idea. Operators evaluating reference patterns should read both.

[`vanzan01/claude-code-sub-agent-collective`](https://github.com/vanzan01/claude-code-sub-agent-collective). Hub-and-spoke subagent collective with explicit context-engineering research framing. Overlaps with cortex-os at the agent teams layer. Cortex-OS adds the cascade and runtime validation; vanzan01 goes deeper on the subagent research itself.

[`affaan-m/everything-claude-code`](https://github.com/affaan-m/everything-claude-code). Agent harness performance optimization patterns. Focused on the runtime envelope around Claude Code rather than the configuration discipline; complementary if both are adopted.

## Agent orchestration frameworks

[LangGraph](https://github.com/langchain-ai/langgraph). DAG-based agent orchestration with typed state and conditional routing. The right tool for workflows that genuinely need a graph runtime. Cortex-OS is not a graph runtime; the planned companion repository will demonstrate LangGraph wrapping a Cortex-OS-governed workflow as the production execution layer.

[CrewAI](https://github.com/crewAIInc/crewAI). Role-based agent crews with hierarchical or sequential processes. Ships as a pip package; lower friction to first run than cortex-os. Different opinions on context-boundary discipline; CrewAI is more permissive about inter-agent information sharing.

[AutoGen](https://github.com/microsoft/autogen). Microsoft's actor-style multi-agent conversation framework. More flexible inter-agent communication patterns than cortex-os's enforced hub-and-spoke. Different niche; choose based on whether your work has genuine peer-to-peer agent interaction.

[Anthropic Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk). Renamed from Claude Code SDK in September 2025. Supports parallel subagents and context isolation as native defaults. Cortex-OS composes Claude Code; the Agent SDK is the canonical programmatic interface to the same primitives.

[DSPy](https://github.com/stanfordnlp/dspy). Stanford's declarative programming model for LLMs with prompt compilation and optimization. Solves a different problem than cortex-os. Compatible: a cortex-os agent could call DSPy-compiled prompts.

[Letta](https://github.com/letta-ai/letta) (formerly MemGPT). Memory-focused agent architectures. Sophisticated state persistence beyond what cortex-os does with markdown Current Reality blocks.

## Cross-tool standards

[AGENTS.md](https://agents.md). Cross-tool standard donated to the Linux Foundation's Agentic AI Foundation in December 2025. Read by Codex, Copilot, Cursor, Windsurf, Amp, and Devin. Claude Code does not auto-load AGENTS.md as of March 2026 (open feature request). Cortex-OS ships an `AGENTS.md` at the repo root that bootstraps cross-tool agents into the cortex-os pattern by pointing them at `CLAUDE.md`.

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2025-11-25). Anthropic-originated protocol for tool integration, also donated to the Linux Foundation's Agentic AI Foundation in December 2025. Cortex-OS uses MCP via `settings.json`; the pattern does not replace it. MCP and cortex-os are orthogonal.

[Skills (SKILL.md)](https://www.anthropic.com/news/skills). Native Claude Code primitive launched December 2025 with progressive disclosure. Cortex-OS ships five SKILL.md files at `_shared/.claude/skills/` that the reference agents declare as dependencies.

## Frameworks for thinking about the space

[Steve Yegge and Gene Kim, "Vibe Coding" / Developer-AI Evolution Scale](https://steve-yegge.medium.com/the-future-of-coding-agents-e9451a84207c). Eight-stage scale of developer-AI integration, where Stage 6+ describes CLI-driven multi-agent orchestration. Cortex-OS targets the Stage 6+ working environment. The scale has remained canonical through 2026 with continuing community discussion emphasizing "coherence through orchestration, not autonomy."

[Anthropic's writing on building agents](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk). The canonical reference for what Claude Code enables. Cortex-OS is one operator's opinionated composition of those primitives; Anthropic's writing is the authoritative source on the primitives themselves.

## What cortex-os adds beyond all of the above

Five things that no single artifact above provides together:

1. The explicit five-layer constitutional doctrine (root → domain → business → function → environment) with refinement rules and tier-graded function governance.

2. Unified schema validation across cascade, hooks, agent frontmatter, models.yaml, and tools.yaml via a six-script Python runtime layer.

3. An operationalized AI Signature Prohibition rule encoded as a post-tool-use hook, with documented exempt-paths for the rules documents that quote the banned vocabulary.

4. A fully instantiated reference business (ResearchCo) that demonstrates the cascade executing on a worked example, with three tier-graded function constitutions.

5. A working pre-compact carry-forward pattern using markdown plus JSON for durable session state, with a state-rewriter script that updates Current Reality blocks programmatically.

The first three are the strongest defensible novelty in May 2026. The fourth and fifth are useful demonstrations rather than original contributions.

## What cortex-os does not do

Cortex-OS is not a graph runtime. Use LangGraph for that.

Cortex-OS is not a workflow durability system. Use Temporal or Restate for that.

Cortex-OS is not a memory architecture. Use Letta or similar for that.

Cortex-OS is not a replacement for Claude Code, the Claude Agent SDK, or MCP. It composes them.

The planned companion repository wraps a Cortex-OS-governed workflow in LangGraph plus Temporal as the production execution layer. The two repositories together demonstrate the configuration-plus-execution story.
