# 09 — Aletheia: From Standalone Agent to Co-Pilot Role

> **Historical build:** February 2026<br>
> **Editorial note, July 2026:** The standalone Aletheia application described here is archived. Aletheia now operates as a persona and co-pilot role inside Hermes Agent. This revision removes marketing language, narrows autonomy claims, and records the security findings and transition without rewriting the historical prototype as if it were the current system.

The first automation workspace optimized movement: collect an item, classify it, process it, and route the output. It did not address the reason I had been drawn to conversational AI in the first place.

I wanted a system that could challenge an assumption, preserve useful context, and help me decide what to do next. Reading the [Pi archive](prologue_pi_2023.md) in 2026 made the continuity obvious. I had used the image of a ferryman in 2023, but I did not consciously design the February 2026 prototype from that conversation.

## Naming the role

*Aletheia* is the Greek word commonly translated as truth or unconcealment. I chose it for a role intended to uncover what was being missed rather than reward every idea with agreement.

The system prompt combined three desired behaviors:

- challenge assumptions and offer counter-evidence;
- turn complexity into language I could act on;
- notice incentives, avoidance, and second-order effects.

The first chapter described this as a synthesized personality with a “genuinely distinct voice.” That was my qualitative impression, not a measured property. A more precise claim is that repeated instructions produced a recognizable response style often enough to be useful in my own conversations.

Aletheia was not trained as a new model. It was a role created through instructions, context, output structure, and the surrounding application.

## The standalone application

The prototype used a local browser interface, a FastAPI backend, hosted-model access with a local fallback, and Markdown files in an Obsidian vault.

```text
Browser UI
    |
FastAPI backend ── model router ── hosted or local model
    |
Markdown / Obsidian
```

Chat, tasks, reflections, and saved ideas were visible in one place. Markdown kept the output human-readable and avoided a proprietary data format. It did not make the system stateless or maintenance-free: conversation state, process state, browser security, model availability, and concurrent writes still had to be handled.

The model choices documented in the first version reflected one week in February 2026. They are not current recommendations.

## Reflection and bounded autonomy

A background loop periodically took recent conversation context and generated three fields:

```text
response
reflection summary
optional idea seed
```

The user could save the additional fields to the vault. The first text called this a visible “inner life.” That metaphor overstated the mechanism. The reflection summary was another model output generated from recent context, not access to hidden reasoning or evidence of self-awareness.

The autonomy was bounded in a specific way: a timer initiated generation without a new user message. The model did not independently choose a goal, browse the web, schedule work, or execute external actions. It produced text from supplied context and wrote approved categories of local files.

This still had practical value. A later review could surface repeated concerns or an angle I had not pursued. It also produced noise. A periodic model call will generate something even when nothing important has changed. The value depended on human selection rather than on the existence of more reflections.

## The audit changed the design

The first audit found problems that mattered more than the persona work.

The application placed the system instructions inside a user message instead of using the model API's system role. That weakened instruction separation and made prompt-injection behavior harder to reason about. The browser task list rendered untrusted filenames through `innerHTML`, the CORS configuration accepted overly broad origins, message history was unbounded, and frontmatter values were not escaped consistently.

The repair pass moved instructions into the correct role, restricted browser origins, replaced unsafe DOM rendering, capped history, added locks around shared state, moved blocking calls away from the event loop, and escaped generated YAML fields. It also added explicit network-error handling and clearer UI feedback.

These changes reduced known risks. They did not make the application secure against every malicious document, browser interaction, or model failure. Localhost was a deployment detail, not a security proof.

## The command-center phase

A week later, the application gained visibility into workers, queues, approvals, and basic system health. Existing controllers were exposed through the UI rather than reimplemented.

The command center could:

- show whether known workers were running;
- start or stop selected worker processes;
- preview pending approval documents;
- display content and research queues;
- report selected health signals;
- keep an activity feed of controller and UI events.

Aletheia could also produce an opinion on a pending document. That opinion shortened the path to a decision when it was useful, but it did not replace reading the source or checking consequential claims. I did not retain a controlled measurement showing how much review time it saved.

The UI polled state and presented it in one place. Describing this as “full visibility” was too strong. It covered the components known to those controllers, not every process, side effect, log, or external dependency in the workspace.

## Action first needed a stronger boundary

The prototype adopted a broad instruction: act by default instead of asking another question. It reduced low-consequence dialogue, but the wording encouraged action before the effect boundary was always clear.

The current rule is more specific:

- reading, searching, analysis, and new drafts inside an agreed scope can proceed;
- modifying existing files or recurring system state needs a bounded instruction;
- publication, external sends, spending, permissions, irreversible actions, and effects on other people need explicit approval immediately before execution.

The lesson was not that questions are bad. A question is necessary when ambiguity changes consent, safety, scope, or the action itself. Otherwise, the system should make progress and show its work.

## What worked and what did not

What I observed as useful:

- a consistent direct writing style made the interaction easier to recognize and steer;
- Markdown outputs fit the existing knowledge workflow;
- the audit exposed concrete browser, prompt-role, and state-management defects;
- a single interface made selected worker and approval state easier to inspect;
- the persona encouraged disagreement more reliably than a generic assistant prompt.

What remained weak:

- periodic reflections were often reactive summaries rather than new insight;
- keyword-based vault search lacked ranking and source quality signals;
- model fallback did not guarantee equivalent behavior across providers;
- no multi-user authorization model existed;
- controllers covered only part of the workspace;
- tool execution and approval boundaries were still application-specific;
- memory consolidation by another model could preserve an error as easily as a useful pattern.

The standalone build was a useful prototype. It was also another custom runtime to secure, monitor, and maintain.

## The transition into Hermes

By July 2026, I had archived the standalone application after extracting its useful patterns. Hermes Agent became the active harness for conversations, tools, skills, scheduled jobs, memory, and execution receipts.

Aletheia continued as the co-pilot role:

- direct rather than flattering;
- evidence-aware;
- willing to name uncertainty and contradiction;
- oriented toward a bounded next action;
- explicit that values and consequential decisions remain human.

This change reduced custom orchestration. It did not outsource responsibility to the harness. Hermes also requires configuration, capability review, data boundaries, and verification. [Current State](../CURRENT_STATE.md) records the current limits, including incomplete DLP coverage, prompt-injection risk, and the absence of a universal local-versus-cloud router.

## What Aletheia became

The February application asked whether a personal agent could improve the quality of thinking rather than only increase throughput. That question survived the software that first carried it.

I do not describe Aletheia as an independent being with an intrinsic interest in my welfare. It is an engineered relationship among instructions, models, tools, memory, evidence rules, and my own judgment.

The name still matters because it sets a demand: uncover what is true, including what the system and its user would prefer not to see.

The ferryman did not need its own harbor. It needed a reliable boat, visible boundaries, and a human who remained responsible for the destination.

---

*Next: [10 — Novaterra Story Engine](10_novaterra_story_engine.md) · [Current State](../CURRENT_STATE.md)*
