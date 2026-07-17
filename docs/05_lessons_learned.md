# 05 — Lessons Revisited: What Survived Operational Use

> **Original reflection:** February 2026<br>
> **Editorial note, July 2026:** The first version presented several recent preferences as settled lessons. This revision keeps the observations but distinguishes measured results, working hypotheses, and conclusions that later chapters changed.

Four months into the automation workspace, I tried to summarize what had worked. Some conclusions held up: visible files, narrow components, and early security controls. Others were reactions to the most recent failure. I had abandoned dashboards, so I wrote that dashboards were unnecessary. I had moved from rules to models, so I treated model classification as the obvious answer.

Operational use made the picture less tidy.

## Simplicity was useful because it exposed the work

The first queue was Markdown. Early state lived in JSON. Shell scripts connected tools that did not yet share an interface.

That was the right level of complexity for learning. I could inspect every transition and see where assumptions broke. Redis, custom web interfaces, and deeper abstractions would have hidden an unstable process behind more infrastructure.

But “build the dumbest thing that works” is incomplete advice. A simple mechanism is useful when its failure modes are visible and acceptable. A file queue still needs duplicate handling, atomic writes, recovery rules, and an owner. Simplicity reduces the surface area; it does not remove operational responsibility.

The same applies to dashboards. Early web dashboards were overhead because I had not defined the decisions they needed to support. A later command center became useful when there were real workers, approvals, and health signals. The interface was justified by the workflow rather than by a desire to make the project look complete.

## Models helped with ambiguity, not with truth

I spent time writing keyword and filename rules for semantic categories. An LLM could handle ambiguous wording more flexibly, and that made it useful as a classifier.

The original rule of thumb—if an `if/else` chain interprets meaning, use an LLM instead—was too broad. A model adds latency, cost, non-determinism, and a new failure mode. It is appropriate when the categories genuinely require language judgment and the result can be constrained or reviewed. Deterministic rules remain better for exact formats, known identifiers, thresholds, allowlists, and effects that must be reproducible.

The stronger pattern became:

```text
code enforces the boundary
model proposes within the boundary
validation checks the proposal
human reviews consequential uncertainty
```

This principle now matters more to me than the choice of a particular model.

## Human attention was a constraint, not a metric I had solved

I wanted the daily review to take ten to fifteen minutes. The system would collect, filter, and draft; I would inspect the small set of consequential outputs.

That was a design target. I did not retain enough measurements to claim that it was consistently achieved. A model-generated quality score and a shorter approval queue did not prove that the right items reached me or that review quality remained high.

The real bottleneck was not simply human time. It was **qualified human attention at the point where an error could change the outcome**. Removing every confirmation can make a workflow feel fast while moving risk out of sight. Adding a confirmation to every low-risk step can make the system unusable.

The later approval model therefore distinguishes ordinary reading and drafting from changes to existing state, publication, spending, permissions, and effects on other people. Friction belongs where consequences begin.

## Security could not be added as a final feature

The early workspace treated prompt instructions and regex checks as more protective than they were. Later audits found broader problems: system prompts in the wrong message role, permissive browser origins, unsafe DOM rendering, unbounded history, weak secret handling, and workers with more capability than their task required.

The lasting security lesson is architectural:

- an untrusted input label does not neutralize the input;
- a model refusal is not an access-control boundary;
- logs are useful only if the relevant action is recorded;
- a local service still has a network and browser attack surface;
- an approval matters only if it occurs before the consequential effect and the human can see what will happen.

The project did not implement all of these controls from the beginning. The corrections in Chapters [03](03_security_evolution.md), [09](09_aletheia_local_agent.md), [11](11_production_reality_check.md), and [13](13_bounded_research_scripts.md) show how the assumptions changed.

## What I would repeat and what I would avoid

| I would repeat | Why |
|---|---|
| Human-readable state | Markdown, JSONL, and receipts remain inspectable without a proprietary interface. |
| Small end-to-end prototypes | A complete narrow path reveals integration failures earlier than a large design document. |
| Bounded workers | A narrow input, output, and capability set is easier to test and recover. |
| Local models as experiments | They provide control and useful specialist options when the hardware and task fit. |
| Dated corrections | They keep the learning record honest when the current architecture changes. |

| I would avoid | Why |
|---|---|
| Quality scores without calibration | Decimal precision made subjective model judgments look measured. |
| Passing model output directly into the next effect | Every handoff can propagate an error or hostile instruction. |
| Building several interfaces before stabilizing state | UI work amplified churn instead of reducing it. |
| Calling retrieval “memory” | Retrieved context, durable user facts, and model training are different mechanisms. |
| Treating local versus cloud as an ideological choice | Data boundaries, capability, traceability, cost, and latency all matter. |

## Collaboration without pretending the model learns from me

The interaction changed from issuing isolated code requests to discussing trade-offs, reviewing failures, and iterating with more context. “Pair programmer” is a useful interface metaphor for that experience.

It does not mean the model never forgets, learns from every exchange, or shares responsibility for the result. Context windows end. Provider behavior changes. Generated explanations can be wrong. Persistent learning only exists when a surrounding system deliberately records, retrieves, evaluates, or trains on prior material.

The partnership is therefore procedural rather than reciprocal in the human sense: I provide context and judgment; the model proposes and transforms; tools execute within their permissions; evidence decides whether the result survives.

## What changed after this reflection

Several February conclusions were later reversed or narrowed:

- dashboards returned when the command-center use case became concrete;
- persistent workers gave way to Hermes Cron and bounded scripts for many recurring jobs;
- local inference remained important but did not become the proven default for recurring reasoning work;
- Aletheia moved from a standalone application into a persona and co-pilot role inside Hermes;
- broad model-driven research jobs were replaced where deterministic collection was more reliable.

The work did not progress by selecting the right architecture once. It progressed by making assumptions visible enough to replace.

That is the lesson I still trust.

---

*Next: [06 — AI Agents Training](06_ai_agents_training.md)*
