# MASTER_PLAN.md – ResearchCo

**ResearchCo · Multi-Phase Engagement Plan · Updated 2026-05-14**

This is a reference MASTER_PLAN.md showing the format the Session Start Protocol expects to read. The engagement and phases below are illustrative; they describe a hypothetical ResearchCo engagement, not a real one.

An operator forking cortex-os replaces this file with their own engagement plan. The file lives at the same path (business root) and follows the same structure.

---

## Active Engagement

**Client:** [Fictional reference engagement: "Project Atlas"]
**Type:** Sector intelligence report
**Started:** 2026-04-01
**Target delivery:** 2026-05-30
**Engagement lead:** [Operator]

## Plan

### Phase 1: Scoping and source library setup (complete)
**Status:** Complete (2026-04-08)
Defined the research question. Built the source library. Identified 47 primary sources, 89 secondary sources. Source credibility evaluation complete.

### Phase 2: Primary research (complete)
**Status:** Complete (2026-04-22)
Read all primary sources. Captured 312 findings to the analysis workspace. Cross-referenced. Identified 18 gaps requiring expert outreach.

### Phase 3: Expert outreach (complete)
**Status:** Complete (2026-05-02)
Interviewed 11 named industry experts. Captured interview summaries. Resolved 14 of the 18 prior gaps. The remaining 4 gaps documented as "source gap" findings.

### Phase 4: Analysis and framework selection (in progress)
**Status:** In progress (60%)
Analyst is mapping findings to the chosen framework. Confidence labels assigned to 68 of 312 findings. Draft framework selection justification under review.

**Next action:** Complete confidence labeling on remaining 244 findings. Estimated 3 sessions.

### Phase 5: Draft deliverable (not started)
**Status:** Pending Phase 4 completion
Writer produces the first draft from labeled findings. Target length: 30-page report plus 20-slide presentation.

### Phase 6: Reviewer pass and revisions (not started)
**Status:** Pending Phase 5 completion
Reviewer runs adversarial review. Findings categorized by severity. Writer addresses blockers and majors.

### Phase 7: Client delivery (not started)
**Status:** Pending Phase 6 completion
Final deliverable published to client portal. Debrief presentation scheduled.

---

## Open Questions

1. Framework selection: client has not yet confirmed whether Porter's Five Forces or a custom competitive map better fits their decision context. Pending response by 2026-05-16.

2. Confidence threshold for inclusion: working assumption is medium-or-higher findings enter the main report, low-confidence findings move to an appendix. Confirm with engagement lead before Phase 5.

3. Two source-gap findings (from Phase 3) require either additional expert outreach or explicit acknowledgment in the deliverable. Decision pending.

---

## Standing Constraints

- All work happens inside the `reference/business-example/functions/<name>/` subtree. The function constitutions are loaded as part of the cascade.
- Client data isolation: this engagement's findings live in a dedicated workspace. No cross-engagement queries.
- Reviewer agent runs with `permissionMode: deny` and never sees the development context.

---

## Format Notes for Operators Adapting This File

The structure above demonstrates the shape the Session Start Protocol expects:

1. An identification block at the top with client and timing.
2. A phased plan with explicit status per phase.
3. Open questions the operator must resolve before downstream phases.
4. Standing constraints that apply across the engagement.

Replace the placeholder content with your real engagement. Update the file at every phase transition. The Session Start Protocol reads it first on every new session.
