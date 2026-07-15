# Lyttek AI Journey

**An engineering journal about building a personal AI automation and decision-support system**

> *"The future isn't only human in the loop. It is AI and humans working with explicit responsibilities, limits, and review gates."*

This repository documents the evolution of a private AI workspace since 2024: early experiments, automation workers, agent security, human approval, local models, production failures, and the lessons that followed.

The production workspace itself is **not published here**. This is a documentation and case-study repository containing sanitized architecture notes, selected code excerpts, training material, and local benchmark observations. It should not be read as a ready-to-deploy agent framework.

## Start Here

- New to the project: read [01 - Genesis](docs/01_genesis.md), [05 - Lessons Learned](docs/05_lessons_learned.md), and [11 - Production Reality Check](docs/11_production_reality_check.md).
- Interested in the current agent direction: read [09 - Aletheia](docs/09_aletheia_local_agent.md).
- Interested in local inference and AMD ROCm: read [12 - Bonsai 1-bit Local Deployment](docs/12_bonsai_1bit_local_deployment.md).
- Interested in training material: see the [workshop](workshops/AI_Agents_Workshop_Outline.md) and presentation below.

## Repository Scope

This repository is intended to show:

- which architectural decisions were made and why;
- which assumptions failed under real end-to-end use;
- how human approval, local inference, and cloud models were combined;
- where security and operational controls were initially insufficient;
- how the system changed over time.

It does **not** provide:

- the private production workspace or its data;
- a supported software distribution;
- independently audited security controls;
- benchmark results that generalize beyond the documented hardware and test conditions.

## Current State

**Documentation state:** April 2026

**Repository review:** July 2026

The most recent documented architecture combines:

- local collectors and worker processes for bounded tasks;
- cloud models for selected synthesis and review work;
- Markdown and Obsidian as the human-readable knowledge layer;
- explicit approval queues for consequential actions;
- a local Aletheia command center for workspace visibility;
- Docker-based local inference experiments.

Earlier chapters are historical snapshots. Statements such as “current,” “production ready,” or “what comes next” describe the state at the chapter date and may be superseded by later chapters.

## Guiding Principles

1. **Human responsibility remains explicit:** AI can propose, analyze, and execute bounded tasks; humans retain accountable decisions.
2. **Cost follows task complexity:** use local models for suitable volume work and cloud models only where their capability adds value.
3. **Security is architectural:** prompt boundaries alone are not a security control; permissions, isolation, validation, logging, and approval gates matter.
4. **Practical over performative:** end-to-end evidence matters more than clean diagrams or “production ready” labels.
5. **Document corrections:** failed assumptions and superseded designs remain visible as part of the engineering record.

## Documentation

| Chapter | Period | Description | Status |
|---|---|---|---|
| [00 - Prequel: Early Experiments](docs/00_prequel_experiments.md) | Aug 2024 | Experiments that laid the foundation | Historical snapshot |
| [01 - Genesis](docs/01_genesis.md) | Oct 2025 | How the workspace started with Claude Code | Historical snapshot |
| [02 - First Automation](docs/02_first_automation.md) | 2025 | Building the first workers and queues | Historical snapshot |
| [03 - Security Evolution](docs/03_security_evolution.md) | Jan–Feb 2026 | Prompt injection, cost controls, and audit gaps | Historical; corrections added |
| [04 - Multi-Agent Architecture](docs/04_multi_agent.md) | Feb 2026 | Hierarchical agents with local and cloud models | Historical snapshot |
| [05 - Lessons Learned](docs/05_lessons_learned.md) | Feb 2026 | What worked and what did not | Historical; later chapters supersede parts |
| [06 - AI Agents Training](docs/06_ai_agents_training.md) | Feb 2026 | Reliability, validation, safety, and regulation | Training snapshot; corrections added |
| [07 - ACE Framework Exploration](docs/07_ace_framework_exploration.md) | Feb 2025 | Exploration of a layered agent architecture | Historical snapshot |
| [08 - Early LLM Patterns](docs/08_early_llm_patterns.md) | Aug 2024–Feb 2025 | Chain prompting, RAG, ReAct, and orchestration | Historical snapshot |
| [09 - Aletheia](docs/09_aletheia_local_agent.md) | Feb 2026 | From local reflection agent to command center | Historical architecture snapshot |
| [10 - Novaterra Story Engine](docs/10_novaterra_story_engine.md) | Feb 2026 | Multi-model story generation experiment | Historical snapshot |
| [11 - Production Reality Check](docs/11_production_reality_check.md) | Feb 2026 | Infrastructure hardening and PDCA verification | Verified case-study snapshot |
| [12 - Bonsai 1-bit Local Deployment](docs/12_bonsai_1bit_local_deployment.md) | Apr 2026 | AMD ROCm deployment and local benchmark | Single-machine case study |

## Evidence Convention

The documents use four evidence categories:

- **Observed:** output, failure, or measurement from the documented local system.
- **External:** claim supported by a linked primary or vendor source.
- **Interpretation:** conclusion drawn from observations or external material.
- **Recommendation:** a proposed practice, not a measured fact.

Older chapters did not always separate these categories clearly. Correction notes now identify important limitations. Numbers without a linked methodology or source should be treated as local observations or author assessments, not universal benchmarks.

## Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│ Human owner                                                     │
│ Accountable decisions · approvals · priorities · risk acceptance│
├─────────────────────────────────────────────────────────────────┤
│ Review and synthesis                                            │
│ Selected cloud/local models · quality checks · routing          │
├─────────────────────────────────────────────────────────────────┤
│ Bounded workers                                                 │
│ Collection · transformation · monitoring · local inference      │
├─────────────────────────────────────────────────────────────────┤
│ Human-readable state                                            │
│ Markdown · Obsidian · queues · logs · documented decisions      │
└─────────────────────────────────────────────────────────────────┘
```

The diagrams and code excerpts describe the system at specific points in time. They are not a deployment specification.

## Training Materials

- **[AI Agents Workshop](workshops/AI_Agents_Workshop_Outline.md)** — half-day and full-day workshop outline
- **[Training Video](https://youtu.be/64qeuW15J8g)** — presentation on YouTube
- **[Training Slides](presentations/AI%20Agents%20Training%20%20Accelerating%20Agent%20Use%20in%202026.pptx)** — PowerPoint source; large binary asset

## Research and Whitepapers

| Paper | Original year | Topic | Follow-up |
|---|---:|---|---|
| [Redefining Efficiency in AI](whitepapers/Redefining%20Efficiency%20in%20AI%20The%20Impact%20of%201.58-bit%20LLMs%20on%20the%20Future%20of%20Computing.pdf) | 2024 | BitNet b1.58 and low-bit inference | [2026 retrospective](whitepapers/1_58_bit_llm_retrospective_2026.md) |

## Related Repositories

- **[myscripts](https://github.com/GLyttek/myscripts)** — public Python utilities and cleaned-up experiments

## Influences and Terminology

The project explored or referenced:

- [David Shapiro's ACE Framework](https://github.com/daveshap/ACE_Framework)
- [OpenAI Agent Swarm / HAAS](https://github.com/daveshap/OpenAI_Agent_Swarm)
- [GATO Framework](https://github.com/daveshap/GATO_Framework)

`GATO` is an external influence. `GOTCHA`, used in some historical chapters, was an internal security mnemonic rather than an industry standard. The public documentation now labels that distinction explicitly.

## Security Notice

The repository contains historical security approaches that were later found to be incomplete. In particular:

- regex detection and prompt delimiters do not neutralize prompt injection;
- local-only services still need deliberate binding, authentication, and browser-origin controls;
- agent safety depends on capability limits and approval boundaries, not only model instructions;
- Docker examples require image, source, and model pinning before they are reproducible or supply-chain hardened.

Do not deploy excerpts unchanged in a sensitive environment.

## Repository Checks

Run the local documentation checks with:

```bash
python3 scripts/check_docs.py
```

The check verifies local Markdown links and confirms that every numbered chapter is indexed in this README.

## License

MIT License — see [LICENSE](LICENSE).

## About Lyttek

Lyttek documents practical work at the intersection of IT security, local AI, automation, and human decision-making. The focus is not autonomous operation at any cost, but systems whose boundaries and operational consequences remain visible.
