# 04 - Multi-Agent Architecture: What the Hierarchy Actually Bought Me

> **Status:** Historical architecture snapshot from February 2026. Revised in July 2026 to distinguish implemented components, operating assumptions, and diagrams of intended behavior.

*February 2026*

## The goal was less noise, not more agents

My original sentence was: “I want AI systems that collect information autonomously, and I just approve the results at the end.”

That sounded efficient. It also hid most of the hard questions. Who chose the sources? What happened when a collector misunderstood an article? Which data could leave the machine? What evidence reached the final reviewer? What did “approve” authorize?

The useful part of the idea was smaller: separate cheap collection from expensive synthesis, and keep a human decision before consequential use.

```text
sources
   │
   ▼
bounded collectors
   │  retained items + source metadata
   ▼
synthesis step
   │  draft briefing
   ▼
human review
```

I described these layers as collectors, team leads, and a CEO. Those were role metaphors expressed in folders and Python classes, not a digital company.

## What was implemented

The workspace contained topic-specific collectors, a model router, staging directories, briefing templates, and approval queues. Local models could rank or summarize items. Cloud models could be selected for synthesis. Files made the hand-offs visible.

A collector followed this general pattern:

```python
items = fetch_approved_sources()

for item in items:
    score = assess_relevance(item)
    if score >= threshold:
        stage_with_source_metadata(item)
```

A later step could turn staged findings into a draft briefing. The human-facing folder was named `00_CEO/Pending_Approval/`. Its value was not the executive branding. It was the state transition: a generated document remained pending until a person moved, edited, or rejected it.

The code and artifacts support the existence of these components. They do not support the stronger impression that every topic ran continuously through one uniformly tested production pipeline.

## Why local and cloud models were separated

In February 2026, local models were useful for repetitive screening where false positives were tolerable and the source material should remain on the machine. Cloud models were sometimes better at compressing several findings into readable prose.

The first version of this chapter attached precise prices to reports and claimed that local work was free. Those numbers were snapshots of particular model routes and prompt sizes, not stable benchmarks. Local inference has no per-token API bill, but it still consumes power, memory, time, and hardware capacity.

The durable decision rule was not “local for simple, cloud for smart.” It became:

- keep sensitive or private material local unless there is an explicit reason not to;
- use the smallest model that passes a task-specific test;
- retain source references through every transformation;
- treat model output as a draft rather than a decision;
- measure cost and latency instead of copying yesterday's estimate.

Current boundaries are documented in [`CURRENT_STATE.md`](../CURRENT_STATE.md).

## Where the hierarchy came from

I was exploring David Shapiro's [ACE Framework](https://github.com/daveshap/ACE_Framework) and [OpenAI Agent Swarm](https://github.com/daveshap/OpenAI_Agent_Swarm). Their layered diagrams made it easier to think about direction flowing down and telemetry flowing up.

I borrowed that separation, then compressed it:

```text
human intent and approval
          │
          ▼
planning or synthesis
          │
          ▼
bounded collection or execution
```

This was influence, not implementation equivalence. My collectors did not become autonomous cognitive entities because I placed them below a “team lead.” The hierarchy was a way to divide responsibility and model cost.

Chapter 07 examines the ACE prototype itself, including how much of it was simulated.

## Where the diagram lied by omission

The clean three-layer drawing concealed failure propagation.

A collector could rank a weak source highly. A synthesis model could remove uncertainty while making the prose smoother. A human reviewer could approve a briefing because it looked organized. Several agents did not create independent verification; they could compound the same error.

The old chapter also claimed a roughly ten-percent false-positive rate and a fixed daily operating cost. I found no retained evaluation set or complete cost record that justified those figures, so they are no longer presented as measurements.

The safer architecture requires more than roles:

- source allowlists or explicit source review;
- immutable provenance between collection and synthesis;
- evaluation sets for relevance scoring;
- limits on files, tools, destinations, and spending;
- visible failures rather than silent fallback;
- human approval that identifies the exact effect being approved.

## Human approval is a boundary only when it has context

A checkbox is not meaningful oversight if the reviewer cannot see the sources, uncertainty, diff, and intended destination. The early approval folder improved visibility, but it did not automatically answer those questions.

I also considered auto-approving “high-confidence” items. I no longer treat model confidence as sufficient authority. Automation can be appropriate for reversible, low-consequence state changes, but the boundary should be based on permissions and impact—not on how certain a model sounds.

## What survived

The hierarchy itself was not the breakthrough. The queue was.

A queue created a pause between stages. It gave each worker a bounded input and output. It made partial failure inspectable. It allowed a human to intervene without pretending to supervise every token.

That remains the useful pattern: fewer invisible conversations between agents, more explicit artifacts between bounded steps.

---

*Next: [05 - Lessons Learned](05_lessons_learned.md)*
