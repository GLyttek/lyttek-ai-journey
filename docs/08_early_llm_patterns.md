# 08 — Early LLM Patterns Revisited

> **Historical period:** August 2024–February 2025<br>
> **Editorial note, July 2026:** The original document presented five patterns as short recipes with “key insights.” This revision compares those ideas with the retained prototypes and later operational experience. The patterns were useful, but the early implementations did not provide the validation, safety, or reproducibility that the old wording implied.

The early experiments repeated a handful of structures: one model call feeding another, retrieval before generation, a loop that selected tools, different models for different tasks, and transcripts used as source material.

At the time, naming a pattern made it feel more mature than it was. The code often demonstrated only the happy path. This chapter records what each pattern contributed and what the prototypes failed to establish.

## Prompt chains reduced scope but did not validate output

A typical chain looked like this:

```text
source → summary → short post → hashtags
```

Splitting a large request into smaller steps made prompts easier to inspect and outputs easier to reuse. It also created error propagation. If the summary omitted a caveat, every later stage inherited the omission.

The original chapter claimed that each step “validates before proceeding.” The code did not do that. It passed text from one model call into the next. Actual validation would require a schema, source comparison, deterministic checks, a separate evaluator with known limits, or human review.

The pattern survived, but with a new rule: a chain is decomposition, not evidence.

## Local RAG was a retrieval experiment, not persistent memory

The local prototype used Ollama embeddings and cosine similarity to select text chunks before calling a chat model:

```text
query → embedding → similarity ranking → selected chunks → model response
```

That was useful for understanding the mechanics of retrieval-augmented generation. The implementation itself had basic defects: the parser did not reliably read the intended paragraphs, the cache-path check was malformed, and there was no question set or relevance judgment to evaluate retrieval.

A later FAISS-based experiment for ISO-related material improved the structure, but the broader limits remained:

- chunking can remove the context needed to understand a passage;
- similarity is not the same as relevance;
- retrieved text can be outdated, hostile, or wrong;
- adding context does not force a model to cite or follow it;
- retrieval does not update model weights or create human-like memory.

RAG became part of the knowledge workflow. I no longer describe it as “giving the model memory” without explaining which retrieval and persistence mechanisms are actually present.

## Tool loops needed boundaries more than clever reasoning

The [ReAct pattern](https://arxiv.org/abs/2210.03629) combines reasoning traces with actions and observations. My small examples included a coffee-shop agent that interpreted an order and selected a tool.

The conceptual loop was simple:

```text
observe → choose an allowed action → execute → inspect result → stop or continue
```

The old pseudocode made the model's reasoning look like the main engineering challenge. In practice, parsing, permissions, termination, and error handling mattered more:

- Which tools are exposed?
- What arguments are accepted?
- Can an action be reversed?
- How many iterations are allowed?
- What requires human approval?
- What happens when output cannot be parsed?

A tool loop without these boundaries is not a capable agent architecture. It is an unbounded retry mechanism with side effects.

## Model routing remained task-specific

I experimented with using different models for embeddings, short responses, longer reasoning, and creative work. The first table labeled particular models as “best.” There was no benchmark supporting that word, and model availability changed quickly.

A more accurate historical description is:

| Task at the time | Candidate used | Reason for trying it |
|---|---|---|
| Embeddings | `mxbai-embed-large` / `nomic-embed-text` | Local vector representation |
| Short local generation | small Llama-family models | Lower latency and memory use |
| Larger local generation | Mixtral or larger Llama variants | More capability when hardware allowed |
| Hosted generation | Claude, Gemini, or Groq-hosted Mixtral | Better output or easier access for selected tasks |

This was exploratory routing, not an automatic system that reliably selected the best model. The decision still required knowledge of data sensitivity, task difficulty, model behavior, cost, latency, and available hardware.

The [Current State](../CURRENT_STATE.md) reflects the narrower 2026 conclusion: there is no mature router that solves this choice for every task.

## Video transcripts were useful and easy to overtrust

One pipeline downloaded a video, extracted audio, transcribed it, and used the transcript as conversational context. Another processed folders of audio with local Whisper and asked a hosted model for summaries and prompted “expert” perspectives.

These experiments anticipated later research intake, but the early label “knowledge source” was too generous. A transcript can be useful source material while still containing:

- automatic transcription errors;
- missing visual context;
- unsupported claims from the speaker;
- lost attribution and timestamps;
- copyright and reuse limits;
- model-generated summaries that add a second layer of distortion.

The current workflow preserves source URLs, captures transcripts where permitted, labels evidence quality, and separates what a speaker said from what stronger sources establish.

## What carried forward

The patterns did not become a production system exactly as drawn. They became questions asked at every handoff:

- Does this step reduce complexity or merely move uncertainty downstream?
- What evidence connects the output to its source?
- Is the model proposing text or authorizing an effect?
- Can deterministic code perform this step more reliably?
- Which context is durable, and who can inspect or correct it?

Later examples are available in [`GLyttek/myscripts/llm-experiments`](https://github.com/GLyttek/myscripts/tree/main/llm-experiments). That directory was added in February 2026 and still needs project-specific security and reproducibility review. It documents the pattern family but is not evidence that those exact files were public during the 2024–2025 experiments.

The value of the early work was not that the recipes were correct. It was that they made the missing controls visible.

---

*Next: [09 — Aletheia](09_aletheia_local_agent.md)*
