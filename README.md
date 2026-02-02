# Lyttek AI Journey

**A Proof-of-Concept for AI-Human Partnership in Business**

> *"The future isn't 'human in the loop' – it's AI hand in hand with Human."*

This repository documents our journey of building a comprehensive AI automation system as a **POC for an AI-partnered company**. Started in late 2025, this project explores how AI and humans can work together as true partners, not just tools and operators.

## What We're Building

A hierarchical AI agent system that:
- **Collects information autonomously** using cheap local models (Docker)
- **Synthesizes findings** using cloud models (OpenRouter)
- **Presents for human approval** - AI proposes, human disposes

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIERARCHICAL AGENT SYSTEM                     │
├─────────────────────────────────────────────────────────────────┤
│  CEO (Human)        │  Final approval, strategic decisions      │
│  ─────────────────  │  ─────────────────────────────────────── │
│  Team Leads (Cloud) │  Synthesis, quality control (OpenRouter)  │
│  ─────────────────  │  ─────────────────────────────────────── │
│  Collectors (Local) │  Data gathering, 24/7 monitoring (Docker) │
└─────────────────────────────────────────────────────────────────┘
```

## Key Principles

1. **AI-Human Partnership**: Not "human in the loop" but genuine collaboration
2. **Cost optimization**: Local models for bulk work, cloud for quality
3. **Security first**: GOTCHA framework, prompt injection protection
4. **Practical over perfect**: Working systems over elegant theories
5. **Learning together**: Both AI and human grow from each interaction

## Documentation

| Document | Description |
|----------|-------------|
| [00 - Prequel: Early Experiments](docs/00_prequel_experiments.md) | August 2024 learning projects that laid the foundation |
| [01 - Genesis](docs/01_genesis.md) | How it all started with Claude Code |
| [02 - First Automation](docs/02_first_automation.md) | Building the first workers |
| [03 - Security Evolution](docs/03_security_evolution.md) | Learning from OpenClaw, implementing GOTCHA |
| [04 - Multi-Agent Architecture](docs/04_multi_agent.md) | Hierarchical agents with local models |
| [05 - Lessons Learned](docs/05_lessons_learned.md) | What worked, what didn't |
| [06 - AI Agents Training](docs/06_ai_agents_training.md) | Building reliable agents in 2026 |
| [07 - ACE Framework Exploration](docs/07_ace_framework_exploration.md) | David Shapiro's layered agent architecture |
| [08 - Early LLM Patterns](docs/08_early_llm_patterns.md) | Chain prompting, RAG, ReAct patterns |

### Training Materials

- **[AI Agents Workshop](workshops/AI_Agents_Workshop_Outline.md)** - Half/full-day workshop outline
- **[Training Video](https://youtu.be/64qeuW15J8g)** - Full presentation on YouTube
- **[Training Slides](presentations/AI%20Agents%20Training%20%20Accelerating%20Agent%20Use%20in%202026.pptx)** - PowerPoint presentation

### Research & Whitepapers

| Paper | Year | Topic | Status |
|-------|------|-------|--------|
| [1.58-bit LLMs](whitepapers/Redefining%20Efficiency%20in%20AI%20The%20Impact%20of%201.58-bit%20LLMs%20on%20the%20Future%20of%20Computing.pdf) | 2024 | BitNet b1.58, ultra-low-bit quantization | [2026 Retrospective](whitepapers/1_58_bit_llm_retrospective_2026.md) |

### Related Repositories

- **[myscripts](https://github.com/GLyttek/myscripts)** - Python AI utilities and cleaned-up experiments

## Architecture Overview

### Components

- **Content Pipeline**: YouTube analysis, webpage processing, content curation
- **Research System**: Automated research queries, knowledge gap detection
- **Writer System**: Content generation with quality thresholds
- **Security Layer**: PromptShield, cost tracking, audit logging
- **Collector Agents**: Topic-specific data gatherers (local Docker models)

### Tech Stack

- **Primary Interface**: Claude Code CLI
- **Cloud Models**: OpenRouter (Mistral, Gemini, Grok)
- **Local Models**: Docker Model Runner (gemma3, ministral3)
- **Knowledge Base**: Obsidian Markdown files
- **Scheduling**: Cron jobs + continuous watchers

## Code Examples

See the [examples/](examples/) directory for sanitized code snippets:
- `prompt_shield_example.py` - Input sanitization
- `collector_example.py` - Local model data collection
- `quality_routing_example.py` - Cloud model synthesis

## Why Open Source This?

1. **Transparency**: Show real-world AI agent development, not just theory
2. **Learning**: Document mistakes and solutions for others
3. **Community**: Contribute to the growing AI agent ecosystem
4. **Marketing**: Demonstrate Lyttek's AI consulting capabilities

## Timeline

| Date | Milestone |
|------|-----------|
| 2025-10 | Project started with Claude Code |
| 2025-11 | First content automation workers |
| 2025-12 | Knowledge management system |
| 2026-01 | Security hardening (GOTCHA framework) |
| 2026-02 | Hierarchical agent architecture |

## Influenced By

- [David Shapiro's ACE Framework](https://github.com/daveshap/ACE_Framework)
- [OpenAI Agent Swarm (HAAS)](https://github.com/daveshap/OpenAI_Agent_Swarm)
- [GATO Framework](https://github.com/daveshap/GATO_Framework)

## License

MIT License - See [LICENSE](LICENSE)

## About Lyttek GmbH

Lyttek is a German AI consulting company helping businesses implement practical AI solutions. We believe in AI that augments human capabilities, not replaces them.

---

*This documentation is auto-generated and manually curated. Last update: 2026-02-02*
