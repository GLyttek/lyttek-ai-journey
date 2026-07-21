# Secure Agent Control Plane

*A practical architecture note for systems in which a model can propose actions but must not authorize itself.*

## The boundary that matters

A language model is useful for interpretation, planning and generation. Those same qualities make it a poor policy-enforcement point. Its output is probabilistic, its context may contain untrusted material, and its plan can change after a failed tool call.

The sustainable design is therefore not “make the model obey harder.” It is:

> Let the model propose. Let a deterministic control plane decide what data, tool, destination and effect are allowed.

This is defense in depth, not a promise that prompt injection can be solved completely.

## Five zones

```text
untrusted sources
       |
       v
context admission -- provenance, trust, parsing, size
       |
       v
model planning ---- no credentials, no self-approval
       |
       v
policy broker ----- actor, action, target, data, expiry
       |
       v
bounded execution - scoped identity, path, network, rate
       |
       v
verification ------ observed effect, receipt, rollback
```

### 1. Context admission

Treat user text, web pages, email, repository content, tool descriptions, images and results from other agents as data. Preserve source and trust level. Restrict active rendering. Do not let retrieved text grant tools, change policy or write durable memory without a separate check.

### 2. Model planning

The model can choose among tools already admitted for the task and prepare normalized parameters. It does not receive broad credentials and it does not decide whether its own call is authorized.

### 3. Policy broker

The broker evaluates an explicit action contract:

```text
actor
agent_run
operation
target
parameters
data_class_in
data_class_out
destination
risk_tier
approval_id
expiry
expected_effect
verification
```

The natural-language justification may help a reviewer. It is not permission.

### 4. Bounded execution

Execution uses a task-bound identity and the smallest necessary filesystem, process and network rights. The host injects authentication after policy approval; credentials do not enter model context.

A sandbox without network policy contains compute. It does not necessarily contain data. If an agent can read private material and reach an external destination, the architecture still has an egress problem.

### 5. Verification

A model saying “done” proves only that the model generated that sentence. Consequential workflows need read-back from the target system, a deterministic test, an artifact hash, a deployment health check or another signal tied to the real effect.

## Mandatory control points

| Effect | External control | Evidence |
|---|---|---|
| Read data | actor, purpose, resource and data class | access decision |
| Write memory | provenance, isolation, retention and conflict policy | memory diff |
| Call a tool | allowlisted operation and normalized parameters | policy result |
| Use a secret | brokered task credential | credential reference, not value |
| Send data | destination, data class, protocol and volume | egress decision |
| Change code | path, branch and diff limits | diff and tests |
| Publish/deploy | exact artifact, environment and approval | hash and read-back |
| Delete/change rights | step-up, single-use authorization | non-replayable record |

Fail closed when authorization, approval lookup or audit logging is unavailable for high-impact actions.

## Memory and rendering are execution surfaces

Persistent memory can carry a poisoned claim into later runs. Rich Markdown, HTML and images can trigger remote loading, unsafe links or misleading visual states. Both need policy:

- isolate memory by user and project;
- record source, author, confidence and expiry;
- review writes to identity, policy and tool instructions;
- support correction, deletion and rollback;
- render untrusted content inert by default;
- treat links and hidden content as data, not consent.

## Operating modes

- **Observe:** approved reads, no side effects.
- **Draft:** isolated new artifacts, no publication.
- **Change:** scoped writes with diff, tests and review.
- **Execute:** bounded operational calls through policy.
- **Publish/deploy:** exact approval, artifact identity and post-effect verification.

A workflow can move through several modes. The approval for research does not silently authorize publication.

## What to test

1. Untrusted content asks the model to ignore policy.
2. A failed tool call causes a broader alternative plan.
3. Tool output contains malformed or active content.
4. The agent has private data, untrusted input and egress at the same time.
5. A memory write affects a later session.
6. An approval is expired or bound to another target.
7. Policy or audit service is unavailable.
8. The target effect differs from the model's report.
9. Revocation and rollback actually stop or reverse the workflow.

## Evidence boundary

This note is an architecture recommendation. It does not demonstrate that a specific agent framework implements these controls or that isolation is complete. Inspect the real host, credentials, network, tool schemas and deployment path.

## References

- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [MCP Client Best Practices](https://modelcontextprotocol.io/docs/develop/clients/client-best-practices)
- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final)
