---
name: writing-style
description: Apply sentence-level writing rules to any prose output for a human reader. Use whenever drafting or editing content that will reach an audience, internal or external. Pairs with the post-tool-use hook for automated enforcement.
triggers:
  - draft prose
  - write a memo
  - write a report
  - draft an email
  - write a blog post
  - edit copy
  - voice review
---

# Writing Style

The writing-style skill operationalizes the AI Signature Prohibition from the root constitution. The hook layer catches what an automated scan can catch; this skill guides the upstream judgment.

## Lead with the answer

Every deliverable opens with the answer the reader is paying for. The evidence chain follows. No deliverable opens with methodology, scope, the executive summary of the executive summary, or a literary throat-clear.

Before: "In considering the question of whether we should expand into the European market, several factors come into play, including but not limited to regulatory environment, competitive intensity, and customer acquisition cost."

After: "Do not expand into Europe in 2026. Regulatory friction is the binding constraint; the next two sections show why."

## Banned vocabulary

Words that flag prose as AI-generated. Replace every instance.

`delve` → examine, study, look at
`landscape` → market, terrain, environment, context (often just remove)
`leverage` → use, apply, draw on
`robust` → strong, durable, reliable, well-tested
`utilize` → use
`streamline` → simplify, shorten, cut steps from
`spearhead` → lead, drive, run
`holistic` → complete, integrated (often just remove)
`synergy` → fit, alignment (almost always remove)
`paradigm` → model, approach, framework

## Banned phrases

`it's important to note` → just say the thing
`it's worth noting` → just say the thing
`it bears mentioning` → just say the thing
`in conclusion` → omit; the conclusion is in the last paragraph
`to summarize` → omit; the summary is the next sentence
`in summary` → omit

## Sentence-length variance

Pure AI prose has uniform medium-length sentences. Mix lengths. Short sentences carry weight. Longer ones develop. Fragments work.

Before: "The first quarter of 2026 demonstrated significant growth in the enterprise segment, with revenue increasing 23% year-over-year, driven primarily by expansion into the financial services vertical, which now represents 34% of total enterprise revenue."

After: "Q1 2026 enterprise revenue grew 23% year-over-year. Financial services drove most of it. The vertical now represents 34% of enterprise revenue, up from 19% a year ago."

## Three-part cadence

The "X, Y, and Z" pattern is fine when the content has three parts. It is an AI tell when used to pad sentences with rhythm rather than content. Audit every three-part list: do the three items each carry distinct meaning, or does one item exist to make the rhythm work?

## Em dashes

No em dashes in prose. Use commas, semicolons, periods, or en dashes. Em dashes inside code blocks are allowed because they appear in source code.

## When the rules bend

The rules bend in two cases.

First: when quoting a source verbatim. A quoted passage with an em dash stays as written.

Second: when the rule itself is the subject. Documentation explaining the AI signature prohibition contains the banned words by necessity; the exempt-paths list in the post-tool-use hook accommodates this.

In both cases, document the exemption inline so a reviewer understands why the rule is not violated.
