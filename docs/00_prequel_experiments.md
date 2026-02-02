# 00 - Prequel: Early AI Experiments (August 2024)

*Before the journey began - learning the fundamentals*

## Context

The Lyttek AI Journey didn't start from zero. In August 2024, months before the main project kicked off, a series of learning experiments laid the foundation for everything that came later.

These experiments were messy, unstructured, and sometimes naive. But they taught essential skills that made the later automation possible.

## The Experiments

### 1. MITRE ATT&CK + LLM Integration

**What:** A script that extracts Tactics, Techniques, and Procedures (TTPs) from natural language cybersecurity scenarios.

**Why it mattered:** Proved that LLMs could bridge the gap between human language and structured security frameworks. This became foundational for content classification later.

```python
# Core insight: LLMs excel at semantic extraction
keywords = llm.extract("Find TTPs in: {scenario}")
matches = mitre_db.search(keywords)
```

**Lesson learned:** Domain-specific prompts beat generic ones. "You are a cybersecurity professional" produces better security content than "You are a helpful assistant."

---

### 2. Vector Database & RAG

**What:** Built a FAISS-based vector database for document Q&A, originally for ISO compliance documents.

**Why it mattered:** First hands-on experience with:
- Embedding models
- Vector similarity search
- Context injection

**Architecture that emerged:**
```
Document → Embed → Store → Query → Retrieve → Generate
```

This exact pattern now powers our knowledge retrieval system.

**Lesson learned:** RAG isn't magic. Quality depends on:
1. Chunk size (too small = no context, too large = noise)
2. Embedding model quality
3. Retrieval count (k=5 works for most cases)

---

### 3. Security Awareness Content Generator

**What:** Automated generation of cybersecurity awareness training materials.

**Why it mattered:** First experience with:
- Multi-step generation (outline → slides → content)
- Output structuring (forcing specific formats)
- Progress tracking for long-running tasks

**Key insight:** Breaking complex generation into steps produces better results than one-shot prompting.

```
Step 1: Generate outline (10-15 items)
Step 2: For each item → Generate detailed content
Step 3: Aggregate into final document
```

This decomposition pattern now underlies our synthesizer architecture.

---

### 4. Ollama API Exploration

Multiple scripts explored different aspects of local LLM deployment:

| Experiment | Learning |
|------------|----------|
| `OllamaPost.py` | REST API basics, timeouts, error handling |
| `ollamachat2.py` | Conversation state, message formatting |
| `Ollamaroles.py` | System prompts, role-based behavior |
| `visionlama.py` | Multi-modal models |

**Critical discovery:** Local models are good enough for filtering and classification, but synthesis needs cloud models.

---

## What These Experiments Taught

### Technical Skills

| Skill | Experiment | Applied Later In |
|-------|------------|------------------|
| LLM API patterns | All scripts | Every worker |
| Vector databases | ISO-vector-db | Knowledge retrieval |
| Prompt engineering | MITRE, Awareness | Content classification |
| Error handling | OllamaPost | Collector resilience |
| Output formatting | Awareness | Structured reports |

### Mental Models

1. **LLMs as interpreters** - They translate between human intent and structured action
2. **RAG as memory** - Vector databases give LLMs persistent context
3. **Decomposition works** - Break complex tasks into simple steps
4. **Local vs. Cloud** - Match model capability to task requirements

---

## From Experiments to System

These experiments converged into the first real automation:

```
August 2024         → October 2024           → February 2026
-----------------      -----------------         -----------------
MITRE extractor    →   Content classifier   →   Team Leads
Vector DB          →   Knowledge retrieval  →   RAG-enhanced responses
Awareness generator→   Synthesizers         →   Report generation
Ollama scripts     →   LLM Router           →   Multi-model orchestration
```

The journey from "random scripts" to "working system" wasn't a leap - it was gradual integration of proven patterns.

---

## Artifacts

The cleaned-up experiments are available at:
[github.com/GLyttek/myscripts/llm-experiments](https://github.com/GLyttek/myscripts/tree/main/llm-experiments)

Including:
- `mitre-attack/` - TTP extraction tool
- `iso-vector-db/` - RAG system
- `security-awareness/` - Content generation

---

## Reflection

Looking back, these experiments seem obvious. Of course you need vector databases for RAG. Of course you decompose complex generation. Of course you match models to tasks.

But at the time, each was a discovery. Each built confidence for the next step.

> *The foundation was laid in experiments. The system was built on patterns.*

---

*This document added: February 2026*
*Documenting work from: August 2024*
