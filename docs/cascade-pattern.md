# The Cascade Pattern

Cortex-OS treats CLAUDE.md files as a layered configuration system. Claude Code reads them in a defined order from the filesystem; deeper files refine shallower ones. The pattern is hierarchical, not flat. Authority comes from depth.

## How the cascade resolves

When Claude Code opens a working directory, it walks up the filesystem tree collecting every CLAUDE.md it encounters. The walk stops at the repository root (typically marked by `.git/`). The collected files are loaded in order from shallowest to deepest.

For a working directory at `reference/business-example/functions/research/`, the cascade is:

```
cortex-os/CLAUDE.md                                       (root)
  ↳ reference/business-example/CLAUDE.md                  (business)
    ↳ reference/business-example/functions/research/CLAUDE.md   (function)
```

The deepest file is loaded last and conceptually wins on any point of contradiction with shallower files. The runtime walker at `runtime/cascade_walker.py` shows the resolved chain for any path.

## What each level owns

Five levels are standard. Not every deployment uses all five.

**Root.** The operator's identity, universal hard rules, and the AI signature prohibition. Everything that applies regardless of which business or function is active. Authority over all subordinate files.

**Domain.** Optional layer that separates personal work from professional work, or one business unit from another inside a larger organization. Many deployments skip this level.

**Business.** A specific business, project, or product line. Customer-facing operating principles, business-specific data governance, function map. The cortex-os reference business at `reference/business-example/` lives at this level.

**Function.** A specific operational function inside a business: research, analysis, delivery, engineering, finance. Tier-specific governance, default agent and model, halt conditions. The three function constitutions under `reference/business-example/functions/` demonstrate this level.

**Environment.** Optional bottom layer that distinguishes runtime conditions: development, staging, production. Most use cases do not need this level; it exists in the pattern for completeness.

## Refinement and contradiction

Each level can do three things relative to its parents.

Add new rules. The function level adds rules that do not exist at the business level. This is the most common case.

Refine existing rules. The function level takes a business-level rule and specializes it. A business rule like "all client deliverables ship with confidence labels" might be refined at the analysis function level into "every finding ships with one of three labels (high, medium, low) and a one-sentence rationale."

Tighten existing rules. The function level can make a business rule stricter for that function's specific context. Loosening a rule from a deeper level is not permitted by convention; the cascade is monotonically restrictive as it descends.

A literal contradiction is resolved in favor of the deeper file by Claude Code's normal precedence handling. The architectural convention is that deeper files should never need to contradict shallower files; they should refine, tighten, or add. A genuine contradiction is a sign that the rules were misplaced and should be restructured.

## Why this shape

The cascade is the answer to two questions that come up in every long-running Claude Code deployment.

Where does context live when the operator works across multiple businesses or functions? Without the cascade, the operator either pastes the same context into every session or maintains a monolithic system prompt that contains every context. The first is unreliable; the second collapses on its own weight.

How does context evolve as the operator descends into specifics? Universal rules apply everywhere. Business rules apply only in that business. Function rules apply only in that function. Putting them in one file forces an impossible compromise: too general to be useful, too specific to apply broadly. The cascade keeps each level honest by giving it a specific scope.

## Inspection

The runtime layer ships a cascade walker for verification:

```
python runtime/cascade_walker.py reference/business-example/functions/research/
```

The output lists every CLAUDE.md that would load, in order, with word counts. Use it whenever the cascade behavior is unexpected or before adding a new layer to confirm the chain resolves as intended.
