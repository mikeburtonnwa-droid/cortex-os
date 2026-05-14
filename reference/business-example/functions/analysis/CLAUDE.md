# CLAUDE.md – ResearchCo Analysis Function
**ResearchCo · Analysis Function (Tier 2) · v1.0 · 2026-05-14**

---

## What This Function Does

The analysis function receives structured findings from research and produces interpreted findings: frameworks, evidence chains, comparative assessments, and confidence-scored conclusions. The output is internal-facing, structured, and machine-readable. The delivery function shapes it for client audiences.

Tier 2 governance applies. The function operates on inputs that have already passed Tier 1 quality gates. Scrutiny is standard rather than maximum.

---

## Default Agent and Model

The analyst agent at `reference/agents/analyst.md` is the default for this function. The agent specifies `model: opus` because adversarial evaluation of evidence rewards deeper reasoning. The function does not override the agent default.

For high-throughput classification or routing tasks within an engagement (tagging sources by relevance, for example), the orchestrator may dispatch to a haiku-routed sub-task. The analyst's primary work remains opus.

---

## Tier 2 Governance Rules

These rules apply in addition to the business-level operating principles.

1. **Every finding has a confidence label.** High, medium, low. Findings without labels are opinions, not findings; the function rejects unlabeled output and returns it to the analyst.

2. **Frameworks are built, not assumed.** When the analyst applies a framework (Porter's Five Forces, a competitive matrix, a SWOT, anything similar), the framework's relevance to the engagement is documented as part of the output. Frameworks selected for convenience contaminate analysis.

3. **The disconfirming question is mandatory.** Every finding ships with a one-sentence answer to: "what would make this finding wrong?" If the analyst cannot articulate what would invalidate the finding, the finding has not been pressure-tested and the function rejects it.

4. **Cross-engagement isolation.** The analyst never references findings from a different engagement, even when they would be informative. Each engagement has its own analysis workspace.

---

## Hooks Configured for This Function

All four base hooks apply. The post-tool-use hook scans analysis output for AI signature violations. The stop.sh hook is configured to require a session summary on every analyst session: the four anchors (decided, built, changed, next) plus an additional anchor specific to this function: open questions for next session.

---

## When the Function Halts

The analysis function halts and escalates to the operator in three cases.

Insufficient research input. If the research function delivered an output missing the dimensions the analyst was asked to evaluate, analysis does not begin. The work returns to research.

Framework selection cannot be defended. If the analyst cannot articulate why a chosen framework fits the engagement, the framework is dropped and the analyst restarts with a more native structure.

Conclusion changes hands too many times. If the same finding has been revised three times without converging, the analyst surfaces the underlying disagreement to the operator. Iterating further is not analysis; it is drift.

---

## Cascade Directive

The cascade resolved at this directory is:

```
cortex-os/CLAUDE.md                                  (root)
  ↳ reference/business-example/CLAUDE.md             (business)
    ↳ reference/business-example/functions/analysis/CLAUDE.md   (this file)
```

This file refines the business rules. It does not weaken them.
