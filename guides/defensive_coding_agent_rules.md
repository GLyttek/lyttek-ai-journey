# Defensive Rules for Coding Agents

Repository instructions can make a coding agent more consistent. They are not a security boundary. Use them to state intent and required evidence, then enforce the important parts through permissions, branch protection, CI and deployment policy.

## Responsibility

The human or organization operating the system remains responsible for the change. The agent must not present generated code, a clean diff or its own review as proof of safety.

## Repository rule set

The following rules are designed to be adapted to a repository's language, framework and threat model.

### Scope

1. Read repository governance and the exact task before editing.
2. List intended files, security surfaces and non-goals.
3. Stop when the required change expands to another service, data class, destination or deployment environment.
4. Do not make drive-by refactors or dependency upgrades.
5. Work in an isolated branch or worktree.

### Secrets and sensitive data

1. Never write credentials, private keys, tokens or personal data into code, tests, logs, examples or prompts.
2. Do not inspect secret values when presence, path or metadata is enough.
3. Use the repository's approved secret broker or placeholder convention.
4. Treat generated logs and error messages as potential disclosure paths.

### Dependencies and supply chain

1. Do not add a package merely to avoid a small implementation.
2. Verify that the dependency exists, is maintained, licensed appropriately and compatible with the project.
3. Pin actions, images and build inputs according to repository policy.
4. Record why the dependency is needed and who will maintain it.
5. Never execute install scripts from an unreviewed source.

### Input, output and authorization

1. Treat every external input as untrusted.
2. Validate structure, length, type and allowed values at the boundary.
3. Encode output for its actual sink.
4. Enforce authorization server-side for every object and state transition.
5. Add negative tests for another user, tenant, role or object identifier.
6. Fail closed for missing policy, identity or security-relevant audit logging.

### Files, parsers and commands

1. Normalize and constrain paths to an approved root.
2. Reject traversal, unexpected links and unsafe archive entries.
3. Avoid shell composition when a typed API exists.
4. Do not deserialize untrusted objects with unsafe formats.
5. Bound file size, recursion, memory and processing time.

### Cryptography and authentication

1. Use maintained high-level libraries and approved algorithms.
2. Do not invent encryption or password-storage schemes.
3. Use constant-time comparison where secret-dependent timing matters.
4. Preserve secure cookie, token expiry, rotation and revocation behavior.
5. Escalate all authentication, authorization, identity and key changes to the highest review tier.

### Errors and logging

1. Handle errors explicitly and preserve a safe failure state.
2. Do not leak internals, credentials or personal data.
3. Log security-relevant decisions with structured identifiers.
4. Do not log full prompts or tool payloads by default.
5. Ensure that monitoring failure does not silently permit high-impact actions.

### Testing and evidence

1. Add or update deterministic functional tests.
2. Add negative and abuse cases for touched trust boundaries.
3. Run the repository's real tests, linters and scanners.
4. Report actual command output, failures and skipped checks.
5. Distinguish pre-existing findings from newly introduced ones.
6. Verify the target behavior after deployment or publication when in scope.

## Risk routing

Escalate automatically when a change touches:

- authentication, authorization, sessions or tokens;
- secrets, cryptography or identity;
- tenant boundaries or regulated data;
- parsers, uploads, paths, archives or template rendering;
- shell execution, dynamic code or deserialization;
- network egress, external publication or webhooks;
- dependencies, build scripts, CI/CD or production infrastructure;
- destructive state or privilege changes.

The agent can propose the tier. Repository policy decides the required checks and reviewers.

## Independent review packet

A coding agent should hand the reviewer:

```text
intent and non-goals
proposed risk tier and triggers
changed files and external dependencies
data-flow and permission changes
tests and scanners actually run
negative cases added
open uncertainty and skipped checks
rollback and post-change verification
```

Use a fresh review context for material changes. A model reviewing its own full conversation can inherit the same assumptions that produced the defect.

## Enforcement map

| Rule | Reliable enforcement |
|---|---|
| path boundary | sandbox/worktree and file broker |
| no secret access | process environment and credential broker |
| required tests | CI and branch protection |
| dependency policy | lockfile, allowlist and SCA |
| reviewer eligibility | repository permissions |
| no autonomous deploy | deployment policy and environment protection |
| exact external effect | action-bound approval and read-back |

## Evidence boundary

These instructions reduce omission and make review easier. They do not demonstrate that generated code is secure, and they must be tailored to the repository's language, framework and threat model.

## References

- [OpenSSF Security-Focused Guide for AI Code Assistant Instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions.html)
- [NIST SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final)
- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- [CISA Secure by Design](https://www.cisa.gov/securebydesign)
- [OWASP Secure Coding with AI Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html)
