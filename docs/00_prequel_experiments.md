# 00 — From Conversation to Code: Early AI Experiments

> **Historical period:** February–August 2024<br>
> **Editorial note, July 2026:** The earlier version began in August 2024 and described several lessons too confidently. Public commits and retained local artifacts show practical AI work from February and March 2024. This revision preserves the sequence, distinguishes public from private evidence, and treats the early code as experiments rather than a finished foundation.

The [Pi conversations](prologue_pi_2023.md) gave me a picture of the relationship I wanted with AI. In early 2024 I began testing what the available models and APIs could actually do.

There was no unified workspace. I had folders full of scripts, generated documents, copied examples, and model outputs. Some experiments worked. Some only produced plausible-looking text. A few taught me more through their mistakes than through their intended result.

## The accessibility gap

My first OpenAI use required Python, an API key, request code, and enough technical knowledge to diagnose failures. Pi showed the other side of the change: an ordinary WhatsApp conversation could make a model useful to someone who had never written an API call.

A friend I told about Pi used it to structure a personal fitness plan. She needed no Python code, API key, or knowledge of prompt engineering. I remember that as an early example of what conversational access changed. It is a personal recollection, not a claim that Pi delivered medical treatment or a measured health outcome.

That difference shaped the experiments that followed. Model capability interested me, and so did the question of how models could become usable parts of a workflow.

## Comparing local-model output

Between February and March 2024 I generated several versions of cybersecurity policies, training material, and technical instructions. I also retained comparison outputs from models including Gemma, Mixtral, Nous Hermes, OpenChat, Orca, and others available through local tooling at the time.

The public `myscripts` repository provides a dated example. On [2 March 2024](https://github.com/GLyttek/myscripts/commit/080422481e981934c573f36fb41d3624aa7900d9), I committed a Python script that sent the same German cybersecurity tasks to two Ollama-backed models and saved their responses to DOCX files.

It was not a benchmark. The prompt set was tiny, the model names were placeholders, and there was no scoring rubric. The retained outputs nevertheless exposed a practical problem: fluent text could contain broken German, invented interface steps, and unsafe technical guidance. One model described BitLocker actions that did not match how Windows works.

The useful result was not a winner. It was the recognition that generated documentation needed review against the actual platform and task.

## Small API pipelines

By late March and early April, I was connecting several model and media components:

- a [Claude API document-generation experiment](https://github.com/GLyttek/myscripts/commit/0b19f0669b38ef0de03352d0a76de269122d5f00);
- a [small Groq/Mixtral chatbot](https://github.com/GLyttek/myscripts/commit/ef2bffa9de363ee6660221c37c57d8fbef98e5ab);
- a [local Whisper transcription and API summarization script](https://github.com/GLyttek/myscripts/commit/50e128f7453da379feda240ead4cb633688394fd).

The local working archive contains related prompt-chain, YouTube-transcription, RAG, and story-generation prototypes. They were direct and often brittle: API keys came from local files, state lived in global variables, exceptions were handled unevenly, and one model's output was frequently passed straight into the next step.

That roughness matters. The later focus on secrets, schemas, validation, and bounded actions did not begin as a theoretical security program. It grew out of code where those controls were missing.

## Retrieval was not memory

A local RAG prototype from March 2024 used Ollama embeddings, cosine similarity, and a local chat model:

```text
Document → chunks → embeddings → similarity search → selected context → response
```

The pattern was useful, but the implementation was not production-ready. The parser iterated over characters from a single line instead of reliably reading paragraphs. The embedding-cache path check was malformed. There was no evaluation set to show whether retrieval improved answer quality.

Calling RAG “memory” hid these weaknesses. Retrieval supplies selected context. It does not guarantee that the correct passage was indexed, retrieved, understood, or cited. That distinction became important later when persistent context and personal memory entered the system.

## Security and document experiments

Later experiments applied models to MITRE ATT&CK extraction, ISO-related document retrieval, security-awareness material, and longer report generation. They explored recurring patterns:

- extracting a structured candidate from natural language;
- splitting a large generation task into smaller calls;
- retrieving context before drafting;
- using local and hosted models for different parts of a pipeline.

The old wording treated these patterns as established solutions. They were not.

A domain-specific prompt could improve terminology, but it could also make an incorrect answer sound more authoritative. Prompt decomposition could reduce task size, but it did not validate intermediate output. Retrieval count and chunk size depended on the corpus and question; there was no universal `k=5`. Local models were sometimes sufficient for classification or drafting, but capability varied by model, prompt, language, and task.

## What the experiments established

By August 2024 I had practical experience with:

- calling local and hosted models from Python;
- preserving conversation state;
- transcription and summarization pipelines;
- embeddings and similarity search;
- multi-step generation;
- producing Markdown, HTML, and DOCX artifacts;
- comparing model output against security knowledge.

That is a narrower claim than saying the later architecture had already emerged. Most of the scripts were isolated prototypes. They did not have common logging, tests, approval gates, stable interfaces, or a shared state model.

What carried forward was a working habit: build a small path end to end, inspect the output, and change the design when the result failed.

## Evidence and publication history

The [`GLyttek/myscripts`](https://github.com/GLyttek/myscripts) repository is publicly accessible and was created on 2 March 2024. Its first commits provide public evidence for local-model and API experiments from March and April 2024.

The current [`llm-experiments`](https://github.com/GLyttek/myscripts/tree/main/llm-experiments) directory contains later examples for MITRE extraction, RAG, security-awareness generation, YouTube retrieval, and simple tool patterns. That collection was added in February 2026. It still contains rough implementation and security boundaries and should be read as learning material, not as a vetted reference implementation. Its present location is not proof that those exact files were public in 2024.

Other early outputs and prototypes remain private because they contain rough code, local paths, obsolete security practices, or generated material that has not been cleared for publication.

The next stage was not a sudden leap into agents. It was the slower work of turning isolated scripts into a workspace.

---

*Next: [01 — Genesis](01_genesis.md)*
