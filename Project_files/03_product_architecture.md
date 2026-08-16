# Product Architecture
*Part of the Knowledge Transfer Project planning series — June 2026*

---

## The Hub Model

Not a single forced pipeline but a desktop interface housing separate tools, each doing one thing well, built independently. Four tools:

- **Tool 1** — reflection layer on top of content consumption (video, podcast, book)
- **Tool 2** — prompted writing for timed reflections
- **Tool 3** — narrative and character store
- **Tool 4** — notes organisation

Build sequence: Tool 2 first — it is the simplest, it is the core mechanism the evidence log validated, and everything else feeds into or out of it. Tool 1 then wraps around consumption to feed it. Tool 3 receives its output. Tool 4 organises the whole.

---

## Product Vision

Build this for yourself first. Ignore market demand, user acquisition, and commercial viability entirely. The product question is deferred. The goal is to build something that actually works for the problem as personally experienced. If it works, the broader question reopens from a position of demonstrated insight rather than speculation.

---

## Tool Descriptions

### Tool 1 — Consumption Reflection Layer
Sits on top of video, podcast, or book content. Identifies moments of conceptual density or narrative significance and interrupts to prompt reflection before consumption continues. Voice input as an option for video/podcast. The writing and mapping process from the Musa AS session is the model — the tool is trying to engineer that process during consumption rather than leaving it as a separate step that requires additional activation energy.

**Critical design principle (from Observation 5):** The interruption must be hard, not soft. Reflection and consumption cannot run in parallel — the moment attention turns inward to process, the content being consumed is lost. The content must stop fully when a reflection prompt fires. A prompt appearing alongside playing content is not sufficient.

### Tool 2 — Prompted Reflection Writer
A timed writing interface with dynamically generated questions. Questions are not generic — they are drawn from whatever content the user just consumed or is currently reflecting on. Removes the blank page that is the primary activation energy problem. The user writes against the questions; the output is stored as a reflection entry, not a note.

The Socratic principle applies here directly: the tool does not tell the user what a lesson means. It asks questions that force them to find where it lives in their own life. You remember what you produced, not what you received.

Example questions:
- Where in your life right now does this principle apply?
- Name one decision coming up where this lesson is relevant.
- What would this character do in your situation this week?

### Tool 3 — Narrative and Character Store
Stores reflections organised around figures and characters — Musa AS, Asta, Thorfinn — rather than topics or dates. Each character accumulates encounters over time. A character functions as a retrievable identity anchor, not just a story. When you are in a hard moment you don't recall the principle of perseverance — you recall Asta. The character does the carrying.

This works across Islamic and non-Islamic sources. The mechanism is the same regardless of origin.

**Long-term direction:** A graph connecting knowledge nodes (characters → principles → personal situations) that maps to a unique identity for the user over time. This is parked — Phase 3 at earliest. Build the simple card-based store first, graph later.

### Tool 4 — Notes Organisation
Container for everything produced across the other tools. Search, tagging, retrieval by character, theme, or date.

---

## Confirmed Tech Stack

- **PyQt6** — desktop UI framework. Produces a professional-looking application, is a real framework employers recognise, and learning it is a legitimate CV line in itself.
- **Python** — backend logic. All core DSA components hardcoded manually.
- **SQLite** — local database for storing reflection entries, characters, and notes. Ships with Python, no setup required. Designing the schema is itself a useful skill.
- **Anthropic API** — question generation in Tool 2. The one place an external service is justified: generating contextual reflection questions from content is a core feature, not filler. The prompt design and context structuring is where genuine thinking is required.

---

## Hardcode vs Vibe-Code Split

The line must be drawn clearly before the build starts or it will blur under pressure.

**Hardcode manually:**
- Question generation logic and prompt engineering
- Graph data structures and traversal (Tool 3)
- Search and similarity scoring
- Core data models and schema design

**Vibe-code handles:**
- UI layout and PyQt6 boilerplate
- File I/O, saving and loading
- API call wrappers
- Config and setup

---

## First Concrete Build Task

Before touching any features: set up the project structure. Clean repo, PyQt6 installed, SQLite schema sketched for Tool 2's reflection entries. The build needs somewhere to live before anything is added to it.

**Tool 2 SQLite schema (to be designed):** Reflection entries indexed by date, content source, character/figure referenced, and questions asked. This is the first session task.

---

## Technical Architecture

### Tool 2 — Prompted Reflection Writer
String processing, question generation logic, storage structure for entries indexed by theme, character, and date.

### Tool 1 — Consumption Reflection Layer
Content parsing, tokenisation, semantic similarity scoring to identify pause points. Graph-based concept mapping for identifying which moments in content warrant reflection.

### Tool 3 — Narrative and Character Store (simple)
Card-based store first. Graph data structures for the character/principle/situation connections later.

### Tool 4 — Notes Organisation
Indexing, hashing, search algorithms.

**Key principle throughout:** Data structures will be built into the project as the build demands them, not planned in advance. The project is the context that gives each structure its purpose and character.

---

## Pre-Build Checklist (Week 1)

Three things must exist before the first feature is built. These are not pre-work — they are the first phase of development.

**1. SQLite schema for Tool 2**
What a reflection entry stores needs to be decided before any UI is built around it. Minimum fields to design:
- Content source (podcast, video, book — title and episode/chapter if applicable)
- Questions generated (stored as a list)
- Written response (the user's reflection text)
- Date and timestamp
- Character or figure referenced (nullable — not every reflection maps to one)

This schema will extend to Tool 3 and Tool 4 later. Design it with that in mind.

**2. Question generation prompt**
Tool 2 lives or dies on the quality of questions returned by the Anthropic API. The system prompt needs to be written and tested in isolation before any UI is built around it. A working API call with a prompt that reliably produces contextual, non-generic reflection questions is the proof of concept. Build and test this before touching PyQt6.

**3. Repo structure**
One repo, four modules — one per tool. Decide the folder structure before writing any code. A clean structure now prevents refactoring later. Actual structure as it stands (superseding the original suggestion below — `tool1_consumption` was renamed `tool1_contents`, `tool4_notes` renamed `tool4_actions`, and the tools were later consolidated under `/tools`):
```
/tools
  /tool1_contents
  /tool2_reflection
  /tool3_narratives
  /tool4_actions
/db
/shared
  /DSA
main.py
```

The `/db` folder holds the SQLite schema and database logic shared across tools. The `/shared` folder holds anything used by more than one tool — API wrappers, common UI components — with hand-rolled data structures (`HashMap`, `TreeNode`) isolated under `/shared/DSA`.
