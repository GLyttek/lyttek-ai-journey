# 03 - Security Evolution: The First Controls Were Not a Shield

> **Status:** Historical security account from January and February 2026. Revised in July 2026 after reviewing the retained implementation. This is not an independent security audit.

*January–February 2026*

## The report that changed the questions

An external report about exposed AI-agent installations crossed my feed. It described systems reachable from the internet with weak access controls, broad agent permissions, and exposure to untrusted instructions.

The original version of this chapter repeated an exact installation count from that report. I did not retain enough of the scan methodology to defend the number, so I removed it. The useful part was not the headline. It was the comparison it forced me to make.

My services were local rather than publicly exposed, but that did not make the workflow safe. Web pages, transcripts, and other external text moved into model prompts. The agents had useful filesystem access. Cost limits and audit trails were incomplete.

The central problem was simple: I had treated content as input without treating it as potentially hostile input.

## GOTCHA was a checklist, not a standard

I used `GOTCHA` as an internal mnemonic:

- **Goals:** define what a worker may and may not do;
- **Orchestration:** control how tasks and results move between components;
- **Threat modelling:** identify how data, instructions, and permissions can be abused;
- **Controls:** add technical and human boundaries;
- **Auditing:** retain enough evidence to reconstruct what happened.

It helped organize the review. It was not an external framework, certification, or proof of security.

## What PromptShield really did

I built a Python component named `PromptShield`. The name now sounds stronger than the implementation was.

The retained code performed four operations:

1. searched text for known phrases with regular expressions;
2. truncated content above a configured length;
3. wrapped the text in an `UNTRUSTED_CONTENT` boundary;
4. logged matches and a preview for later review.

A simplified version of the flow looked like this:

```python
for pattern, threat_type in compiled_patterns:
    if pattern.search(content):
        threats.append(threat_type)

bounded = content[:max_length]
wrapped = add_untrusted_content_boundary(bounded)
log_if_flagged(threats, wrapped)
```

This was useful as telemetry. It could flag obvious phrases such as “ignore previous instructions,” and the boundary made the intended data/control distinction explicit.

It did not sanitize language in the security sense. A model can still follow an instruction inside a delimiter. An attacker can avoid known patterns. Legitimate material discussing prompt injection can trigger the same expressions. In fact, one of the component's own test cases is an ordinary sentence about how attacks work; the regex can still flag it.

The implementation also assigned a risk score by adding fixed values for matches. That number was a local heuristic, not a calibrated probability. Logging a content preview created another question: whether sensitive input should be copied into the audit trail at all.

> **Correction, July 2026:** Pattern detection and prompt boundaries are signals, not a trust boundary. The stronger controls are capability limits, isolated execution, typed tool interfaces, validation of proposed actions, destination checks, and explicit approval for consequential effects.

## The cost limiter existed, with limits of its own

The retained `CostTracker` logged model, token, caller, and estimated cost data to JSONL. Before an OpenRouter request, the router checked whether the accumulated daily spend had reached a configured limit.

That was better than having no budget control, but it was not a transaction-safe quota system. The check did not reserve the estimated cost of the next request, so one call could exceed the remaining budget. Malformed log entries were skipped. Local inference still consumed electricity and hardware resources even when its API price was zero.

The right historical claim is therefore narrow: I added cost visibility and a pre-call stop condition. I did not prove that every execution path was bounded.

## Retiring the security score

The first chapter assigned the system scores such as `5.2/10` before and `7.2/10` after the changes. Those numbers were directional self-assessment, not measurements. They compressed unlike questions—network exposure, authorization, logging, prompt handling—into a precision the evidence did not support.

I no longer use the aggregate score as evidence. The more useful record is the control inventory:

| Area | February 2026 state | Evidentiary limit |
|---|---|---|
| Network exposure | Primarily local services | Local-only does not remove browser, local-process, or misconfiguration risk |
| Untrusted text | Regex flags and prompt boundaries | Detects some patterns; does not neutralize instructions |
| Cost control | JSONL accounting and daily pre-check | Not a hard reservation or complete resource budget |
| Audit trail | Partial event and content logging | Coverage and data-minimization were not independently tested |
| Human approval | Used for selected outputs | Not every code path had the same gate |

## The lesson that survived

The early controls were not useless. They changed the project from “accept input and hope” to “label input, record signals, and stop some obvious failures.” But the code review also showed why security language matters. Calling a regex wrapper a shield encouraged more confidence than the mechanism deserved.

The durable design rule is now:

> Treat model output as a proposal. Authority belongs to explicit code paths and people, not to the fluency of the proposal.

Later chapters document the move toward narrower permissions, local-first processing, evidence receipts, and approval gates. None of those makes the system finished. They make its remaining uncertainty easier to see.

---

*Next: [04 - Multi-Agent Architecture](04_multi_agent.md)*
