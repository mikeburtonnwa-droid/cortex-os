---
name: pressure-testing
description: Run seven adversarial checks against an artifact (finding, draft, decision, configuration change) before treating it as final. Invoke before any commit, any external publication, any consequential dispatch from the orchestrator to a downstream agent.
triggers:
  - pressure test
  - adversarial check
  - quality gate
  - pre-commit review
  - before publication
---

# Pressure-Testing Protocol

Pressure-testing is the quality gate that runs before any artifact ships. The protocol catches deterministic violations and surfaces judgment-dependent issues for human review.

## The seven checks

Run all seven against every candidate artifact.

**1. AI signature scan.** Em dashes in prose, banned vocabulary (delve, landscape, leverage, robust, utilize, streamline, spearhead, holistic, synergy, paradigm), throat-clearing phrases (it's important to note, in conclusion, to summarize). Run via `runtime/pressure_testing_harness.py` for automated scanning. Manual scan for cases the harness misses.

**2. Veracity flag.** Every substantive numeric claim has a citation marker in the same paragraph. Currencies, percentages, three-digit-or-more numbers, decimals. If the number is real, the source must be addressable.

**3. Falsifiability flag.** Every claim that uses a hedge word (could, possibly, perhaps, might) either contains a number or a conditional structure that grounds the hedge. "The market could shift" is filler; "If the proposed tariff passes in Q3, the market structure reverses" is a real claim.

**4. Confidence label check.** For analytical content, every finding heading carries a confidence label (high, medium, low) with a one-sentence rationale. Findings without labels are opinions.

**5. Scope drift heuristic.** File length growth beyond the documented budget. Sections not listed in the relevant spec. Features the operator did not request. Cut what does not move the deliverable forward.

**6. Three-part cadence count.** Count "X, Y, and Z" patterns. Three-part lists are an AI cadence when overused. Five or more per artifact is a flag for review.

**7. Sentence-length variance.** Pure AI prose has low variance. Mix sentence lengths. Short sentences, occasional long ones, occasional fragments. The variance is what gives prose a human texture.

## Severity tiers

Findings are categorized as blocker, major, or minor.

Blocker: publication-stopping. The artifact cannot ship until resolved.

Major: must fix before publication. The artifact ships with a known issue if not resolved.

Minor: review but not blocking. May be a false positive; may be a legitimate edge case. Operator judgment applies.

## When to halt

Halt and surface to the operator in three cases.

First: any blocker. The artifact does not ship until the operator approves the resolution path.

Second: more than three majors. The artifact has accumulated enough quality debt that a fresh draft is faster than patching.

Third: the same finding appears on consecutive passes. The fix did not stick. Diagnose the root cause before patching again.

## Invocation

The runtime layer ships `runtime/pressure_testing_harness.py` as the automated implementation. Run it before any commit:

```
python runtime/pressure_testing_harness.py --recursive .
```

For artifacts not under runtime tracking (a draft in a scratch file, a conversation summary), apply the seven checks manually. The protocol is the same; only the automation changes.
