# 07 - ACE Framework Exploration: A Prototype, Not an Autonomous Mind

> **Status:** Historical learning experiment. Revised in July 2026 after inspecting the retained `ace.py` and `ace2.py` implementations.

**Date:** February 2025

**Source:** David Shapiro's [ACE Framework](https://github.com/daveshap/ACE_Framework)

## Why I explored ACE

The Autonomous Cognitive Entity framework offered a vocabulary for separating values, strategy, planning, and execution. At the time, that was attractive because my scripts were beginning to form a workspace without a clear model of who—or what—was allowed to decide.

ACE described six layers:

| Layer | Intended responsibility |
|---|---|
| Aspirational | Mission, ethics, and values |
| Global Strategy | Long-term direction and environmental model |
| Agent Model | Capabilities and limitations |
| Executive Function | Planning and resource allocation |
| Cognitive Control | Selecting the next task |
| Task Prosecution | Performing the selected action |

A northbound/southbound bus carried status upward and directives downward. I wanted to see whether the abstraction made agent behavior easier to reason about.

## What I built

Two experimental versions survive in the archive: `ace.py` and `ace2.py`. The second version defined all six layer classes, a message bus, a final integration layer, and an integrity check.

The bus itself was ordinary Python state:

```python
class Bus:
    def __init__(self):
        self.northbound = []
        self.southbound = []

    def publish_northbound(self, message):
        self.northbound.append(message)

    def publish_southbound(self, message):
        self.southbound.append(message)
```

The important correction is what happened behind those layers.

Five layers called a function named `simulate_llm_call`, which returned the prompt with a model label. The task-prosecution layer attempted a local Ollama request and fell back to the same simulated response if the request failed. The final integration step was simulated as well.

So the prototype exercised control flow and message passing. It did not demonstrate six independently reasoning agents, persistent autonomy, or a reliable ethical hierarchy.

## What the prototype taught me

### Separation helped readability

Giving goals, planning, and execution different names made hidden assumptions visible. A task runner should not silently invent its own mission. A planning step should not automatically receive every tool permission.

### A bus is not governance

Messages moving north and south do not prove that higher-level constraints are enforced. In the prototype, the “aspirational” layer produced text. No deterministic policy engine checked whether later output complied with it.

### Layer count increased ceremony quickly

For a small task, six classes and a final integration step created more places for state, prompt drift, latency, and failure. The architecture looked sophisticated before it had earned that complexity.

### Simulation was useful—and easy to misread

Using simulated calls let me test the shape of the program without depending on six working model endpoints. That is a legitimate prototyping technique if it remains visible. The earlier chapter did not make the simulation boundary clear enough.

## How ACE influenced the later workspace

The later collector–synthesis–approval workflow borrowed a loose three-part separation:

```text
human intent and approval
          │
          ▼
planning or synthesis
          │
          ▼
bounded execution
```

This is an analogy, not a claim that a human CEO equals ACE's Aspirational Layer or that a collector implements Task Prosecution in the framework's full sense.

The durable influence was simpler:

- goals should be explicit;
- planning and execution should not share unlimited authority;
- lower layers should return evidence rather than only conclusions;
- the human boundary should remain outside the model hierarchy.

## What was missing

The prototype had no persistent state model, formal policy enforcement, authorization layer, evaluation suite, or adversarial test harness. Its integrity check counted messages and printed “All systems nominal”; it did not test semantic integrity.

That gap became the main lesson. Architecture diagrams describe intended responsibility. Tests, permissions, and receipts show whether the responsibility is actually enforced.

## References and code

- [ACE Framework](https://github.com/daveshap/ACE_Framework)
- [OpenAI Agent Swarm / HAAS](https://github.com/daveshap/OpenAI_Agent_Swarm)
- [Public experimental code collection](https://github.com/GLyttek/myscripts)

---

*Part of the [Lyttek AI Journey](../README.md)*
