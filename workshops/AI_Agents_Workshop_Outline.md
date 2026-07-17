# AI Agents Workshop: Designing Bounded, Verifiable Workflows

> **Status:** Public outline derived from a February 2026 training, revised in July 2026. The original [video recording](https://youtu.be/64qeuW15J8g) remains a historical artifact and may contain claims corrected here. This outline is not legal advice or a complete workshop package.

**Format:** Half-day, 4 hours

**Audience:** Technical leads, developers, architects, and security practitioners

**Prerequisites:** Basic familiarity with LLM APIs and software workflows

## Purpose

This workshop does not teach participants how to make an agent “trustworthy” through prompting. It teaches them how to expose uncertainty, constrain authority, and collect evidence around one workflow.

By the end, participants should be able to:

1. turn a vague agent idea into a bounded action and failure model;
2. distinguish retrieval, model review, and executable verification;
3. identify where untrusted data can become control input;
4. choose approval, isolation, logging, and recovery controls by consequence;
5. draft a small evaluation plan before increasing autonomy;
6. recognize when legal or compliance classification requires qualified review.

## Half-day agenda

The four-hour format consists of a 15-minute opening, four 45-minute modules, 20 minutes of breaks, and a 25-minute close.

### Module 1 — From fluent answer to checkable claim

**Question:** What can the workflow actually prove?

Participants compare four mechanisms:

- retrieval supplies selected context;
- citation links a sentence to a source;
- a second model critiques a candidate answer;
- deterministic tests check properties that can be encoded.

**Demonstration:** A sourced answer containing a claim not supported by its citation.

**Exercise:** Extract the checkable claims, assign an evidence type to each, and mark what remains interpretation.

**Output:** A claim–evidence table, not a generic “verification strategy.”

### Module 2 — Translating intent without inventing scope

**Question:** What decisions are hidden inside a short instruction?

The working example is “delete old files.” Participants identify directory, age rule, exclusions, backup, symlinks, preview, rollback, and authorization.

**Demonstration:** Convert a sentence into a typed intent artifact and dry-run output.

**Exercise:** Write an artifact for one participant workflow and have another participant attack its ambiguity.

**Output:** A revised intent artifact with explicit unresolved questions.

### Module 3 — Treating content as data and tools as authority

**Question:** Where can an attacker or accident change behavior?

The module covers:

- indirect prompt injection in pages, documents, and transcripts;
- excessive filesystem, network, account, or publishing permission;
- unsafe destinations and generated tool arguments;
- agent-to-agent propagation of unsupported material;
- sensitive data copied into prompts or logs;
- silent fallback and configuration drift.

**Demonstration:** An untrusted document requests a tool action. Prompt delimiters flag the boundary but do not enforce it; a typed tool policy rejects the effect.

**Exercise:** Map data flow, trust transitions, permissions, and approval points for one agent.

**Output:** A small threat model tied to concrete controls.

### Module 4 — Earning limited autonomy

**Question:** What evidence would justify giving the workflow more authority?

Participants define:

- a representative evaluation set;
- success and failure criteria;
- false-positive and missed-detection measures;
- budgets and rate limits;
- human escalation rules;
- rollback and incident evidence;
- conditions under which the pilot stops.

**Exercise:** Draft a 30-day experiment for one reversible workflow.

**Output:** A pilot plan whose next phase depends on measured results rather than a predetermined rollout.

## Risk-based control table

| Consequence | Default workshop recommendation | Example |
|---|---|---|
| High or irreversible | Strong authentication, exact effect preview, explicit approval, recovery plan | Delete, publish, transfer funds, alter access |
| Medium | Isolated environment, tests, diff, human review before effect | Code and configuration changes, external drafts |
| Low and reversible | Bounded automation, logging, sampled review | Read-only collection from approved public sources |

The label belongs to the complete workflow. A summarizer handling private health data is not low risk merely because it only produces text.

## Full-day extension

A full-day version can add three practical labs:

### Retrieval and provenance lab

Build a small corpus, inspect chunking and retrieval failures, require claim-level citations, and test stale or conflicting sources. A vector database is optional; the learning target is provenance, not a particular product.

### Tool-bound agent lab

Give an agent one typed, reversible tool in an isolated environment. Add parameter validation, dry-run behavior, structured logs, and an approval gate. Test both ordinary mistakes and adversarial input.

### Evaluation and legal-triage lab

Create an evaluation set and review the intended purpose, affected people, data, operator role, and sector. This is triage, not a legal determination.

Primary legal references:

- [European Commission — AI Act overview and application timeline](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [EUR-Lex — NIS2 Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng)
- [EUR-Lex — DORA Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj/eng)

## Facilitator guardrails

The February material used memorable slogans. These are the corrected versions.

| Earlier shorthand | Better teaching point |
|---|---|
| “The bottleneck is validation, not hallucination prevention.” | Reliability depends on task design, evidence, permissions, validation, and consequence limits. |
| “AI validates AI; humans validate validators.” | Models can assist review; independent sources, executable tests, and accountable people establish the boundary. |
| “Low-risk can be autonomous.” | Reversible, bounded actions may be automated after evaluation; the whole data and destination path determines risk. |
| “Start small, verify everything, scale trust.” | State what is checked, measure failures, and expand only the authority supported by evidence. |

Facilitators should not demonstrate a dangerous action against a real account or production system. Use disposable data, isolated credentials, and dry runs. Participants should leave with evidence artifacts, not with a one-click “autonomous agent.”

## Materials and availability

| Item | Public status |
|---|---|
| Historical training video | [Available on YouTube](https://youtu.be/64qeuW15J8g) |
| Corrected training notes | [Chapter 06](../docs/06_ai_agents_training.md) |
| Historical code examples | [Public `myscripts` repository](https://github.com/GLyttek/myscripts); examples require review before reuse |
| Slide deck | Not included in this repository |
| Intent and risk templates | Described in this outline; no packaged template set is currently published |
| Legal checklist | Not provided; use official sources and qualified review |

## Technical setup

For demonstrations:

- Python 3.10 or newer;
- an isolated working directory or disposable container;
- a local or cloud model endpoint with test credentials;
- approved sample documents containing no private or client data;
- a code editor and a way to inspect structured logs.

The workshop should still work if a model endpoint fails. The core lessons are the boundary, evidence, and recovery behavior—not a live model performance show.

---

*Developed by Lyttek GmbH in February 2026; substantially revised in July 2026.*
