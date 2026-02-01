# 04 - Multi-Agent Architecture: Hierarchical AI Systems

*February 2026*

## The Vision

"I want AI systems that collect information autonomously, and I just approve the results at the end."

This simple statement drove our architecture evolution. The key insight: **different tasks need different AI capabilities** (and costs).

## The Cost Problem

Cloud AI models are powerful but expensive. Running everything through GPT-4 or Claude would cost hundreds per day. But local models, while cheap, lack the reasoning ability for complex synthesis.

**Solution: Hierarchical specialization.**

```
┌─────────────────────────────────────────────────────┐
│  CEO (Human)                                        │
│  Role: Final approval, strategic decisions          │
│  Cost: Your time                                    │
├─────────────────────────────────────────────────────┤
│  Team Leads (Cloud Models via OpenRouter)           │
│  Role: Synthesis, quality control, report writing   │
│  Cost: ~$0.01-0.05 per report                       │
├─────────────────────────────────────────────────────┤
│  Collectors (Local Docker Models)                   │
│  Role: Data gathering, filtering, 24/7 monitoring   │
│  Cost: FREE (runs on your hardware)                 │
└─────────────────────────────────────────────────────┘
```

## Influenced By David Shapiro

We studied several frameworks:

### ACE Framework
- 100% local, no cloud
- Good for privacy, but limited reasoning
- Inspired our local collector approach

### HAAS (Hierarchical Autonomous Agent Swarm)
- Three-tier hierarchy
- "Supreme Oversight Board" at top
- Directly influenced our CEO → Team Lead → Collector structure

### GATO (Heuristic Imperatives)
- Ethical guidelines for AI
- "Reduce suffering, increase prosperity, increase understanding"
- Reminded us that AI should serve human values

## Our Implementation

### Layer 1: Collectors (Local, Free)

Topic-specific agents running on Docker:

```python
class AISecurityCollector:
    def __init__(self):
        self.model = "ai/gemma3:latest"  # Local Docker model
        self.api = "http://localhost:12434/v1"  # OpenAI-compatible

    def collect(self):
        # Fetch RSS feeds (HackerNews, Schneier, etc.)
        items = self.fetch_all_sources()

        # Use LOCAL model to assess relevance
        for item in items:
            score = self.assess_relevance(item)
            if score >= 0.5:
                self.stage_for_synthesis(item)
```

**Cost per run: $0.00** (local model, your electricity)

### Layer 2: Team Leads (Cloud, Quality)

Synthesis agents using OpenRouter:

```python
class TeamLeadProcessor:
    def __init__(self):
        self.model = "mistralai/mistral-small-creative"
        self.router = LLMRouter()

    def synthesize(self, collector_output):
        # Create executive briefing from raw findings
        prompt = f"""
        Synthesize these {len(items)} findings into an
        executive briefing for the CEO...
        """

        result = self.router.call_openrouter(
            model_id=self.model,
            prompt=prompt,
            caller="team_lead"
        )

        return self.format_for_ceo(result)
```

**Cost per report: ~$0.02** (cloud model, pay per token)

### Layer 3: CEO Approval (Human)

Reports land in `00_CEO/Pending_Approval/`:

```markdown
# AI Security Briefing

**Generated:** 2026-02-01 21:03
**Source:** Automated Collection

## Executive Summary
The most critical AI security development this week is...

## Recommended Actions
| Priority | Action | Timeline |
|----------|--------|----------|
| Critical | Audit OpenClaw deployments | 1 week |
| High | Reassess defensive AI | 2 weeks |

---
**CEO Action Required:**
- [ ] Approve for Knowledge Lab
- [ ] Mark for follow-up
- [ ] Reject
```

**Cost: Your attention** (reading and deciding)

## The Flow in Practice

```
08:00  Collector runs (cron)
       → Fetches RSS feeds
       → Local model scores relevance
       → Stages 30 items in .staging/

09:00  Team Lead runs (cron)
       → Reads staged items
       → Cloud model synthesizes
       → Creates CEO briefing

09:05  CEO checks Pending_Approval/
       → Reviews 1-2 page briefing
       → Approves/rejects
       → ~5 minutes of attention
```

**Total daily cost: ~$0.10 in API calls + 10 minutes of human time**

## Why This Works

1. **Cost efficiency**: 90% of work done by free local models
2. **Quality where it matters**: Cloud models only for synthesis
3. **Human oversight**: Nothing publishes without approval
4. **Scalability**: Add collectors for new topics easily

## Adding New Topics

Want to monitor crypto trends? Add a collector:

```python
class CryptoCollector:
    def __init__(self):
        self.model = "ai/gemma3:latest"
        self.sources = [
            "https://cointelegraph.com/rss",
            "https://decrypt.co/feed"
        ]
        self.relevance_keywords = ["bitcoin", "ethereum", "defi", ...]
```

Register with cron, and you're monitoring a new topic.

## Challenges

1. **Local model quality**: gemma3 sometimes misclassifies. We accept ~10% false positives as the cost of running free.

2. **Synthesis coherence**: Team Lead sometimes misses connections. We're iterating on prompts.

3. **Human bottleneck**: CEO approval is still manual. Considering auto-approve for high-confidence items.

## What's Next

- More topic collectors (business, legal, tech)
- Better quality scoring
- Auto-approval for routine items
- Historical trend analysis

---

*Next: [05 - Lessons Learned](05_lessons_learned.md)*
