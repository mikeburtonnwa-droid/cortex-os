# CLAUDE.md – ResearchCo Delivery Function
**ResearchCo · Delivery Function (Tier 3) · v1.0 · 2026-05-14**

---

## What This Function Does

The delivery function produces client-facing artifacts from the analyst's structured findings: written reports, presentation decks, debrief summaries, executive memos. The function is throughput-oriented. The hard quality work has already happened upstream; delivery's job is to render the analysis cleanly for the audience.

Tier 3 governance applies. Light enforcement, high throughput, but the three quality gates from the business constitution still apply at the artifact level before any client sees anything.

---

## Default Agent and Model

The writer agent at `reference/agents/writer.md` is the default for this function. The agent specifies `model: sonnet` because writing under voice constraints is well-served by the sonnet capability tier at this cost point. The function does not override.

For high-volume rendering tasks (generating slide titles, formatting tables, copy-editing for length), the orchestrator may dispatch to haiku. The writer's primary work remains sonnet.

---

## Tier 3 Governance Rules

These rules apply in addition to the business-level operating principles.

1. **Lead with the answer.** Every external deliverable opens with the answer the client is paying for. The evidence chain follows. No deliverable opens with the methodology, the engagement scope, or the executive summary of the executive summary.

2. **No invented framings.** The deliverable presents the analyst's findings using the framework the analyst chose. The writer does not introduce new frameworks at delivery time; that is analysis work and belongs upstream.

3. **Audience awareness without audience flattery.** Client deliverables address the reader's role and interests. They do not soften findings to manage feelings. A client paid for what the analysis says.

4. **Length is a cost, not a virtue.** Every page in a deliverable earns its place. Pages that summarize content the reader will read on the next page are removed.

---

## Hooks Configured for This Function

All four base hooks apply. The post-tool-use hook is the central enforcement mechanism for this function: every Write or Edit on a deliverable triggers the AI signature scan. Failed scans return the artifact to the writer with the specific corrections.

The pre-tool-use hook enforces the `publish_to_client_portal` approval requirement. The writer cannot publish without explicit operator approval, even if the artifact has passed all upstream gates.

---

## When the Function Halts

The delivery function halts and escalates to the operator in three cases.

Failed quality gate. If the artifact fails any of the three gates (source, pressure-testing, voice), delivery halts and the artifact returns to the relevant upstream function.

Audience mismatch flagged. If the writer assesses that the analyst's findings, presented as written, will not land with the client audience, delivery halts and the writer surfaces the mismatch to the operator before adapting the content.

Publication request without approval. The pre-tool-use hook blocks unapproved publications. If the writer attempts a publish, the operator is the explicit go-no-go authority.

---

## Cascade Directive

The cascade resolved at this directory is:

```
cortex-os/CLAUDE.md                                  (root)
  ↳ reference/business-example/CLAUDE.md             (business)
    ↳ reference/business-example/functions/delivery/CLAUDE.md   (this file)
```

This file refines the business rules. It does not weaken them.
