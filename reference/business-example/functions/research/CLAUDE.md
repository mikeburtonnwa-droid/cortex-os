# CLAUDE.md – ResearchCo Research Function
**ResearchCo · Research Function (Tier 1) · v1.0 · 2026-05-14**

---

## What This Function Does

The research function is the source of truth for everything downstream. It gathers external and internal information against a research question, evaluates source credibility, and produces structured findings with explicit citations. Every claim that eventually reaches a client deliverable traces back to a source captured here.

Tier 1 governance applies. This is the function with the highest cost of error in the business; a sourcing failure here contaminates every downstream analysis and deliverable.

---

## Default Agent and Model

The researcher agent at `reference/agents/researcher.md` is the default for this function. The agent specifies `model: sonnet` in its frontmatter. The research function overrides this to opus for engagements where source credibility is contested or where the research question touches a domain where stale or unreliable sources are common.

Override via the function's models.yaml (if present) or by passing an explicit model directive to the agent invocation.

---

## Tier 1 Governance Rules

These rules apply in addition to the business-level operating principles.

1. **No anonymous web content as a finding.** Anonymous web content can surface a hypothesis but cannot serve as the source for a claim in a deliverable. Trace every anonymous lead to a named primary or secondary source before treating it as a finding.

2. **Source date sensitivity.** Every source carries its publication date in the structured output. The analyst function downstream is responsible for evaluating staleness; the researcher is responsible for recording the date accurately.

3. **No paraphrase without citation.** Even paraphrased claims require a source. The structured output records the source, the original language if a translation is involved, and the paraphrase if one was applied.

4. **Failed lookups are findings.** If a research question cannot be answered with available sources, that fact is itself a finding. It ships to the analyst as "source gap, this dimension of the question is uncovered." It does not silently disappear.

---

## Hooks Configured for This Function

All four base hooks apply. The post-tool-use hook is configured to scan researcher outputs (markdown files in the research workspace) for AI signature violations before they reach the analyst. The pre-tool-use hook blocks external research tools that lack an explicit approval flag on calls that involve outbound communication (email to a primary source contact, for example).

---

## When the Function Halts

The research function halts and escalates to the operator in three cases.

Source library outage. If the internal source library is unreachable, no engagement-relevant research can proceed. The researcher does not substitute web search for the library; the operator must restore access first.

Conflicting primary sources without a tiebreaker. If two primary sources disagree on a fact and no third source can adjudicate, the researcher surfaces both and asks the operator to choose how to proceed.

Source credibility falls below the threshold. The researcher maintains a per-engagement credibility floor. If every source available for a given claim falls below it, the function halts rather than ship a low-credibility finding into analysis.

---

## Cascade Directive

The cascade resolved at this directory is:

```
cortex-os/CLAUDE.md                                  (root)
  ↳ reference/business-example/CLAUDE.md             (business)
    ↳ reference/business-example/functions/research/CLAUDE.md   (this file)
```

This file refines the business rules. It does not weaken them. If you are reading this and any rule above appears to contradict a rule below, the rule above wins on the contradicted point.
