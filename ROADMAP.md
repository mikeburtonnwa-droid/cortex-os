# ROADMAP

This document describes the planned production-execution companion to cortex-os. It is a working architectural plan, not a date commitment. Phasing and scope may evolve as the work progresses. The current cortex-os repository is stable; everything below describes future work that will live in a separate companion repository.

---

## The companion repository

Working name: `cortex-pipeline`. Planned location: `github.com/mikeburtonnwa-droid/cortex-pipeline`.

The companion repository will demonstrate cortex-os executing under production conditions. cortex-os is the configuration and discipline layer; cortex-pipeline will be the production execution layer. Together, the two repositories tell a complete story: how to compose Claude Code's primitives into a disciplined operating system, and how to run that operating system durably under real load.

Why a separate repository. cortex-os is a pattern; cortex-pipeline will be one specific workflow built on that pattern. Mixing the two would confuse the artifact. A reader who wants the configuration discipline reads cortex-os; a reader who wants the production execution clones cortex-pipeline.

---

## What the companion will demonstrate

A daily Morning Brief pipeline. The pipeline pulls fresh sources on a defined topic, runs them through research, analysis, writing, and review under cortex-os governance, scores the output with a RAG-triad evaluator, and publishes the result on a defined schedule. The pipeline runs as a long-running service that survives restarts, retries failures, and reports its quality metrics over time.

The workflow is fictional and generic, the same way ResearchCo is in cortex-os. It demonstrates the production execution pattern without exposing any real data.

Four technology layers compose the production stack:

**Temporal** wraps the workflow for durability. Each LangGraph node executes inside a Temporal activity. Temporal handles crash recovery, retries with exponential backoff, multi-day workflow continuity, and observability via the Temporal UI. Workflow versioning supported.

**LangGraph** defines the agent DAG. Five nodes: source-gather, source-evaluate, analyze, draft, review. State flows along edges as typed Pydantic objects. The reviewer node routes back to draft on failed review; LangGraph's conditional edges handle the loop. Maximum iteration count caps the loop to prevent runaway costs.

**Cortex-OS** governs the Claude calls inside each activity. The companion repository imports cortex-os as a git submodule. Every Claude call loads the relevant CLAUDE.md cascade for that agent's role, applies the hooks, uses the agent frontmatter from `reference/agents/`, and runs the response through the pressure-testing harness before returning.

**FastAPI** exposes the operator surface. Status endpoints for in-flight workflows, results endpoints for completed runs, an eval scores endpoint that drives the public dashboard, OpenAPI docs at `/docs`.

---

## Quality measurement as a first-class concern

A RAG-triad evaluation harness scores every Brief the pipeline produces. Three measurements:

**Context relevance.** Whether the retrieved chunks are relevant to the query. Target above 0.8.

**Groundedness.** Whether the answer's claims are supported by the retrieved chunks (catches hallucination). Target above 0.9.

**Answer relevance.** Whether the answer addresses the query. Target above 0.85.

Scores accumulate in a local store. A dashboard graphs trends over time. Regressions trigger automated holds on publication until reviewed.

This is what quality measurement looks like when treated as a first-class engineering concern rather than an afterthought.

---

## Planned repository structure

```
cortex-pipeline/
├── README.md
├── ARCHITECTURE.md
├── DEPLOY.md
├── docker-compose.yml
├── pyproject.toml
├── cortex-os/                     # git submodule
├── src/
│   ├── workflow.py                # Temporal workflow
│   ├── activities.py              # LangGraph nodes as Temporal activities
│   ├── graph.py                   # LangGraph DAG construction
│   ├── agents/                    # Claude calls under cortex-os governance
│   ├── cortex/                    # cortex-os Python integration package
│   ├── rag/                       # retriever, chunker, corpus loader
│   ├── eval/                      # RAG-triad scorer plus harness
│   ├── api/                       # FastAPI endpoints
│   └── schemas/                   # Pydantic models for state and outputs
├── corpus/                        # generic news/document corpus for demo
├── eval/                          # historical eval results
├── ops/                           # Temporal worker entry point plus deployment configs
└── tests/
```

---

## Planned phases

Twelve phases, executed in order.

1. **Repository setup.** Create the repo, .gitignore, pyproject.toml, docker-compose skeleton, add cortex-os as git submodule.

2. **Cortex-OS Python integration package.** Bridge between Python execution and cortex-os configuration. Cascade loader, hook subprocess wrappers, pressure-testing wrapper, unified `governed_claude_call` interface.

3. **Pydantic schemas.** Typed state for the LangGraph DAG. Source, Finding, Analysis, Brief, Review, EvalScore.

4. **LangGraph DAG.** Five-node graph with conditional routing back from review to draft. SQLite checkpointer for local; Postgres in production.

5. **Cortex-governed agents.** Researcher, analyst, writer, reviewer. Each loads cortex-os cascade and runs pressure-testing before returning.

6. **Temporal workflow.** MorningBriefWorkflow with retry policy, timeout policy, signals for cancellation and human-in-the-loop intervention, queries for in-flight status.

7. **RAG layer.** Retriever, chunker, sample corpus. Backed by LanceDB or pgvector.

8. **RAG-triad eval.** Context relevance, groundedness, answer relevance. Scores stored in SQLite; dashboard reads from the store.

9. **FastAPI service.** Status, results, eval scores, eval dashboard endpoints. OpenAPI docs.

10. **Docker compose orchestration.** Temporal server, worker, API, and database wired up for `docker-compose up`.

11. **Deployment.** Fly.io or Render, public URL.

12. **Documentation.** README under 600 words, ARCHITECTURE.md under 3,000 words, DEPLOY.md under 1,000 words, eval methodology doc.

Estimated effort: 22 to 32 hours of focused work. Critical-path phases are 2 (cortex integration), 4 (LangGraph), 6 (Temporal), and 8 (eval). Others are mostly mechanical once the critical infrastructure is in place.

---

## Acceptance criteria

The companion repository will be ready when:

1. A reader can fork the repo, run `docker-compose up`, and trigger a workflow run via curl inside thirty minutes from clone.
2. The deployed public URL serves the eval dashboard and the Temporal UI to unauthenticated viewers.
3. The README scans cleanly in under thirty seconds.
4. The ARCHITECTURE.md is defensible to a senior AI infrastructure engineer who has not seen the repo.
5. No real client data, no proprietary methodology, no credentials in any committed file. Same data governance bar as cortex-os.
6. The cortex-os submodule loads cleanly; the governance integration tests pass.
7. Eval scores accumulate over time. The dashboard shows historical trends.
8. Both repositories cross-link: cortex-os README points at the cortex-pipeline URL; cortex-pipeline points at cortex-os as the configuration source.

---

## What this is not

Not a framework to compete with LangChain, LangGraph, or CrewAI. The companion repository uses LangGraph as the agent orchestration runtime.

Not a SaaS or hosted service. The deployed public URL exists for demonstration; production use requires a separate deployment with appropriate operational controls.

Not a production system for any real workload. The Morning Brief is a fictional demonstration. Operators adapting this pattern to real workloads need to adjust the corpus, the eval thresholds, the retry policies, and the deployment topology for their specific context.

---

## Deferred decisions

Three decisions to make at the start of execution:

1. **Final repository name.** `cortex-pipeline` is the working name. Alternatives: `morning-brief-pipeline` (workflow-focused), `cortex-execution` (descriptive), `cortex-companion` (explicit pairing).

2. **Deployment target.** Fly.io (cheaper at idle, better Temporal support) or Render (simpler configuration).

3. **RAG backend.** LanceDB (embedded, simpler) or pgvector (integrates with Temporal's PostgreSQL).

These will be resolved in the cortex-pipeline README once execution begins.

---

## Status

Not started. The cortex-os repository will run on its current launch trajectory for a period of community engagement before this companion workstream opens. The current expectation: two to four weeks between cortex-os launch and cortex-pipeline kickoff.

Updates to this roadmap will be reflected in this file in cortex-os. The companion repository, once created, will become the canonical source for its own status.
