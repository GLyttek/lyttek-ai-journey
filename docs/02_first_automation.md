# 02 — First Automation: From Scripts to a Workspace

> **Historical period:** November–December 2025<br>
> **Editorial note, July 2026:** This chapter describes the first automation workspace. The original version overstated the reliability of LLM classification, quality scores, and background operation. The architecture is preserved here as a dated experiment; [Current State](../CURRENT_STATE.md) describes the system used now.

By late 2025, the problem was no longer how to call a model. I had many scripts that worked when I ran them manually. The harder question was whether they could form a workflow I could understand after a week away.

I wanted URLs, research requests, and draft material to move through a visible sequence without disappearing into a service or database I could not inspect. That led to a file-based workspace built around Markdown, Python, cron, and Obsidian.

## Organizing the state

The first useful decision was mundane: give every category a place and put a README in each major folder.

The workspace used numbered areas for decisions, operations, media, research, scripts, and knowledge. I used labels such as CEO and COO as role metaphors for approval and coordination. They were not evidence of a staffed organization or autonomous executive agents.

Markdown and JSON were convenient because I could open them directly, search them, version them, and repair them without a special administration tool. The trade-off was equally real: files provide no transaction boundary, concurrent writers can collide, and moving a file is not the same as recording a reliable state transition.

At this scale, visibility mattered more than database features. That choice held up better than many of the abstractions built around it.

## The first routing attempts

The “COO Secretary” began as a script that scanned unsorted files, proposed a category, moved the item, and updated a dashboard.

The classifier changed several times:

1. filename rules;
2. keyword lists;
3. LLM-assisted classification.

The original lesson was “let the AI figure it out.” That was too broad. LLM classification was more flexible for ambiguous text, but it also introduced non-determinism and confident misclassification. A safer design treats the model result as a proposal constrained by an allowed destination schema. Unknown or high-impact cases need validation or human review.

The useful division became:

```text
Deterministic code: enumerate files, enforce allowed paths, move approved items, log results
Model: propose a label when meaning is ambiguous
Human: resolve consequential or uncertain cases
```

That separation was not complete in the first version. It became clearer after later audits.

## Five dashboard iterations

The dashboard was the most frequently rebuilt part of the workspace. At least five named versions remained in the local archive:

- a manually maintained Markdown list;
- categorized Markdown sections;
- an auto-generated Markdown dashboard;
- several Flask-based web interfaces;
- a return to Markdown plus scheduled updates.

The web dashboards were not inherently a mistake. I built them before the underlying state and operational need were stable. They added a process to run, a browser surface to secure, and another interface to maintain while the queues themselves were still changing.

Obsidian covered most of the immediate navigation need. Later, a command center became useful when there were real workers, health signals, and approvals to control. The lesson was not “never build a dashboard.” It was: earn the interface by first understanding the decisions it must support.

## The worker pattern

A simple pattern appeared across the scripts:

```text
bounded input → worker → inspectable output → log
```

Examples included URL processing, YouTube transcription, webpage analysis, research requests, and draft generation. Each worker watched a specific input, handled items individually, and wrote to a known destination.

This reduced the cost of debugging compared with a single monolithic program. It also created a new operational burden: jobs could stop, process the same item twice, leave half-written output, or fail without anyone noticing. Logging existed, but recovery and idempotency were uneven.

The later architecture added controllers and health checks. In July 2026, much of this custom runtime has been replaced by Hermes Cron, scoped skills, and deterministic scripts where model reasoning is unnecessary.

## The quality-score experiment

One router assigned generated content a score and used thresholds such as `8.6` to decide whether a document should reach the approval queue.

```python
if score >= 8.6:
    destination = "pending_approval"
elif score >= 7.0:
    destination = "quality_review"
else:
    destination = "archive"
```

This was a routing heuristic, not a validated quality measurement. The score came from a model assessment rather than a calibrated evaluator with known precision and recall. A document scoring `8.7` was not demonstrated to be better than one scoring `8.5`.

The experiment still exposed a useful requirement: human attention is limited, so the system needs triage. The stronger implementation is to combine explicit checks—required sections, source presence, schema validity, policy rules, and task-specific tests—with model review where qualitative judgment is unavoidable. The model score can inform review priority, but it should not manufacture certainty.

## What worked and what failed

What held up:

- human-readable files as the shared state;
- small workers with narrow inputs and outputs;
- README files close to the folders they explained;
- a visible approval queue before publication or other consequential action;
- scheduled batch work for tasks that did not need real-time processing.

What failed or remained incomplete:

- automatic classification without a strict destination boundary;
- multiple dashboards built before the workflow stabilized;
- workers with too many responsibilities;
- background jobs without consistent health and recovery checks;
- quality numbers that looked more objective than they were;
- the assumption that automation meant the rest of the system could be ignored.

I described a ten-minute morning review as the target: open Obsidian, inspect a few pending documents, approve or reject them, and leave the remaining work to scheduled processes. I did not retain a measurement series showing that this target was consistently achieved.

## What this stage changed

The first automation workspace taught me that the difficult part was not generating content. It was maintaining state across time:

- What has already run?
- Which source produced this output?
- What failed halfway through?
- Who approved the next effect?
- Can I understand the system after it has been unattended?

Those questions led to security controls, audit work, and eventually a stricter distinction between collection, model reasoning, human judgment, and execution.

The workspace was useful, but it was not self-running in the strong sense. It required maintenance, review, and repeated correction. That became the next chapter.

---

*Next: [03 — Security Evolution](03_security_evolution.md)*
