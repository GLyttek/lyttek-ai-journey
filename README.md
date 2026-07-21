# Lyttek AI Journey

**A documented personal AI journey — from a WhatsApp conversation with Pi in May 2023 to local models, automation workers, and a bounded human-approved agent system.**

I did not begin with an agent architecture. I began by talking to an AI and asking what kind of relationship between people and machines might be useful.

The first retained source is a private WhatsApp conversation with Pi from May 2023. By March 2024 I was publishing small Python experiments for local models and model APIs. In 2025 those experiments grew into file-based workers and queues. In 2026 the work became less about adding autonomy and more about evidence, permissions, failure recovery, and knowing when a deterministic script is the better tool.

This repository preserves that development without pretending it was a straight line.

## What this repository is

This is a documentation and case-study repository. It contains:

- dated reflections on the ideas and systems I was testing;
- selected and sanitized code excerpts;
- links to publicly verifiable experiments;
- local observations with their limitations;
- corrections where later evidence changed my assessment.

The private production workspace, personal data, credentials, and raw source archives are not published here. The repository is not a supported agent framework, an audited security product, or a deployment guide.

## Timeline and evidence

| Period | What I was doing | Evidence available to a reader |
|---|---|---|
| **May 2023–Jan 2025** | Talking with Pi about trust, memory, bias, hallucinations, care, attachment, and AI as a ferryman rather than an authority | [Public reflection](docs/prologue_pi_2023.md), based on a private retained WhatsApp export |
| **Feb–Apr 2024** | Comparing local-model output, calling Claude and Groq from Python, transcribing audio, and building rough RAG and document pipelines | Public commits in [`GLyttek/myscripts`](https://github.com/GLyttek/myscripts) plus private local artifacts |
| **Aug 2024–Feb 2025** | Exploring MITRE extraction, retrieval, prompt chains, tool loops, and model routing | [Early experiments](docs/00_prequel_experiments.md) and [pattern review](docs/08_early_llm_patterns.md); cleaned examples were published later |
| **Oct–Dec 2025** | Turning scripts into file-based queues, workers, dashboards, and approval folders | [Genesis](docs/01_genesis.md) and [First Automation](docs/02_first_automation.md) |
| **Jan–Feb 2026** | Adding security controls, multiple model roles, Aletheia, and a local command-center prototype | Chapters [03](docs/03_security_evolution.md) through [11](docs/11_production_reality_check.md) |
| **Apr–Jul 2026** | Testing local deployment, replacing brittle agentic jobs with bounded scripts, and moving Aletheia into Hermes Agent | [Bonsai deployment](docs/12_bonsai_1bit_local_deployment.md), [bounded research](docs/13_bounded_research_scripts.md), and [Current State](CURRENT_STATE.md) |

The earliest public code evidence is the [`myscripts` repository](https://github.com/GLyttek/myscripts), created on 2 March 2024. Its 2024 history includes:

- a [local-model comparison script](https://github.com/GLyttek/myscripts/commit/080422481e981934c573f36fb41d3624aa7900d9);
- a [Claude API document experiment](https://github.com/GLyttek/myscripts/commit/0b19f0669b38ef0de03352d0a76de269122d5f00);
- a [Groq/Mixtral chatbot](https://github.com/GLyttek/myscripts/commit/ef2bffa9de363ee6660221c37c57d8fbef98e5ab);
- a [local Whisper and API summarization pipeline](https://github.com/GLyttek/myscripts/commit/50e128f7453da379feda240ead4cb633688394fd).

These are learning artifacts. They contain rough edges and should not be read as current implementation advice. The later `llm-experiments/` collection in that repository was cleaned up and added in 2026; its current location is not evidence that the same published files existed in 2024.

## Choose a reading path

- **Origin and intent:** [The Ferryman Before the System](docs/prologue_pi_2023.md) → [Early Experiments](docs/00_prequel_experiments.md) → [Genesis](docs/01_genesis.md)
- **Automation and failure:** [First Automation](docs/02_first_automation.md) → [Lessons Revisited](docs/05_lessons_learned.md) → [Production Reality Check](docs/11_production_reality_check.md)
- **Aletheia and human control:** [Aletheia](docs/09_aletheia_local_agent.md) → [Current State](CURRENT_STATE.md)
- **Local models and reliability:** [Early LLM Patterns](docs/08_early_llm_patterns.md) → [Bonsai 1-bit Deployment](docs/12_bonsai_1bit_local_deployment.md) → [When Agentic Research Needed Less Agency](docs/13_bounded_research_scripts.md)

## Practical agent-security guides

These guides turn the repository's later lessons into reviewable control patterns. They are design and review material, not an audited framework or a substitute for testing the real environment.

- [Secure Agent Control Plane](guides/secure_agent_control_plane.md) — separate model proposals from authorization, execution, egress and verification.
- [MCP Least Privilege and Tool Scoping](guides/mcp_least_privilege.md) — inventory servers, minimize tool exposure, protect credentials and control cross-server data flow.
- [Defensive Rules for Coding Agents](guides/defensive_coding_agent_rules.md) — repository instructions plus the deterministic controls that must enforce them.
- [API Security by Design](guides/api_security_by_design.md) — make actors, resources, relationships, states and negative authorization cases explicit before generation.
- [Verifiable Control Points](guides/verifiable_control_points.md) — define where a control runs, what it blocks and which evidence proves its operation.

### Field note in German

- [Risk Tiering in der Praxis: Was funktioniert hat und was nicht](field-notes/risk_tiering_in_practice_de.md) — local successes, classification failures, approval fatigue and the boundary between recommendation and enforcement.

## Current state

**Snapshot:** 16 July 2026<br>
**Repository review:** July 2026

[Current State](CURRENT_STATE.md) describes what I actually use now. Hermes Agent is the active harness for conversations, skills, tools, memory, scheduled work, and execution receipts. Aletheia continues as a persona and co-pilot role inside Hermes rather than as the standalone command-center application described in Chapter 09.

The project remains a proof of concept. The recurring value today is research support, structured collaboration, learning, and bounded execution after review. It is not an autonomous production platform.

## Evidence convention

Public claims in this repository should fit one of four categories:

- **Observed:** output, failure, or measurement from a documented local run.
- **External:** a claim attributed to a linked primary or vendor source.
- **Interpretation:** my conclusion from observed or external material.
- **Recommendation:** a proposed practice, not a measured result.

There is also a necessary visibility distinction:

- **Public evidence** can be opened by an unauthenticated reader.
- **Private archival evidence** is retained locally but withheld for privacy or security.
- **Historical recollection** is identified as recollection when no stronger artifact remains.

Older chapters did not always make these boundaries explicit. The July 2026 editorial pass narrowed unsupported claims and added dated correction notes without hiding the original sequence of work.

## Principles that survived the experiments

1. **Human responsibility stays explicit.** Models can propose, analyze, or execute bounded tasks. Values, publication, money, rights, risk acceptance, and decisions affecting other people remain human decisions.
2. **A model response is not evidence of success.** The output still needs source checks, validation, or an end-to-end test appropriate to the task.
3. **Security belongs in the architecture.** Prompt wording alone cannot provide isolation, least privilege, safe tool use, auditability, or approval boundaries.
4. **Use the least complex mechanism that works.** A deterministic script is often more reliable than an agent for collection, thresholds, file checks, and repeatable transformations.
5. **Preserve corrections.** Failed assumptions are part of the engineering record, not material to be edited out after the fact.

## Documentation

| Chapter | Period | Description | Status |
|---|---|---|---|
| [Prologue — The Ferryman Before the System](docs/prologue_pi_2023.md) | May 2023–Jan 2025 | Early conversations about trust, memory, care, and AI as a ferryman | Historical reflection |
| [00 — From Conversation to Code](docs/00_prequel_experiments.md) | Feb–Aug 2024 | Local models, APIs, RAG, and document-generation experiments | Historical evidence review |
| [01 — Genesis](docs/01_genesis.md) | Oct 2025 | How conversational coding became a file-based workflow | Historical account; claims corrected against retained artifacts |
| [02 — First Automation](docs/02_first_automation.md) | Nov–Dec 2025 | File-based workers, dashboards, queues, and early routing | Historical evidence review |
| [03 — Security Evolution](docs/03_security_evolution.md) | Jan–Feb 2026 | What PromptShield and the cost tracker actually controlled | Historical implementation review |
| [04 — Multi-Agent Architecture](docs/04_multi_agent.md) | Feb 2026 | Queues, model roles, approval gates, and failure propagation | Historical architecture review |
| [05 — Lessons Revisited](docs/05_lessons_learned.md) | Feb 2026 / Jul 2026 | What survived later operational use and what did not | Historical reflection with corrections |
| [06 — AI Agents Training](docs/06_ai_agents_training.md) | Feb 2026 / Jul 2026 | Reliability through evidence, bounded authority, and evaluation | Corrected training notes; original video remains historical |
| [07 — ACE Framework Exploration](docs/07_ace_framework_exploration.md) | Feb 2025 / Jul 2026 | What the retained six-layer prototype implemented and simulated | Historical code review |
| [08 — Early LLM Patterns Revisited](docs/08_early_llm_patterns.md) | Aug 2024–Feb 2025 | Prompt chains, RAG, tool loops, and routing under review | Historical pattern review |
| [09 — Aletheia](docs/09_aletheia_local_agent.md) | Feb 2026 / Jul 2026 | Standalone prototype, audit findings, and transition into Hermes | Historical architecture review |
| [10 — Novaterra Story Engine](docs/10_novaterra_story_engine.md) | Aug 2024 / Feb 2026 / Jul 2026 | A 12-chapter drafting engine, model comparison, and rule-based checks | Historical artifact review |
| [11 — Production Reality Check](docs/11_production_reality_check.md) | Feb 2026 | Infrastructure hardening and PDCA verification | Verified case-study snapshot |
| [12 — Bonsai 1-bit Local Deployment](docs/12_bonsai_1bit_local_deployment.md) | Apr 2026 | AMD ROCm deployment and local benchmark | Single-machine case study |
| [13 — When Agentic Research Needed Less Agency](docs/13_bounded_research_scripts.md) | Jul 2026 | Replacing brittle model-driven research crons with bounded scripts | Verified local case-study snapshot |

## Responsibility flow

```text
Question, local material, or public source
                    |
                    v
       Bounded tool, script, or model
                    |
        +-----------+-----------+
        |                       |
        v                       v
 Operational evidence      Human-readable context
 and execution receipt     and working notes
        |                       |
        +-----------+-----------+
                    |
                    v
               Human review
                    |
                    v
       Optional bounded action or publication
```

The diagram describes responsibility, not a deployable architecture. Historical chapters contain more specific diagrams for the systems that existed at those dates.

## Security notice

Some historical examples contain approaches that later proved incomplete:

- regex checks and prompt delimiters do not neutralize prompt injection;
- generated classifications and scores are not self-validating;
- local services still need deliberate binding, authentication, and browser-origin controls;
- tool-using agents need capability limits and commit-time approval for consequential effects;
- model and container examples need pinned sources, revisions, and reproducible tests.

Do not deploy excerpts unchanged in a sensitive environment.

## Training, research, and related work

- [AI Agents Workshop](workshops/AI_Agents_Workshop_Outline.md) — revised public outline with exercises, evidence boundaries, and facilitator guardrails
- [Training video](https://youtu.be/64qeuW15J8g) — unedited February 2026 presentation snapshot; later corrections live in Chapter 06 and the workshop outline
- [Redefining Efficiency in AI](whitepapers/Redefining%20Efficiency%20in%20AI%20The%20Impact%20of%201.58-bit%20LLMs%20on%20the%20Future%20of%20Computing.pdf) — 2024 paper with a [2026 retrospective](whitepapers/1_58_bit_llm_retrospective_2026.md)
- [`GLyttek/myscripts`](https://github.com/GLyttek/myscripts) — public Python experiments and utilities

External influences referenced in historical chapters include David Shapiro's [ACE Framework](https://github.com/daveshap/ACE_Framework), [OpenAI Agent Swarm / HAAS](https://github.com/daveshap/OpenAI_Agent_Swarm), and [GATO Framework](https://github.com/daveshap/GATO_Framework). `GOTCHA` was an internal security mnemonic, not an industry standard.

## Repository checks

Run:

```bash
python3 scripts/check_docs.py
```

The check validates local Markdown links and confirms that every numbered chapter is indexed here.

## License

MIT License — see [LICENSE](LICENSE).

## About Lyttek

Lyttek documents practical work at the intersection of IT security, local AI, automation, and human decision-making. I am interested in what survives contact with real workflows: what helps, what fails, and which decisions must remain visibly human.
