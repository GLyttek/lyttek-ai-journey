# API Security by Design for AI-Assisted Development

An AI coding assistant can accelerate implementation and review. It cannot infer the organization's authorization model from endpoint names, schemas and happy-path tests alone.

The useful shift is to make security intent inspectable before code generation.

## Start with an access model

For each resource, record:

| Question | Example answer |
|---|---|
| Actors | customer, tenant admin, support analyst, service account |
| Resource | report, invoice, case, user profile |
| Relationship | owner, member of tenant, assigned analyst |
| Operation | create, read, update, delete, export, share |
| State condition | draft only, approved, locked, expired |
| Field boundary | public fields, internal notes, regulated attributes |
| Tenant boundary | same tenant only, explicit cross-tenant exception |
| Evidence | authorization decision and audit event |

A route such as `GET /reports/{id}` describes transport. It does not answer who may read which report.

## Authorization matrix

```text
actor × resource × relationship × operation × state × tenant
```

Write the matrix in a format that humans can review and tests can consume. The model may help generate candidate cases, but business and security owners approve the meaning.

## Negative tests are first-class requirements

For every allowed path, include denied paths:

- authenticated user requests another user's object;
- member of one tenant supplies an identifier from another tenant;
- lower role calls an administrative function;
- actor replays an operation after role or ownership changes;
- user changes a field that was not intended for mass assignment;
- export reveals fields not present in the normal view;
- object state no longer permits the transition;
- cached or background access uses stale authorization.

BOLA/IDOR is not fixed by hiding identifiers. The server validates the actor's relationship to the requested object on every call.

## Design packet for an AI coding agent

Provide:

```text
API purpose and non-goals
actors and trust boundaries
resource and relationship model
data classification by field
allowed and denied state transitions
authorization matrix
rate and abuse constraints
audit requirements
error-disclosure policy
negative test inventory
```

Without this packet, the agent will often imitate neighboring code. That may be useful for consistency and still reproduce a flawed authorization assumption.

## Security controls by lifecycle

### Design

- threat model actors, assets, boundaries and misuse cases;
- classify data and external destinations;
- define server-side authorization and state transitions;
- choose safe defaults and failure behavior;
- define audit events without sensitive payloads.

### Implementation

- validate type, format, length and allowed values;
- bind data access to authenticated actor and tenant;
- use allowlists for writable fields;
- centralize authorization policy where practical;
- avoid unsafe deserialization and dynamic query construction;
- use maintained security libraries.

### Verification

- run functional and negative authorization tests;
- use SAST, SCA and API testing where relevant;
- test rate, size, timeout and resource limits;
- verify logs and alerts;
- test policy failure and stale identity;
- review generated code independently.

### Release and operation

- protect deployment with artifact and environment gates;
- stage changes and preserve rollback;
- monitor denied calls, unusual object enumeration and privilege use;
- reassess after schema, identity, provider or dependency changes;
- maintain vulnerability handling and retirement plans.

## Compliance boundary

Code can implement technical controls that support compliance. An AI assistant cannot make an API compliant by generating annotations, policies or tests. Compliance depends on applicable law, organizational process, data handling, evidence and effective operation over time.

Treat generated compliance mappings as review leads. Verify them against the actual obligation and system.

## Review checklist

- [ ] actors, resources, relationships and tenants explicit
- [ ] field-level data classes recorded
- [ ] every operation has server-side authorization
- [ ] state transitions and forbidden transitions defined
- [ ] negative tests cover other user, tenant, role and object
- [ ] writable fields are allowlisted
- [ ] rate, size and abuse limits exist
- [ ] errors do not disclose sensitive internals
- [ ] audit events support investigation without leaking data
- [ ] external destinations and egress are controlled
- [ ] deployment and rollback are independently gated
- [ ] compliance claims are attributed and reviewed

## Evidence boundary

This checklist supports design and review. It is not an API penetration test, legal opinion or certification. Implementation needs testing against the actual identity, data store, gateway and deployment environment.

## References

- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [NIST SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final)
- [CISA Secure by Design](https://www.cisa.gov/securebydesign)
