# 08 - Early LLM Patterns

**Date:** August 2024 - February 2025
**Status:** Learning Journey
**Source:** Various experiments

---

## Overview

This document captures the patterns we discovered during early LLM experimentation. These simple patterns became the foundation for more complex systems.

## Pattern 1: Chain Prompting

Breaking complex tasks into sequential prompts.

### The Problem

Single prompts for complex tasks often fail:
```
"Write a marketing strategy and implementation plan for a new product"
```

### The Solution

Chain smaller, focused prompts:

```python
# Step 1: Analysis
analysis = llm("Analyze the target market for {product}")

# Step 2: Strategy (uses Step 1 output)
strategy = llm(f"Based on this analysis: {analysis}, outline key strategies")

# Step 3: Implementation (uses Step 2 output)
plan = llm(f"Create implementation steps for: {strategy}")
```

### Key Insight

Each step validates before proceeding. Errors caught early.

---

## Pattern 2: Local RAG

Retrieval-Augmented Generation using local models.

### Architecture

```
User Query → Embedding → Vector Search → Context Injection → LLM → Response
```

### Implementation (Ollama + PyTorch)

```python
# Embed the query
query_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=query)

# Find similar documents
similarities = torch.cosine_similarity(query_embedding, doc_embeddings)
top_docs = get_top_k(similarities, k=3)

# Generate with context
response = ollama.generate(
    model='llama3',
    prompt=f"Context: {top_docs}\n\nQuestion: {query}"
)
```

### Key Insight

Query rewriting improves retrieval:
```python
rewritten = llm(f"Rewrite this query for better search: {original_query}")
```

---

## Pattern 3: ReAct Agents

Reason + Act pattern for tool-using agents.

### The Loop

```
Observe → Think → Act → Observe → Think → Act → ...
```

### Implementation

```python
while not done:
    # Think: What should I do?
    thought = llm(f"Given {observation}, what action should I take?")

    # Act: Execute the action
    action = parse_action(thought)
    result = execute(action)

    # Observe: What happened?
    observation = result
```

### Coffee Shop Example

We built a barista agent that:
1. Receives customer order (Observe)
2. Decides what to make (Think)
3. Calls make_coffee() tool (Act)
4. Confirms with customer (Observe)

### Key Insight

Simple tools + clear thinking = capable agents.

---

## Pattern 4: Multi-Model Orchestration

Using different models for different tasks.

### The Insight

Not all tasks need the same model:

| Task | Best Model | Why |
|------|------------|-----|
| Embedding | mxbai-embed-large | Optimized for vectors |
| Fast inference | llama3.2:3b | Low latency |
| Complex reasoning | llama3.2:70b | Higher capability |
| Creative writing | Gemini | Different "personality" |

### Implementation

```python
def route_to_model(task_type):
    if task_type == "embedding":
        return "mxbai-embed-large"
    elif task_type == "quick":
        return "llama3.2:3b"
    elif task_type == "complex":
        return "llama3.2:70b"
```

---

## Pattern 5: YouTube as Knowledge Source

Transcripts contain valuable unstructured knowledge.

### Pipeline

```
YouTube URL → Transcript API → Chunking → Embedding → RAG
```

### Why It Works

- Experts share knowledge in videos
- Transcripts are free
- Spoken content is often clearer than written docs
- Timestamps enable source verification

### Caution

- Transcripts have errors (auto-generated)
- Context can be lost without video
- Copyright considerations

---

## Evolution

These patterns evolved into our production system:

| Early Pattern | Production Version |
|--------------|-------------------|
| Chain Prompting | Content Pipeline |
| Local RAG | Knowledge Manager |
| ReAct Agents | Team Lead Workers |
| Multi-Model | LLM Router |
| YouTube RAG | Content Intelligence |

## Code Locations

- **myscripts/llm-experiments/local-rag/** - RAG implementations
- **myscripts/llm-experiments/youtube-rag/** - YouTube processing
- **myscripts/llm-experiments/agent-patterns/** - ReAct examples

---

*Part of the [Lyttek AI Journey](../README.md)*
