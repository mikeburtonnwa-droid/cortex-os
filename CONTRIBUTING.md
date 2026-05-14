# Contributing

Cortex-OS is open to community contributions. The standards below apply to every pull request. They exist to keep the pattern coherent and the repository defensible to a peer expert in agentic AI.

## What contributions are accepted

The repository's job is to demonstrate a pattern for AI operating systems built on Claude Code. Three kinds of contributions move that job forward:

Pattern improvements. A new hook that catches a class of failure not currently covered. A schema field that codifies a configuration concern that currently requires manual discipline. A new section in the constitutional template that addresses a gap in the existing structure.

Pattern fixes. A bug in the cascade walker, the schema validator, or any of the runtime scripts. A correctness issue in a hook script. A document that misrepresents how a layer behaves.

Documentation improvements. Clearer phrasing that does not weaken the standards. Better worked examples in the reference business. Additional per-layer references in `docs/` that go deeper on a topic the existing documentation only sketches.

Three kinds of contributions are not accepted:

Extensions to ResearchCo that do not demonstrate a new pattern element. ResearchCo's job is to demonstrate the cascade, the tiers, and the function pattern. Adding features that do not advance any of those is scope creep.

New runtime scripts that duplicate Claude Code's native functionality. The runtime layer exists for inspection and validation, not to replace what Claude Code already does well.

Identity content. The repository is intentionally generic. Operator identity content (military service, employer history, financial details) belongs in a private fork, not the public pattern.

## Contribution standards

Every pull request meets the following bar.

**Pressure-testing.** Run `python runtime/pressure_testing_harness.py --recursive .` against your branch before opening the PR. Blockers are publication-stopping. Majors must be resolved or explicitly justified in the PR description. Minors are not required to be resolved but should be acknowledged.

**No AI signatures.** Em dashes in prose, banned vocabulary, throat-clearing phrases, three-part list cadence. The AI Signature Prohibition rule in the root constitution is the canonical reference. The post-tool-use hook scans for these patterns; the pressure-testing harness re-runs the scan at the diff level. PRs that fail the scan are rejected without further review until the prose is rewritten.

**Deterministic enforcement preferred over advisory.** If you are adding a rule, prefer a hook over a constitutional addition wherever the rule has a deterministic answer. A new banned phrase belongs in `post-tool-use.sh`, not in the CLAUDE.md template. A new credential pattern belongs in `pre-tool-use.sh`, not in the data governance section. Constitutional content is for rules that require judgment.

**Schema discipline.** New configuration fields must be added to the documented schema in `docs/schema-reference.md` in the same PR that introduces them. Schema validation must pass after the addition.

**Data governance.** No credentials, no API keys, no real client data, no personal identifying information beyond the maintainer's public name and email. This applies to test fixtures, documentation examples, and code comments as much as to substantive content.

## How to propose a new pattern

Open a GitHub issue first. Pattern additions are higher-stakes than fixes; an issue prevents the PR-and-rejection cycle when the pattern does not fit.

The issue describes three things. What gap the pattern fills. Why the existing four layers do not already cover it. What the public-facing API of the new pattern would look like (new hook, new schema field, new template section, new runtime script).

A maintainer responds within a week. If the pattern fits, the issue becomes an approved scope and the PR can move forward. If the pattern does not fit but the underlying need is real, the response will name an existing layer that should absorb the concern.

Pattern PRs without a prior approved issue may be closed without review.

## Review timeline and process

Pull requests receive an initial response within seven days. Standard fixes and documentation PRs typically merge within two weeks if the standards above are met. Pattern additions may take longer because they require updates across documentation, templates, runtime scripts, and the reference business.

Reviewers apply the same standards to their own review comments. No AI-signature phrasing in PR feedback. No padding. Lead with the verdict; evidence follows.

## License

By contributing, you agree your contribution is licensed under the MIT License that covers the repository. See LICENSE.
