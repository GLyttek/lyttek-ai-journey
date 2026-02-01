# 01 - Genesis: How It All Started

*October 2025*

## The Problem

As a small AI consulting company, Lyttek faced a common challenge: too much information, too little time. Every day brought:
- New AI research papers
- Security vulnerabilities
- Market trends
- Client inquiries

Manual tracking was unsustainable. We needed automation, but traditional solutions felt either too complex (enterprise platforms) or too simple (basic scripts).

## Enter Claude Code

Claude Code changed everything. Instead of writing automation from scratch, we could:

1. **Describe what we wanted** in natural language
2. **Iterate quickly** with immediate feedback
3. **Build incrementally** - start simple, add complexity

### First Conversation

```
User: I need a system that watches a folder for YouTube URLs,
      analyzes them, and saves insights to my Obsidian vault.

Claude: Let me build that for you. I'll create:
        1. A file watcher for your queue
        2. A YouTube analyzer using yt-dlp
        3. A markdown formatter for Obsidian
```

That first conversation spawned our entire automation system.

## Key Realization

**AI development is now conversational.**

Instead of:
- Writing specs → coding → testing → debugging

We now:
- Describe intent → Claude implements → test together → refine

This isn't just faster - it's fundamentally different. The AI becomes a pair programmer who never tires, never forgets context, and can explain every line of code.

## Initial Architecture

```
┌──────────────────┐
│  CONTENT_QUEUE   │  (Markdown file with URLs)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Queue Watcher   │  (Python script)
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
YouTube   Webpage
Analyzer  Processor
    │         │
    └────┬────┘
         ▼
┌──────────────────┐
│  Obsidian Vault  │  (Knowledge Base)
└──────────────────┘
```

Simple. File-based. No databases. No containers. Just Python scripts and markdown files.

## Lessons from Day One

1. **Start stupidly simple**: Our first "queue" was a markdown file. It still is.

2. **File-based is underrated**: JSON/JSONL files beat databases for small scale. Easier to debug, version, and understand.

3. **Obsidian as Knowledge Base**: Using a note-taking app as our database sounds crazy, but it works. Everything is searchable, linkable, and human-readable.

4. **Claude Code as primary interface**: We rarely touch the code directly anymore. Claude reads, writes, and refactors. We describe intent.

## What Came Next

With the basic pipeline working, we started asking: "What else can we automate?"

- Research queries
- Content writing
- Security monitoring
- Trend analysis

Each became a new "worker" in our system. Each built conversationally with Claude.

---

*Next: [02 - First Automation](02_first_automation.md)*
