# CLAUDE.md – ResearchCo Business Constitution
**ResearchCo · Reference Business · v1.0 · 2026-05-14**

---

## What ResearchCo Is

ResearchCo is a fictional market research firm used as the reference business for Cortex-OS. It is not a real company. It exists in this repository as a worked example of the cascade pattern operating on a coherent business with three functions, defined customers, and explicit operating principles.

ResearchCo provides sector intelligence and competitive analysis to corporate clients. Engagements typically span four to eight weeks and conclude with a written deliverable plus a debrief presentation.

Read this file before working in any `reference/business-example/` subdirectory. The root cortex-os/CLAUDE.md takes precedence on universal rules. This file adds business-specific operating context.

---

## Customers and Engagements

ResearchCo serves three customer types.

Corporate strategy teams commissioning sector-level reports for upcoming board meetings. Engagement length four to six weeks. Deliverable: written report plus presentation.

Private equity associates preparing for diligence on a target. Engagement length two to three weeks. Deliverable: a target dossier plus key-person interviews summary.

Independent boards commissioning competitor intelligence for an annual planning cycle. Engagement length six to eight weeks. Deliverable: competitive map plus narrative analysis.

Engagement scope is fixed at contract signing. Scope changes require a written amendment. The orchestrator agent refuses scope drift on this basis.

---

## Operating Principles (Business-Level)

These refine the root operating principles for the conditions of ResearchCo's work. The root principles continue to apply.

1. **Source before synthesis.** No claim enters a deliverable without a primary or named secondary source. Anonymous web content is a lead, not a finding.

2. **Engagements are deliverable-driven, not hours-driven.** The team optimizes for the quality of the artifact at delivery, not for the volume of work in between.

3. **Client confidentiality is absolute.** Information learned in one engagement never appears in another, even when the second client would benefit. This rule has no exception clause.

4. **Findings are reproducible.** Any conclusion in a deliverable must be reconstructible from the source library and the analysis notes. If the analyst cannot reproduce the path from source to finding, the finding is removed.

---

## Function Map

ResearchCo operates three functions. Each has its own CLAUDE.md at `functions/<name>/CLAUDE.md`.

`research` (Tier 1) gathers information from external and internal sources. Operates the source library. Highest governance scrutiny; this function produces the inputs that all downstream work depends on.

`analysis` (Tier 2) interprets the research output into structured findings. Builds frameworks and synthesizes evidence chains. Standard governance; produces internal artifacts that the delivery function consumes.

`delivery` (Tier 3) produces client-facing artifacts: written reports, presentations, debriefs. Light governance, high-throughput; the prior functions have already done the quality work.

Tiers are a governance signal, not a hierarchy. A Tier 3 function with a missing input from a Tier 1 function will halt. Tier governs scrutiny and default model selection, not authority.

---

## Communication Style for Client Work

The root communication style applies. The following refinements apply specifically to client-facing artifacts.

External deliverables use a formal register. Direct does not mean blunt; lead with the answer, but frame for a professional reader.

Client confidence levels are stated explicitly. Every key finding ships with a confidence label: high, medium, low. Without a label the finding is not a finding; it is opinion.

No hedge language in client outputs unless the hedge is doing work. "It is possible that the market may shift" is filler. "If the proposed tariff passes in Q3, the market structure reverses" is doing work.

---

## Quality Standards

Every external deliverable passes through three gates before client delivery.

Source gate: every claim has a source. The reviewer agent walks the deliverable claim by claim. Unsourced claims are removed or sourced.

Pressure-testing gate: the reviewer agent runs the seven adversarial checks against the deliverable. Failures at blocker or major severity block delivery.

Voice gate: the post-tool-use hook scans the deliverable for AI signature artifacts. The deliverable does not ship until the hook returns clean.

The three gates run in order. Failure at any gate returns the deliverable to the relevant upstream function with the failure report attached.

---

## Data Governance (Business-Level)

The root data governance bar applies. The following refinements apply to ResearchCo client work.

Client data is segregated by engagement. Each engagement gets its own workspace; no cross-engagement queries.

Source data is retained for the duration of the engagement plus seven years for audit. After that, raw sources are archived; only the deliverable and the analysis notes remain in the active workspace.

The reference business in this repository contains no real client data. All examples, source references, and engagement details are fictional and used solely to demonstrate the cascade.

---

## Current State

**Updated: 2026-05-14**

ResearchCo as a reference business is a worked example in cortex-os. It has no real engagements. The function constitutions, agent assignments, and example workflows under this directory are illustrative.

If you are reading this because you have forked cortex-os and are adapting ResearchCo into your actual business, replace this Current State block with your real engagement portfolio before treating any of the function CLAUDE.md files as operational.

---

## Cascade Directive

The cascade for any work in `reference/business-example/` is:

```
cortex-os/CLAUDE.md                                  (root)
  ↳ reference/business-example/CLAUDE.md             (this file)
    ↳ reference/business-example/functions/<name>/CLAUDE.md   (function level)
```

The function CLAUDE.md refines the business rules. The business CLAUDE.md refines the root rules. The root rules are non-negotiable. If a deeper file contradicts a shallower one, the shallower one wins on the contradicted point.

If any file in the chain is missing or unwritten, flag it and halt. Do not proceed on a partial cascade.
