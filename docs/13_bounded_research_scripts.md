# 13 - When Agentic Research Needed Less Agency

*July 2026 — A local case study of nine recurring research jobs*

> **Status:** Verified local case-study snapshot. The failure counts and smoke-test results come from my private Hermes workspace on July 5, 2026. The scripts and operational data are not published in this repository, so these observations should not be treated as an independently reproducible benchmark.

## What I wanted the jobs to do

I had recurring research jobs for nine areas: AI security, cyber threat intelligence, OSINT methods, agent security, local models, RAG, SOC and incident response, health research, and psychology.

The original idea was attractive. A scheduled agent would search arXiv or PubMed, identify relevant papers, download material, create a report, update Kanban, and send me a useful summary. I would receive finished research instead of another list of links.

Several prompts gradually accumulated all of these steps in a single run:

```text
search
  -> delegate subtasks
  -> inspect and download papers
  -> assess relevance
  -> write a full report
  -> create Kanban items
  -> prepare a final chat summary
```

Each addition looked reasonable on its own. Together they created a long, model-dependent execution path with several external services, large outputs, and side effects.

## The failure pattern

I audited the jobs on July 5, 2026. All nine were failing or brittle.

| Result | Jobs affected | Observed failure |
|---|---:|---|
| Provider quota failure | 1 | Gemini returned HTTP 429 |
| Response truncation | 8 | The model-dependent run exceeded the usable response path before completing the requested workflow |

The problem was larger than a poor prompt. The model had become the scheduler, researcher, orchestrator, report writer, and delivery formatter at the same time. A failure near the end could invalidate work that had already consumed time and quota. A short final response also made it difficult to tell whether the search was incomplete, the report had been truncated, or an intermediate tool step had failed.

This matters more in unattended scheduled work than in an interactive session. During a conversation I can see a weak answer, ask what happened, and narrow the task. A cron job has to expose its own limits and failure state.

## The repair was a reduction in scope

I replaced the model-driven execution path with one deterministic Python collector and nine small wrapper scripts. Each wrapper selects a fixed screening configuration. The shared collector handles the common work.

The new path:

```text
fixed arXiv/PubMed queries
  -> bounded metadata collection
  -> per-query error capture
  -> deduplication
  -> transparent keyword scoring
  -> Top-5 triage
  -> source JSON + Markdown report
  -> compact delivery message
```

The collector uses public arXiv and PubMed endpoints. Every screening defines its queries, lookback window, score terms, maximum results per query, and total record cap in code. The ranking is deliberately simple: terms found in the title, abstract, or categories add points; recent work and terms such as `benchmark`, `evaluation`, or `systematic review` add small bonuses.

The full collected metadata is saved as JSON. The Markdown report contains the bounded Top 5, the remaining source list, and any collection errors. Failed queries are recorded instead of disappearing behind a polished summary.

The runtime no longer performs:

- LLM inference;
- delegated research subtasks;
- PDF downloads;
- Kanban changes;
- deep full-text analysis;
- a long model-generated delivery message.

That removed Gemini and local-model quota dependence from the collection stage. It also removed side effects that did not belong inside source discovery.

## What the smoke test showed

I ran all nine wrappers manually after the change.

| Screening | Records collected | Collection errors |
|---|---:|---:|
| AI security | 25 | 0 |
| Threat intelligence | 30 | 0 |
| OSINT methods | 24 | 0 |
| Agent security and architecture | 30 | 0 |
| Local models | 30 | 0 |
| RAG and knowledge management | 30 | 0 |
| SOC, incident response, and detection | 30 | 0 |
| Health and longevity | 24 | 0 |
| Psychology and personality | 24 | 0 |

The Python syntax check passed before the smoke runs. The existing schedules and delivery targets remained in place. The cron configuration showed all nine jobs active with `no_agent` enabled and the new wrapper scripts attached.

A later scheduler snapshot showed successful collector runs. One job still recorded a separate delivery-adapter error. That distinction is useful: source collection, report creation, scheduler state, and message delivery are different operational stages. A single `success` label for the whole chain can hide where the real failure occurred.

## What became better

The collection stage now has a visible contract:

- known public sources;
- explicit queries and limits;
- bounded output;
- saved raw metadata;
- per-query errors;
- no model or provider requirement;
- no write actions outside the report and source-data paths.

A rerun does not depend on a model deciding how much research is enough. I can inspect the queries, score terms, limits, source records, and collection errors directly.

The cost of the run is also easier to understand. There is no hidden expansion through delegated agents or repeated model calls. Network access remains a dependency, and upstream APIs can still fail, but those failures are captured at the query level.

## What became worse or disappeared

The scripts do less.

They do not read full papers. They cannot judge methodological quality. Keyword scoring can miss relevant work or rank a superficial match too highly. Metadata and abstracts can be incomplete. The selected Top 5 reflects the configured terms rather than a defensible literature-review method.

The report therefore says exactly what it is:

> This is a triage screen, not a literature review.

That sentence is part of the control. A deterministic script can produce repeatable output and still be incomplete, biased by its query design, or wrong about relevance.

Kanban creation also disappeared from the collection stage. A paper should become a task only after its relevance has been reviewed. Automatic task creation had mixed discovery with commitment and created administrative noise from weak matches.

## Where models still help

Models remain useful after collection. A bounded set of papers can be compared, challenged, and summarized with the sources kept in view. Full-text review can use a model when the data boundary permits it. A model can also propose search terms that I then inspect before adding them to the deterministic configuration.

The important change is the handoff point. The script establishes a small evidence base. Reasoning begins after that base exists and after collection errors are visible.

I now separate the roles this way:

| Stage | Default tool | Reason |
|---|---|---|
| Repeated source collection | Deterministic script | Known APIs, explicit limits, inspectable failures |
| Relevance triage | Script first, human review | Cheap narrowing with visible heuristic limits |
| Cross-source synthesis | Model with bounded sources | Semantic comparison and counter-arguments add value |
| Operational decision | Human | Context, risk acceptance, and accountability remain human responsibilities |
| External action | Approved tool path | Consequential effects need a separate gate |

This is a working rule, not a universal architecture pattern. Some research questions require exploratory agents from the beginning. The deciding factor is whether open-ended reasoning adds value before a stable evidence set exists.

## A correction to an earlier lesson

[Chapter 05](05_lessons_learned.md) argued that if I was writing `if`/`else` chains to interpret meaning, I should use an LLM. I still agree with the narrow version of that lesson. Semantic classification is often a poor fit for hand-written rules.

The research cron failure exposed a different category of work. Fetching known feeds, applying explicit limits, preserving metadata, and reporting exceptions are control-flow problems. Moving them into an LLM prompt made the execution harder to inspect without improving the collection itself.

The updated lesson is more precise:

- use code for repeatable control flow and evidence preservation;
- use models where interpretation changes the quality of the result;
- keep side effects behind their own approval boundary;
- test the full scheduled and delivery path, not only the core function.

## What I take from this

I had treated agency as a capability upgrade. In this case it became an unpriced reliability dependency.

The useful repair was smaller than the original design. It gave up automated full reports and task creation to make the first stage observable. That trade was worth it because I can now see what was searched, what was returned, which query failed, and where human or model review still begins.

The next improvement should preserve that boundary. A synthesis step may be added on top of the saved source set, with its own failure state and evidence rules. The collector should remain boring.

*Next: [Current State](../CURRENT_STATE.md) · [Back to Documentation Overview](../README.md)*
