---
name: citation-discipline
description: Apply rigorous citation format and source evaluation when producing research output. Use whenever the deliverable contains claims sourced from external evidence. Pairs with the researcher agent's primary workflow.
triggers:
  - research findings
  - cite sources
  - source evaluation
  - bibliography
  - reference list
  - fact-check
---

# Citation Discipline

Every claim in a research output traces to a source. The source is named, dated, and addressable. Without these properties, the claim is not a finding.

## Citation format

In-line citations use the format `[Source name, Year]` for prose flow.

In-line citations use the format `[1]` `[2]` `[3]` with a numbered reference list at the end when density requires it.

A reference list entry includes: author or organization, title, publication, year, URL when available, date accessed when the source is web-based.

Example:

```
[1] McKinsey Global Institute. "The state of AI in 2024."
    McKinsey Quarterly, June 2024. https://www.mckinsey.com/...
    Accessed 2026-05-14.
```

The exact format matters less than the addressability. A reader who wants to verify a claim should be able to retrieve the source from the citation.

## Source credibility

Evaluate every source against five criteria before treating it as authoritative.

Author or organization. Named, with credentials or institutional affiliation. Anonymous web content is a lead, not a source.

Publication or venue. Peer-reviewed for academic claims. Trade publications for industry claims. Institutional reports for sector data. Press releases for company-specific facts; not for sector analysis.

Date. Sources older than two years for fast-moving topics (AI, crypto, geopolitics) carry reduced weight. Note the date explicitly in the citation.

Methodology, when quantitative. Survey sample size and methodology. Data collection date. Statistical significance. A "Forbes article citing a study" is two sources removed from the primary data; track to the primary.

Independent confirmation. A claim that appears in one source is a lead. A claim that appears in three independent sources is a finding. Common-cause sources (three articles all citing the same study) count as one source.

## Primary vs. secondary

Primary sources contain original data, original analysis, or first-hand reporting. A government statistical release. A company's filing. A research paper presenting new results.

Secondary sources interpret or aggregate primary sources. A news article summarizing a study. A consultancy report citing government data.

Default to primary. Use secondary only when primary is inaccessible or when the secondary adds analytical value the primary lacks. When using secondary, name both the secondary and the underlying primary in the citation.

## Date sensitivity

Some claims age faster than others.

Slow-aging: mathematical results, historical facts, geographic data. A 1995 source on a 1990 event is still usable.

Medium-aging: market sizing, demographic data, regulatory frameworks. Sources older than three to five years carry reduced confidence; replace if newer is available.

Fast-aging: AI capabilities, tooling landscapes, crypto markets, geopolitical positions. Sources older than twelve months may be obsolete. Sources older than six months should be treated with caution.

The researcher records the source date and flags age explicitly in the structured output. Downstream agents apply the staleness judgment.

## Anonymous content

Anonymous web content (Reddit threads, unattributed blog posts, AI-generated summaries) is a lead, never a source. A claim that originates in anonymous content does not reach a deliverable until it has been confirmed by a named source.

The exception: anonymous content is the topic of the analysis. Reddit sentiment analysis legitimately cites Reddit threads as primary data because the threads are the subject.

## Failed lookups are findings

If the research question cannot be answered with available sources, that fact is a finding. It ships in the structured output as "source gap: this dimension uncovered." It does not silently disappear.

A research output that elides gaps is worse than one that acknowledges them. The operator needs to know what is uncertain.

## Hallucination prevention

Never invent a citation. If a source is paywalled, inaccessible, or unverified, that fact is part of the output, not a reason to construct a citation that looks plausible.

The most common hallucination failure: the model produces a citation in the correct format with a plausible author, title, and journal, but the source does not exist. Verify every citation against its URL before treating the source as confirmed.
