# 10 - Novaterra: What a Story Engine Could—and Could Not—Do

> **Status:** Historical creative-system case study. Revised in July 2026 after inspecting the retained code, model outputs, comparison report, and generated chapters. It does not describe the current state of the writing project.

*Original experiment: August 2024 · Story-engine build: February 2026*

## The book came before the architecture story

In August 2024, I started experimenting with a post-apocalyptic science-fiction project called “Flasstory.” The world later became Novaterra: humans and AI trying to coexist decades after a destructive war.

I used local language models for world-building and draft generation. By February 2026, the experiment had grown into a structured project with a lore bible, character files, a chapter queue, model adapters, generation scripts, and a rule-based consistency checker.

The first version of this chapter called Novaterra the blueprint for my entire multi-model workspace. That was too neat. The creative project did exercise patterns I later reused—queues, model comparison, review gates, and structured context—but the wider architecture had several influences and evolved in parallel.

## What survives in the project archive

The retained February 2026 directory contains:

```text
07_Novella/
├── LORE_BIBLE.md
├── CHARACTER_ARCS.md
├── CHAPTER_QUEUE.json
├── generate_next_chapter.py
├── generate_multimodel_comparison.py
├── engine/
│   ├── llm_backends.py
│   ├── consistency_checker.py
│   ├── character_voice.py
│   ├── scene_builder.py
│   └── story_generator.py
├── characters/
├── output/comparisons/
└── output/chapters/
```

There are nineteen retained chapter files, including revisions, covering twelve distinct chapter numbers. The latest file for each number contains roughly 34,600 words in total. That proves substantial machine-assisted output existed. It does not prove that the result was publication-ready or that every chapter passed human literary review.

The generation script could read the queue, build prompts from chapter and character data, call a configured model, run checks, save a Markdown chapter, and append a human review checklist. “Automated book generation” was therefore technically real in a narrow sense. Authorship and quality remained unresolved human work.

## The creative constraints

I used an interpretation of Viktor Frankl's paths to meaning as a thematic scaffold:

- creative value through making and repairing;
- experiential value through connection;
- attitudinal value in the face of unavoidable suffering.

These were writing constraints, not a claim that the engine implemented logotherapy or reproduced Frankl's work completely.

The same was true of character voice. Eli was prompted toward longer, metaphorical speech; Maya toward short, direct fragments; Lucas toward technical language and dark humor; Amelia toward questions and curiosity.

The old chapter called those patterns “measurable.” The archive shows explicit voice rules and checks, but no validated metric proving that readers could reliably identify every speaker. The practical test remained human: hide the character name and ask whether the dialogue is still distinguishable.

## One comparison run, not a universal ranking

On 2 February 2026, the engine generated the same opening scene with four model routes. The retained report recorded:

| Model route | Provider | Elapsed time | Output words | Checker flags |
|---|---|---:|---:|---:|
| `ministral3` | local Docker Model Runner | 35.8 s | 1,520 | 2 |
| `gemma3` | local Docker Model Runner | 13.1 s | 989 | 1 |
| `gemini-2.0-flash` | OpenRouter | 9.4 s | 840 | 1 |
| `ministral-3b` | OpenRouter | 2.3 s | 453 | 1 |

Those figures describe one scene, one machine, one prompt, and one day. They are not current performance benchmarks.

The report gave star ratings and called `ministral3` the best prose. That was my subjective reading, not a blinded evaluation. Longer output may have felt richer while also being slower and, in that run, incomplete at the end. The useful result was not a permanent model leaderboard. It was evidence that the routes produced visibly different drafts worth comparing.

## What the checker checked

The `NovaterraConsistencyChecker` was real, but narrower than “validation against the lore bible” implied. Its rules were encoded in Python. It looked for items such as:

- forbidden modern technology terms;
- a young character claiming pre-war memories;
- a character acting against a hard-coded physical constraint;
- too many distant locations appearing in one scene;
- explicit violations of selected world rules.

This could catch known contradictions. It could also produce false positives, miss paraphrases, and confuse a mention with an actual story event. A result of “no consistency issues” meant no configured rule fired; it did not mean the chapter was coherent, accurate, or good.

That distinction now shapes how I treat validation elsewhere. A checker should say what it tested, not pronounce the artifact valid.

## What transferred to the wider workspace

Novaterra made four patterns tangible:

**Structured context.** A lore bible and character files worked like domain rules: they made some constraints inspectable instead of leaving everything inside a prompt.

**Queues.** A chapter queue separated planning from generation and made progress visible.

**Model routing.** Different routes could be compared on the same bounded task rather than chosen by reputation alone.

**Human review.** Generated chapters ended in a review state. The system could produce volume; it could not decide whether the prose deserved a reader.

The analogy to business automation has limits. A fictional inconsistency and an incorrect security action do not have the same consequences. Creative freedom is useful in one context and dangerous in the other.

## The honest result

Novaterra did not prove that an automated pipeline could produce a “genuinely good” book. It proved something smaller and more useful: I could turn a world model, a chapter plan, several model backends, and a set of explicit checks into a reproducible drafting workflow.

The archive contains a long machine-assisted manuscript and the machinery that produced it. Whether that manuscript becomes literature depends on selection, rewriting, voice, and judgment beyond the engine.

---

*Part of the [Lyttek AI Journey](../README.md)*
