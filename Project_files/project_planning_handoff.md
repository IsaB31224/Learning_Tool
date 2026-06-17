# Project Planning — Session Handoff
*Compiled from conversation session — June 2026*

---

## Who John Is (Context for Planning)

- First-year CS student, University of Leeds
- CV arc so far: **Cambridge Battlecode** (learned to build fast, first exposure to agentic systems, where vibe-coding started) → **Leeds AI Hackathon** (built Prompt Sustainability Analyzer using Anthropic API, learned product thinking and pitching)
- The **missing layer** identified: technical depth / DSA. CV has breadth but lacks demonstrated algorithmic ability.
- Placement applications typically happen October/November of second year — roughly 16 months away
- DSA baseline: understands stacks, queues, linked lists, arrays, hash maps as concepts from COMP1860/1870. Has implemented a hashmap once. NeetCode roadmap is known but not yet worked through.

---

## The Summer Decision

**Primary commitment: personal project + DSA practice**
**Secondary: applied to IHSAAN Summer Internship Programme (no cost, good backup)**

Reasoning:
- The window between year 1 and year 2 is the right time to build technical depth
- Placement interviewers need to see a self-initiated project with genuine technical decisions, not just professional experience
- The knowledge transfer project is in an observation phase — not yet ready to build — but the build phase belongs this summer
- Internship applications cost nothing; if one comes through it fits within the summer without crowding out the project

---

## The Project — Full Intellectual Foundation

### The Problem (as diagnosed)

Islamic knowledge consumed through YouTube lectures doesn't transfer into behaviour. The pattern:
- A lecture is watched, a principle is understood in the moment
- Within days or weeks it is functionally gone — not retrievable, not shaping behaviour
- Exception: something that struck emotionally remains retrievable, and through it the broader content sometimes becomes accessible

**The gap is not retention of information. It is situational recognition** — knowing in the moment that you are in a situation where a piece of knowledge applies. The knowledge sits dormant rather than absent. It is underused, not uncovered.

### The Key Insight

Abstract models fade. Embodied characters persist.

When tawakkul is presented as a framework it doesn't stick. When Musa AS reaches the sea with Pharaoh's army behind him — that sticks. Not because the principle changed but because it is now carried by a person, a story, a dramatic moment with emotional weight and consequence.

The Quran itself teaches this way — not primarily through propositions but through narrative, character, and dramatic situation. The Seerah works the same way. There is a reason these have transmitted across 1,400 years while most lectures don't survive the week.

**The mechanism:** Emotional charge → narrative memory → knowledge retrievable in situation → behaviour change. The emotional anchor is not a bug — it is the mechanism through which knowledge transfers at all.

### Why Existing Tools Don't Solve This

- **Anki / Readwise** — assume the problem is forgetting propositional content. Solve it with spaced repetition of propositions. But the issue is the knowledge was never narratively embodied in the first place, so it has no situational grip. Repeating a proposition more frequently doesn't make it behaviourally accessible.
- **Notion / Obsidian** — store propositions, not narratives
- **Lecture summarisers** — compress propositions
- **Habit trackers** — monitor behaviour without addressing the knowledge-to-behaviour gap

**The differentiator:** This is a narrative embodiment problem, not a retention problem. The solution should look different from all of the above.

### The Al-Ghazali Foundation

Al-Ghazali's framework in the *Ihya* distinguishes between:
- Knowledge that benefits the hand — instrumental, immediately applicable
- Knowledge that forms the person — shapes observation, character, response over time

The *Ihya* is partly a critique of scholars who accumulate propositional knowledge without transformation. The problem he diagnosed institutionally in 11th century Baghdad is the same problem experienced personally watching YouTube lectures in 2026. The gap between knowing and being changed is not new — the scale of content consumption makes it more acute.

Transformation requires knowledge internalised at the level of character, not just stored at the level of proposition. Character is shaped by narrative and example — hence the Quran's method.

### What To Build — The Three Load-Bearing Words

Something that helps transfer content and knowledge through **reflection** into something that can be held and remembered as a **narrative** over a **timeframe**.

- **Reflection** — the middle step between consumption and transfer. The conversion process from proposition to personal meaning.
- **Narrative** — the output isn't a note or flashcard. It holds knowledge in a form with emotional grip — a story, a character, a moment — retrievable not just as information but as lived understanding.
- **Timeframe** — not a single-session tool. The narrative accumulates. What Musa AS means to you in six months is built from multiple encounters. The tool should hold that accumulation and make it visible.

### What This Is Not

- Not a note-taking app (Notion, Obsidian) — those store propositions
- Not a spaced repetition tool (Anki, Readwise) — those repeat propositions
- Not a lecture summariser — that just compresses propositions
- Not a habit tracker — that monitors behaviour without addressing the knowledge-to-behaviour gap
- Not trying to Islamicise a productivity app — trying to recover a pedagogical method the tradition itself used

---

## Open Questions Still Unresolved (as of this session)

John was mid-answering a question set when this session ended. These remain open:

1. **Where is John in the observation phase?** — Has he started logging real moments, or is that still ahead of him?
2. **What's the honest product vision?** — Personal tool, small community tool, real product for Muslims broadly, or primarily a technical portfolio piece?
3. **Which technical direction feels most interesting?**
   - Spaced repetition engine built from scratch
   - Semantic search / RAG over Islamic content
   - Narrative graph connecting knowledge nodes
   - Not sure yet

These should be the first three questions in the next planning session.

---

## Technical Architecture Options (discussed but not decided)

Each of these would teach real DSA through the build:

**Option A — Custom Spaced Repetition Engine**
Build the scheduling algorithm from scratch rather than using Anki's algorithm. Teaches: graph traversal, scheduling algorithms, priority queues. Maps to NeetCode: trees, heaps, graphs.

**Option B — Semantic Search Layer over Islamic Content**
Build a retrieval system that lets users query Quranic/hadith content by meaning, not keyword. Teaches: vector embeddings, similarity search, how RAG works at implementation level. Maps to NeetCode: arrays/hashing (the indexing structures), plus systems thinking.

**Option C — Narrative Graph**
Connect knowledge nodes (Prophets, principles, stories) in a graph structure that shows relationships and accumulation over time. Teaches: graph data structures, traversal, possibly recommendation logic. Maps to NeetCode: graphs, BFS/DFS.

**Key principle agreed:** Wherever possible, make architectural choices that touch DSA — build the core engine yourself before reaching for a library. The goal is DSA learning through the build, not just a finished product.

---

## Proposed Summer Structure (3 phases, ~12 weeks)

**Mornings — DSA practice (protected, non-negotiable)**
Follow NeetCode roadmap. 1-2 problems daily minimum. Don't skip for project work.

**Afternoons/Evenings — Project build**

### Phase 1 — Weeks 1-4
- NeetCode: Arrays, Hashing, Two Pointers, Sliding Window
- Project: Design the architecture, make core decisions, get a basic working version running
- Observation phase: Start logging real moments in phone notes (one or two sentences, no structure required)

### Phase 2 — Weeks 5-8
- NeetCode: Trees, Graphs, BFS/DFS
- Project: Build the technically harder parts — the spaced repetition engine or search layer
- This is where DSA learning directly feeds the build

### Phase 3 — Weeks 9-12
- NeetCode: DP basics, review and consolidate
- Project: Polish to something you'd actually show someone. Write up what you built and why.

---

## Observations Still To Make (from the project MD file)

*These should be noted in real time, not theorised in advance. Phone notes — one or two sentences per observation, no structure required.*

- When does knowledge fail to transfer? Note the specific moment — what was consumed, what the situation was, where the gap appeared
- When does knowledge successfully transfer? What was different — emotional charge, telling someone else, encountering the situation soon after learning?
- Which Islamic characters or stories are already functioning as behavioural models? What made them stick?
- In which situations do you find yourself thinking "I know something relevant to this but can't access it"?

---

## Placement Context (why this summer matters)

For placement applications (October/November second year), the strongest profiles at John's level have:
1. Something self-built (shows initiative and technical ability)
2. Something done in a real organisation (shows professional function)
3. A coherent story connecting them

The knowledge transfer project — if built with real technical decisions — satisfies (1). The story connecting it to John's broader interests in Islamic knowledge transmission and CS satisfies (3). The IHSAAN internship, if it comes through, satisfies (2).

For top placements (Google, Microsoft, Palantir): the project's technical depth matters most.
For good-but-not-top placements (mid-size tech, consultancies, AI startups): project + internship combination is close to ideal.

---

## Broader Intellectual Context (relevant to project framing)

From the Islamic intellectual conversations MD file — the project sits within a larger diagnosis:

- British Muslim communities have a **translation layer problem**: deep traditional Islamic knowledge exists but there is no infrastructure converting it into frameworks for navigating modern life
- The madrasa system is designed to **preserve and transmit** knowledge, not generate new application in novel environments
- The knowledge transfer tool is a **micro-instance** of this larger problem — the same gap that exists institutionally (knowledge not applied to modern problems) exists individually (knowledge not applied in daily situations)
- This connection may sharpen the product vision: the tool isn't just a personal productivity app, it's an attempt to recover a pedagogical method the tradition itself used

---

*Next session should start with the three open questions above, then move into concrete project architecture decisions.*
