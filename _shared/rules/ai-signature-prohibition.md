# AI Signature Prohibition

The canonical reference for the AI Signature Prohibition rule. The post-tool-use hook references this file in its block message when an output fails the signature scan.

## The rule

Output that reads as AI-generated is rewritten until it does not.

Three sub-rules operationalize the principle.

## Banned vocabulary

The following words mark prose as AI-generated. Replace every instance.

`delve`, `landscape`, `leverage` (and `leverages`, `leveraging`), `robust`, `utilize` (and `utilizes`, `utilizing`), `streamline` (and `streamlines`), `spearhead`, `holistic`, `synergy`, `paradigm`.

Substitutions are context-dependent. Suggested defaults:

- delve → examine, look at, study
- landscape → market, environment, terrain (often omit)
- leverage → use, apply, draw on
- robust → strong, durable, reliable, well-tested
- utilize → use
- streamline → simplify, cut steps from
- spearhead → lead, drive, run
- holistic → complete (often omit)
- synergy → fit, alignment (almost always omit)
- paradigm → model, approach, framework

## Banned phrases

The following phrases function as throat-clearing. Remove them and state the underlying claim directly.

`it's important to note that <X>` → just say X
`it's worth noting that <X>` → just say X
`it bears mentioning that <X>` → just say X
`in conclusion, <X>` → omit "in conclusion"; X is the conclusion
`to summarize, <X>` → omit "to summarize"; X is the summary
`in summary, <X>` → omit "in summary"

## Em dashes

No em dashes in prose. Use commas, semicolons, periods, or en dashes.

Em dashes inside fenced code blocks are allowed because they may appear in source code or shell output.

## Three-part cadence

The pattern "X, Y, and Z" inside a single sentence is fine when the content has three distinct parts. It is an AI tell when used to pad sentences with rhythm rather than content.

Self-audit: for every three-part list, ask whether each item carries distinct meaning. If one item exists to make the rhythm work, cut it.

## Sentence-length variance

Pure AI prose has uniform medium-length sentences. Vary length deliberately. Short sentences carry weight. Longer ones develop a point. Fragments work.

## Exempt files

Files that quote the banned words as the subject of the rule itself are exempt from the scan. The current exempt list lives in `_shared/.claude/hooks/post-tool-use.sh` and includes:

- `_template/CLAUDE.md`
- `_shared/rules/ai-signature-prohibition.md` (this file)
- `_shared/rules/communication-style.md`
- `docs/hooks-layer.md`
- `docs/schema-reference.md`

When adding new rule documentation that quotes the banned terms, add the new file to the hook's exempt list.

## Enforcement

The post-tool-use hook scans every Write and Edit against this rule and blocks violations with feedback. The pressure-testing harness re-runs the scan at commit time. The stop hook re-runs the scan against the final assistant message.

Three layers of enforcement for one rule. The redundancy is intentional. The model under context pressure forgets; the hooks do not.
