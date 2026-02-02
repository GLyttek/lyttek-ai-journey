# 07 - ACE Framework Exploration

**Date:** February 2025
**Status:** Learning Experiment
**Source:** David Shapiro's ACE Framework

---

## What is ACE?

The **Autonomous Cognitive Entity (ACE)** Framework is a layered architecture for building autonomous AI agents. Created by David Shapiro, it provides a conceptual model for how AI systems can operate with increasing levels of autonomy.

## The Six Layers

```
┌─────────────────────────────────────────┐
│ Layer 1: ASPIRATIONAL                   │
│ Mission, ethics, values                 │
├─────────────────────────────────────────┤
│ Layer 2: GLOBAL STRATEGY                │
│ Long-term planning, environmental model │
├─────────────────────────────────────────┤
│ Layer 3: AGENT MODEL                    │
│ Self-awareness, capabilities            │
├─────────────────────────────────────────┤
│ Layer 4: EXECUTIVE                      │
│ Task planning, resource allocation      │
├─────────────────────────────────────────┤
│ Layer 5: COGNITIVE                      │
│ Task execution, problem-solving         │
├─────────────────────────────────────────┤
│ Layer 6: TASK PROSECUTION               │
│ Direct action execution                 │
└─────────────────────────────────────────┘
```

## Communication: The Bus System

ACE uses a **Northbound/Southbound Bus** pattern:

- **Northbound (↑)**: Status, telemetry, summaries flowing up
- **Southbound (↓)**: Directives, strategies, commands flowing down

```python
class Bus:
    def __init__(self):
        self.northbound = []  # Upward messages
        self.southbound = []  # Downward messages

    def publish_northbound(self, message: str):
        self.northbound.append(message)

    def publish_southbound(self, message: str):
        self.southbound.append(message)
```

## Our Implementation

We built two experimental versions:

### ace.py - Basic Implementation

Simple layer classes with bus communication:

```python
class AspirationalLayer(Layer):
    def process(self, input_data=None):
        mission = (
            "Mission: Prioritize reducing suffering, "
            "increasing prosperity, and expanding understanding."
        )
        self.bus.publish_southbound(f"[{self.name}] {mission}")
        return mission
```

### ace2.py - Enhanced Version

Added more sophisticated layer interactions and state management.

## Key Learnings

### 1. Separation of Concerns

Each layer has a specific responsibility. The Aspirational Layer doesn't care about implementation details; the Task Prosecution Layer doesn't set ethical guidelines.

### 2. Hierarchical Control

Higher layers set constraints for lower layers. A directive from Layer 1 (ethics) overrides optimizations from Layer 4 (execution).

### 3. Autonomous Operation

Each layer can operate independently, making decisions within its scope without constant supervision.

### 4. Practical Limitations

In practice, we found:
- Full 6-layer implementation is complex for simple tasks
- Most business use cases need only 2-3 layers
- The bus pattern adds overhead for small systems

## How This Influenced Our Architecture

Our production system uses a simplified version:

```
CEO (Human)        ≈ Layer 1: Aspirational
Team Leads (Cloud) ≈ Layer 4: Executive
Collectors (Local) ≈ Layer 6: Task Prosecution
```

The key insight: **You don't need all 6 layers.** Use what makes sense for your use case.

## References

- [ACE Framework GitHub](https://github.com/daveshap/ACE_Framework)
- [David Shapiro's YouTube](https://www.youtube.com/@DavidShapiroAutomator)
- [Original HAAS Paper](https://github.com/daveshap/OpenAI_Agent_Swarm)

## Code Location

Experimental implementations: [myscripts/llm-experiments](https://github.com/GLyttek/myscripts)

---

*Part of the [Lyttek AI Journey](../README.md)*
