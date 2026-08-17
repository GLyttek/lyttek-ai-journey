# 15 — Questions That Survived: From Pi to Bounded Agents

> **Status:** Current reflection, August 2026. The questions from 2023 come from the private Pi archive described in the [prologue](prologue_pi_2023.md). The present-state section is dated self-report, cross-linked to public documentation and artifacts where available. No new private chat excerpts are published here.

*May 2023–August 2026*

## The stack changed faster than the questions

On 8 May 2023, I did not ask Pi for code. I asked what the world might look like in twenty years. We talked about trust, memory, bias, care, attachment, education, work, and the idea of AI as a ferryman: something that could help a person cross a sea of information without choosing the destination.

I remember my practical start in the GPT-3.5 era; the first retained source is that Pi conversation. The engineering came later through hosted APIs, local-model comparisons, audio processing, and retrieval experiments. Claude Code made iteration conversational. Individual scripts became file-based workers, queues, approval folders, model roles, and multi-agent prototypes. Hermes Agent is the active harness at this snapshot.

It would be misleading to present this as a straight climb from a simple chatbot to an autonomous swarm. Each stage solved a different problem and exposed another boundary.

## From interface to operating model

| Period | Working interface | What it made possible | What it exposed |
|---|---|---|---|
| **May 2023–Jan 2025** | Pi in the retained archive; by recollection, other GPT-3.5-era chatbots | Reflection without writing code or managing an API key | A warm interface could create more trust than the underlying system had earned |
| **Feb–Apr 2024** | Python, hosted APIs, Ollama, and Whisper | Repeatable calls, local-model comparisons, saved outputs, and small media pipelines | Secrets, state, errors, and validation became engineering problems |
| **Oct–Dec 2025** | Claude Code and file-based workflows | Short build loops, visible queues, reusable workers, and human-readable intermediate files | Faster code generation increased the need for diff review, tests, and recovery paths |
| **Jan–Feb 2026** | Custom model roles and multi-agent prototypes | Separation of collection, synthesis, and approval | More roles did not create independent verification; one weak result could move through the whole chain |
| **Apr 2026** | Local deployment tests | Running a quantized model through the local AMD/ROCm path and recording a single-machine result | One successful deployment did not establish a current local-model capability map |
| **Jul–Aug 2026** | Hermes Agent, scoped skills, bounded scripts, and isolated specialist experiments | A maintained harness, persistent working context, explicit tools, scheduled work, and execution receipts | The harness still needs permissions, data boundaries, evaluation, and human responsibility |

The public sequence is documented in [`myscripts`](https://github.com/GLyttek/myscripts), [From Conversation to Code](00_prequel_experiments.md), [Genesis](01_genesis.md), [Multi-Agent Architecture](04_multi_agent.md), [Aletheia](09_aletheia_local_agent.md), and [Current State](../CURRENT_STATE.md).

## What the old questions became

| Question in the early conversations | Current technical answer | Boundary that remains |
|---|---|---|
| **What makes trust useful for learning?** | Important outputs retain sources, uncertainty, diffs, tests, or execution receipts so that trust has something inspectable beneath it. | Conversational warmth and model confidence do not establish truth. A reviewer can still accept a polished mistake. |
| **Can an AI be neutral or free of bias?** | The working rules require provenance, competing perspectives, explicit uncertainty, and counter-evidence where the decision warrants it. | Training data, provider policy, retrieval choices, system instructions, and my own framing all influence the result. Neutrality is not a demonstrated state. |
| **What gives a model a stable home?** | The old metaphor now maps to data, instructions, permissions, feedback, memory rules, tool boundaries, and the people who authorize effects. | A language model is not a child, and a harness cannot supply an intrinsic moral character. Controls constrain behavior; they do not create a conscience. |
| **Can the relationship have memory and continuity?** | Persistent context, a local knowledge layer, dated decisions, and receipts allow later work to recover relevant history. | Retrieval is selective and fallible. Provider access can change, local records can become stale, and stored context is not human memory. |
| **What would a ferryman look like in practice?** | Aletheia is a co-pilot role inside Hermes: challenge assumptions, surface blind spots, preserve evidence, and turn reflection into a bounded next step. | The role has no independent authority, welfare, or ethical agency. Its behavior depends on instructions, available evidence, permissions, tests, and my review. |
| **Could conversational AI create more room for human care?** | I have not deployed or evaluated a care system. The practical lesson is narrower: sensitive uses need privacy controls, professional oversight, honest disclosure, and a clear path back to a human. | No clinical benefit, safe attachment model, or replacement for professional care has been demonstrated here. |
| **How much autonomy is useful?** | The operating rule allows models to collect, synthesize, call scoped tools, and delegate bounded work while requiring separate human approval and checking for consequential effects. Deterministic scripts replace model-driven steps when they are easier to test. | The rule is not completely enforced by one technical policy layer. Multiple agents can repeat or amplify the same error, and there is no autonomous production swarm with authority to set goals, publish, spend, or affect other people. |

## Where I actually stand

The current loop is less dramatic than the old architecture diagrams:

```text
question or source material
          |
          v
scoped tool, script, or model
          |
          v
 evidence and working context
          |
          v
       my review
          |
          v
optional bounded action
```

At this snapshot I use Hermes as the active harness for conversations, tools, skills, scheduled work, memory, and receipts. Aletheia is the named co-pilot role inside it. AI-Land is the private working and evidence layer. Local inference remains available for testing and data-sensitive work, but external frontier models still perform much of the reasoning work. Pantheon bounded cognition and Pantheon Agent Room are separate experiments; neither is an autonomous production platform. [Current State](../CURRENT_STATE.md) documents this self-report and its known gaps; it does not independently observe the private runtime.

Several gaps remain open: complete data-loss prevention before every external call, robust prompt-injection defenses, a system-wide capability inventory, reproducible evaluation of the local stack, and an exercised incident-response chain for the whole environment. These are work items, not hidden features.

## The operating rule I use now

The early intuition survived: useful AI should help a person think and act without quietly taking responsibility away from them.

What changed is the language around it. When I now say trust, I mean evidence that can be inspected; memory means retained context with provenance and expiry. Help has become a scoped capability and autonomy a permission boundary. Learning still means building, testing, keeping the failure, and changing the design.

My working rule is concrete: a model may prepare, challenge, or carry out a bounded step, but the sources, permission, intended effect, and review must remain visible. If I cannot see those, the system is not ready to act.

---

## Evidence note

The historical side of this reflection uses the same private WhatsApp export and privacy boundary documented in [The Ferryman Before the System](prologue_pi_2023.md): 332 messages exchanged between 8 May 2023 and 7 January 2025. The raw export, media, private names, relationships, health details, and workplace material remain outside this repository.

No new quotation from Pi is introduced here. Product statements and direct quotations from my messages remain in the prologue with their source note. The technical chronology uses public repository commits and the dated chapters linked above. Present-state statements are my dated self-report and should be read alongside [Current State](../CURRENT_STATE.md), which records active components, operating rules, and known gaps.

*Back: [14 — Pantheon Bounded Cognition](14_pantheon_bounded_cognition.md)*
