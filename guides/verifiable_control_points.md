# Verifiable Control Points for Agent Workflows

A guardrail is useful only when we can say where it runs, what it observes, what it blocks and which evidence shows that it worked.

This guide turns broad principles into checkpoints around a real workflow.

## The control-point contract

Every control should name:

```text
trigger
input
policy or invariant
external enforcement component
allow / deny / escalate result
evidence emitted
failure behavior
owner
version
```

“Human in the loop” is incomplete until the exact action, data, target and reviewer authority are known.

## Checkpoints

### 1. Task admission

**Question:** Is the requested outcome inside the user's authority and the system's purpose?

**Control:** authenticated requester, bounded task contract, data and action classification.

**Evidence:** task ID, owner, allowed scope, denied scope, policy version.

### 2. Context admission

**Question:** Which sources may influence planning?

**Control:** provenance, trust label, parser, size, freshness and disclosure checks.

**Evidence:** admitted source IDs and rejected-source reasons.

### 3. Tool exposure

**Question:** Which capabilities does this task need?

**Control:** task-scoped allowlist and progressive discovery.

**Evidence:** server/tool catalog and granted scopes.

### 4. Plan-to-call translation

**Question:** Does the proposed call preserve the approved meaning?

**Control:** normalized operation, target, parameters, data classes and destination.

**Evidence:** action contract and policy decision.

### 5. Credential use

**Question:** Which identity performs the effect?

**Control:** brokered task credential, audience and expiry.

**Evidence:** credential reference and scope, never the secret value.

### 6. Data egress

**Question:** May this data leave for this destination?

**Control:** destination and protocol allowlist, data-class policy, volume and rate limit.

**Evidence:** egress decision and transfer metadata.

### 7. Commit-time authorization

**Question:** Is the exact effect still permitted now?

**Control:** bind approval to actor, operation, target, normalized parameters, artifact/state hash, expiry and single-use status.

**Evidence:** approval ID and replay-protected validation.

### 8. Execution

**Question:** Can the effect escape its intended boundary?

**Control:** filesystem, process, network, resource and time limits; idempotency where possible.

**Evidence:** execution trace and bounded result.

### 9. Verification

**Question:** Did the target system reach the intended state?

**Control:** independent read-back, test, hash, API query or health check.

**Evidence:** verifier, observation and pass/fail result.

### 10. Closure

**Question:** Can the action be explained, reversed and learned from?

**Control:** receipt, rollback status, retained uncertainty, incident trigger and memory policy.

**Evidence:** closed trace linked from intent to outcome.

## Example trace

```json
{"event":"task_admitted","task":"T-42","scope":"draft-docs","policy":"p7"}
{"event":"tool_allowed","task":"T-42","tool":"file.write","target":"docs/"}
{"event":"change_created","task":"T-42","artifact":"sha256:…"}
{"event":"publish_denied","task":"T-42","reason":"scope_missing"}
```

The example is deliberately incomplete. A production schema should add actor identity, timestamps, normalized parameters, data classes and verification while avoiding sensitive payloads.

## Test the controls, not the prose

For each checkpoint, create at least one allow case, one deny case and one unavailable-control case.

Examples:

- context source has no provenance;
- model requests a tool outside the catalog;
- destination changes after approval;
- artifact changes between review and deploy;
- approval is replayed;
- audit service is unavailable;
- model reports success but read-back fails;
- rollback token has expired.

## Evidence levels

- **Declared:** documentation says the control exists.
- **Configured:** a policy or setting can be inspected.
- **Tested:** a controlled case proves allow and deny behavior.
- **Observed:** a real run emitted the expected evidence.
- **Exercised:** failure, revocation and rollback were tested.

Do not call a control operational when evidence remains at the declared level.

## Maintenance

Re-test affected checkpoints when the model, prompt, tool schema, MCP server, memory policy, identity provider, network, deployment path or data classification changes.

## Evidence boundary

A checklist can reveal missing proof. It cannot replace environment-specific testing, and a complete trace does not by itself prove that the policy was correct.

## References

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
