# Data Governance

The canonical reference for data governance rules. Public repositories, private forks, and operator-specific deployments all observe the same bar; what changes is the scope of "sensitive."

## The bar

Never include sensitive data in any output intended for version control or external sharing. Flag when a task requires data that should not leave a secure context. Treat all proprietary methodology, pricing, scoring logic, and client data as confidential at all times.

## What is sensitive

Five categories.

Credentials. API keys, access tokens, OAuth secrets, database connection strings, SSH keys, private keys of any kind. Never written to a file under version control. Never pasted into a public artifact.

Personal identifying information. Real names beyond the operator's public name, real email addresses beyond the operator's public address, phone numbers, home addresses, dates of birth, government identifiers. The public-name carve-out applies only to the maintainer's own published identity; all other names get redacted.

Proprietary methodology. Internal scoring logic, internal frameworks, internal pricing models, internal data schemas that would help a competitor replicate the operator's work. The methodology lives in the private fork; the public repo describes the pattern in generic terms.

Client data. Anything an operator learned through a client engagement. Client names, deal sizes, internal documents, meeting notes. This is non-negotiable; client confidentiality has no expiration date and no aggregation exception.

Operational secrets. Tradecraft details, security configurations, system internals that would give an attacker an advantage. Generalize to public-level abstractions if the topic must be discussed at all.

## Enforcement layers

Three layers catch sensitive data before it reaches version control.

The pre-tool-use hook scans tool input for credential patterns (AWS keys, private key headers, common environment variable names with credential keywords nearby). Blocks the tool call before the model can write to disk.

The pressure-testing harness includes a credential scan in its commit-time gate. Re-runs the same patterns plus operator-specific patterns configured per-deployment.

The git pre-commit hook (operator-installed, not Claude Code) runs the same scan once more before commit. Belt and suspenders.

These three layers are deterministic. The constitutional rule above is advisory. Both are required.

## Public-repo audit

Every commit to a public repository passes a data governance audit before push.

Audit criteria:

1. No credentials of any kind.
2. No personal identifying details beyond the operator's published identity.
3. No proprietary methodology from any organization the operator has worked with.
4. No client names, deal information, or engagement specifics.
5. No private session artifacts, commit logs from non-public sources, or debugging history from private forks.

A draft commit that fails any criterion is rejected. The file is rewritten or removed. The audit re-runs.

## Private-fork audit

A private fork relaxes some of the public-repo constraints. The operator's real Current Reality block lives here. Their real engagements and clients. Their real proprietary methodology if they choose to encode it.

Private forks still observe:

1. No credentials in files under git tracking. Use environment variables and a gitignored `.env` instead.
2. No PII for third parties without their consent.
3. Operator-specific data governance rules added to this file or to a fork-specific extension.

The boundary between public and private is the audit bar above. Crossing the boundary in either direction requires a deliberate review.

## Operator extensions

Operators extending these rules for their own context add their content as appendices below this section, in their private fork. The public version of this file stays generic.

Common extensions:

- Specific company names that should be redacted from any public artifact
- Specific project codenames that are confidential
- Specific clients whose engagement existence is itself confidential
- Industry-specific compliance requirements (HIPAA, FERPA, GDPR, etc.)

The extension lives below this line in the operator's private fork. The public file stops here.
