# 06 - AI Agents Training: Reliability Means Showing the Boundary

> **Status:** Training notes from February 2026, revised in July 2026 after reviewing the claims against later operating experience. The linked video remains a historical recording and cannot carry these corrections retroactively. This material is not legal advice.

> **Video:** [Original training recording on YouTube](https://youtu.be/64qeuW15J8g)

## What I was trying to teach

The training began with two recurring failures.

The first was unsupported output: a model produced an answer that sounded complete but could not be defended. The second was the intent gap: a person gave a short instruction and the system filled in missing scope on its own.

I initially presented five “pillars of reliability.” That language implied a settled framework. What I had was a toolbox. Each technique can reduce one class of failure while leaving others untouched.

## Five tools, each with a failure mode

### Retrieval

Retrieval-augmented generation can place selected documents beside a question:

```text
question → retrieve documents → generate answer → retain citations
```

This can improve grounding. It does not prove that the right document was indexed, retrieved, current, or interpreted faithfully. A citation is useful only when it supports the nearby claim.

### Claim checking

A verification pass can extract factual claims, seek independent evidence, and revise unsupported sentences:

```text
candidate answer
    → list checkable claims
    → inspect independent sources or tests
    → revise with evidence and uncertainty
```

The old text said that Chain of Verification “validates the output.” That was too strong. A second model can repeat the first model's mistake, invent a source, or fail to identify the important claim. The method creates another opportunity to detect error; it is not a certificate.

### Repeated sampling

Generating several answers can reveal instability. If answers diverge, the task or prompt may be underspecified. If they converge, confidence may increase for a narrowly evaluated task.

Agreement is not truth. Related models can reproduce the same learned error, and repeated calls increase cost and latency.

### Multiple reviewers

Different models or prompts can play generator, critic, and adjudicator roles. This is useful when disagreement is captured and resolved against a rubric.

Model count alone does not create independence. A council can turn one unsupported answer into three polished versions of the same assumption.

### Deterministic tests and bounded effects

The most important addition from later practice was not another model. It was ordinary software control:

- schema validation;
- unit and integration tests;
- source and destination allowlists;
- filesystem and tool permission limits;
- dry runs and diffs;
- explicit approval before irreversible or external effects.

Language models are most useful where interpretation is required. Deterministic code should enforce the boundary where it can.

## Intent must survive translation into action

“Delete old files” is not an executable requirement. The agent still needs to know which directory, what “old” means, whether symlinks count, what must be retained, and whether a backup is required.

For consequential work, I now prefer a small intent artifact:

```yaml
action: archive
scope: /approved/input/path
selection: modified_before_2025-01-01
excluded:
  - legal-hold
  - active-projects
preview_required: true
approval_required: true
```

The artifact does not eliminate ambiguity, but it makes assumptions reviewable before a tool acts.

## Validation is a design, not a final model call

The original maturity model suggested a progression from humans validating everything toward AI validating almost everything. That can become a story of automation for its own sake.

A better progression is based on consequence and evidence:

| Stage | What changes |
|---|---|
| Observe | Record inputs, outputs, tool calls, and failures without granting new authority |
| Assist | Let models flag issues; humans inspect the evidence and effect |
| Bound | Automate reversible actions inside tested permissions and budgets |
| Evaluate | Measure task errors, missed detections, false alarms, and recovery behavior |
| Expand selectively | Increase authority only for cases whose failure cost and controls are understood |

Some workflows should remain human decisions even if the model becomes more accurate. The goal is not maximum autonomy. It is appropriate autonomy.

## A practical risk boundary

| Consequence | Default control | Examples |
|---|---|---|
| High | Strong authentication, explicit approval, exact effect preview | Delete data, publish, transfer funds, change access |
| Medium | Isolated execution, tests, diff, human review | Code changes, configuration, drafted external messages |
| Low and reversible | Bounded automation, logging, sampled review | Read-only collection from approved public sources |

Risk depends on data sensitivity, permissions, reversibility, and destination. “Summarize” is not automatically low risk if the input is private or the output is sent externally.

## Threats worth teaching without theatre

The old material used labels such as “AI kill chain” and listed six dramatic attack vectors. The practical risks are easier to understand in ordinary language:

- untrusted content can be mistaken for an instruction;
- a useful tool can have more permission than the task requires;
- generated parameters can point to the wrong file, account, or destination;
- hidden state and silent fallback can obscure what actually ran;
- one agent can pass malicious or unsupported material to another;
- logs can leak the sensitive content they were meant to protect;
- configuration changes can quietly widen authority.

The response is not a magic prompt. It is isolation, least privilege, typed interfaces, validation, approval, logging, and recovery testing.

## EU rules: applicability comes before slogans

Four legal frameworks may matter, depending on the organization, role, sector, data, and intended use:

| Framework | Operational question | Status as of July 2026 |
|---|---|---|
| EU AI Act | What is the system's intended purpose, operator role, and risk category? | Entered into force in 2024; application is phased. Most remaining provisions are scheduled for 2 August 2026, with exceptions. |
| GDPR | Does the workflow process personal data, and on what lawful basis? | Applicable. |
| NIS2 | Is the organization within national implementing law, and what security duties apply? | EU transposition deadline was 17 October 2024; national implementation must be checked. |
| DORA | Is the organization or ICT relationship within the financial-sector regime? | Applies from 17 January 2025. |

Primary references:

- [European Commission — AI Act overview and application timeline](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [EUR-Lex — NIS2 Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng)
- [EUR-Lex — DORA Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj/eng)

A generic label such as “internal agent” or “business automation” does not establish compliance. Where classification or obligations matter, obtain qualified legal or compliance review.

## A 30-day experiment, not a rollout promise

A useful first month can stay deliberately small:

1. choose one reversible workflow and write its failure conditions;
2. build a representative evaluation set before changing authority;
3. add provenance, logs, budgets, and an approval boundary;
4. run a pilot, inspect failures, and decide whether the workflow deserves expansion.

The evidence from the pilot should decide the next step. A calendar should not.

## What I would teach now

- Retrieval can ground an answer; it cannot guarantee one.
- Verification requires independent evidence or executable tests where possible.
- Human review needs sources, uncertainty, and an exact effect—not just polished prose.
- Friction is useful when it protects a meaningful boundary.
- Trust should be attached to a tested workflow, not to a model name.

---

*Based on internal training material from February 2026; corrected in July 2026.*
