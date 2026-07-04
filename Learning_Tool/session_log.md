# Session Log
*Running log of build sessions — most recent at top*

---

## Session 9 — July 2026

### What was done
- Confirmed `hashmap_initialise()` is wired into app startup: `main.py` calls `init_db()` then `Hash.hashmap_initialise()` (via the `Hash` singleton instance created in `medium.py`) before the `QApplication`/`MainWindow` are constructed
- Reviewed `get_character_name()` in `db/database.py` — confirmed it returns all reflection rows for a given character

### State of the code
- Hashmap population at startup — confirmed wired and working, no longer outstanding

### Next session
- Begin thinking through UI for reflection retrieval

---

## Session 8 — June 2026

### What was done
- `get_all_character()` written in `db/database.py` — queries all unique character names from Reflections table using `SELECT Character_referenced FROM Reflections GROUP BY Character_referenced`, returns a list of tuples
- `hashmap_initialise()` written in `shared/hashmap.py` — calls `get_all_character()`, loops over results, unpacks each tuple with `[0]` to extract the name string, calls `hash_insertion` for each character

### Concepts learned
- Cursor vs data — `conn.execute()` returns a cursor (a pointer hovering over results), not the results themselves; `fetchall()` is what pulls the rows into a Python list. Without it, the cursor dies when the `with` block closes and the return value is unusable
- `commit()` on SELECT — `commit()` persists a write to disk; SELECT doesn't write anything so it doesn't need one
- `get_connection` vs `get_connection()` — referencing a function vs calling it; leaving off the parentheses passes the function object itself, not the connection it returns
- Tuple indexing — `character[0]` extracts the string from a single-element tuple; `str(tuple)` converts the whole tuple to a string literal, which is wrong

### State of the code
- `get_all_character()` — complete in `db/database.py`
- `hashmap_initialise()` — complete in `shared/hashmap.py`
- `hashmap_initialise()` not yet wired into app startup — hashmap is still empty when the app launches

### Next session
- Wire `hashmap_initialise()` into app startup so the hashmap is populated before anything tries to read from it
- Begin thinking through UI for reflection retrieval

---

## Session 7 — June 2026

### What was done
- Hash map class designed and implemented in full
- `__init__` method: array of 100 slots initialised to None
- `hash_insertion(character_name)` implemented — hashes character name to index, creates new dictionary at slot if empty, adds character as new key if collision (separate chaining)
- `read_character(character_name)` implemented — hashes to index, returns reflection tuples via dictionary lookup, handles missing key with try/except KeyError
- `delete_reflection(character_name, reflection_id)` implemented across two layers:
  - Hashmap layer: reads character reflections, takes user input for reflection ID, removes matching tuple from list using list.remove()
  - Database layer: `delete_reflection(character_name, reflection_id)` in database.py executes DELETE SQL query and commits the change to SQLite

### Design decisions
- Separate chaining used for collision handling — dictionary at each array slot holds multiple characters keyed by name
- read_character returns rather than prints to support downstream use by delete and UI
- Database delete uses two ? placeholders in a single tuple — safe parameterised query, prevents SQL injection
- No return value from database delete function — nothing meaningful to return from a DELETE operation

### Concepts learned
- try/except for KeyError handling — why if/else can't catch exceptions that halt execution  
- conn.execute() vs conn.commit() — execute sends the SQL, commit persists it to disk
- ? placeholders in SQLite queries — parameterised queries and why they exist
- list.remove() for in-place list mutation — why loop variable reassignment doesn't modify the underlying list

### State of the code
- Hash map class: __init__, hash_insertion, read_character, delete_reflection all implemented
- Database delete function implemented in database.py
- No UI layer yet — methods untested end to end

### Next session
- Connect hash map population to SQLite at startup
- Begin thinking through UI for reflection retrieval

---

## Session 6 — June 2026

### What was done
- UI colour theme implemented across `tool2_reflection/ui.py`
- Dark theme applied via single `_STYLESHEET` constant — cascades to all widgets

### Design decisions
- Background: near-black `#0f111a`
- Input boxes: dark navy `#1c2233`, subtle blue border, brightens to solid blue on focus
- Question displays (read-only): 14px bold text, light blue `#93c5fd`, permanent solid blue `#3b82f6` border — visually distinct from writable boxes
- Buttons: bright blue `#2563eb`, bold, rounded corners, hover/press states
- Confirm & Save button: green `#059669` to distinguish it as the terminal action
- Labels: light blue `#93c5fd`
- Scrollbar: thin 8px, blue handle
- Metadata confirmed border updated from plain green to `#10b981` to match the theme

### State of the code
- Dark theme complete and validated
- Two-call pipeline complete and tested
- All prompt fixes done
- UI colour theme done

### Next session
- No outstanding items — full re-test of the tool end to end after all prompt and UI changes

---

## Session 5 — June 2026

### What was done
- Full two-call pipeline tested end to end with real content
- Call 1 and Call 2 both validated against a real reflection session
- Four improvement areas identified from the test and logged as evidence

### Test results
- Pipeline ran cleanly — both calls fired, questions generated, final question returned
- Call 2 final question quality confirmed: surfaced the unconscious belief correctly, landed at the right level
- Four areas identified for next iteration:

1. **Question 1 format** — Question referenced the user being at work; user does not work. General theme (family) was applicable but the specific situation was assumed rather than forced out. Question 1 must not suggest specific situations — it must make the user surface one themselves.
2. **Visual design** — UI colour theme is too uniform. Colour scheme to be dictated by John and implemented next session.
3. **Final question missing action prompt** — User wrote the actions they needed to take unprompted, but the final question did not ask for them. The final question prompt needs something that forces the user to name a concrete action.
4. **Situation recollection** — When narrating an event, the user naturally drifted into general flow rather than exact specifics. Forcing specifics (exact calls, exact moments) was what surfaced what was truly going on. Explicit situation recollection needs to be built into the prompting.

### State of the code
- Two-call pipeline validated and working
- All four prompt fixes completed — Call 1 and Call 2 system prompts updated
- UI colour theme — pending John's colour decisions

### Prompt fixes completed
- Call 1 Q1: no longer suggests specific situations — forces the user to surface one themselves
- Call 1: explicit situation recollection added — user prompted to name exact moments, exact calls, exact specifics rather than general event flow
- Call 2: action-naming instruction added — final question now prompts the user to name a concrete action, not just surface the belief

### Next session
- John to dictate colour theme — implement across `tool2_reflection/ui.py`

---

## Session 4 — June 2026

### What was done
- Call 2 prompt designed and implemented in `tool2_reflection/logic.py` as `generate_final_question`
- Full two-call pipeline now complete in `logic.py`
- Prompt engineering session — both call prompts derived from first principles, not AI generated theory
- Call 1 and Call 2 prompts written by John from his own evidence and experience before being formalised
- Cognitive dissonance identified as the formalised mechanism behind what John observed personally — the uncomfortable question that closes the escape route
- Muhasaba identified as the Islamic parallel — self-accounting, named explicitly in Al-Ghazali's Ihya
- Aporia identified as the Socratic parallel — the moment the contradiction is fully exposed and there is nowhere to go

### State of the code
- Two-call pipeline complete in `tool2_reflection/logic.py`
- `generate_context_questions(source_content, initial_reflection)` — Call 1, returns list of 3 questions
- `generate_final_question(source_content, initial_reflection, questions, responses)` — Call 2, returns one Socratic question targeting the unconscious belief implied by the user's responses
- UI wired to both calls — pending test

### Architecture decisions made
- Call 2 target is the unconscious belief implied by the user's own responses — not the behaviour, not the gap, not the blocker
- The model infers the belief from contradictions across the 4 sources — it does not generate one from nothing
- The question leads the user to name the belief themselves — the model does not state it to them
- All prompt rules derived from John's own evidence log and personal experience of what produced dispositional change

### Next session
- Test the full two-call pipeline end to end with real content
- Validate Call 1 question quality — are the three questions contextualised or generic
- Validate Call 2 question quality — does it surface an unconscious belief or loop back into the concept
- Log results as new evidence log entries
- UI polish pass and QThread implementation for both calls

---

## Session 3 — June 2026

### What was done
- SQLite schema implemented into the actual database — `initialise_db()` written in `db/database.py`, creates the Reflections table using `IF NOT EXISTS`
- `init_db()` updated to call `initialise_db()` — single entry point for database setup at app startup
- Conceptual session: schema implementation taught using cognitive framework — abstract shape, structure, analogy, test
- Line 4 of `database.py` broken down — the `DB_PATH` location resolver pattern explained through roles and narrative
- `os.path` relative path resolution identified as a reusable development pattern: `__file__` + `os.path.dirname` + `os.path.join`
- `init_db()` tested and confirmed running cleanly
- Tool 2 UI boilerplate generated in `tool2_reflection/ui.py` — full progressive reveal flow across 7 states, all widgets wired, DB save implemented in `_on_confirm()`
- `main.py` updated to load `Tool2Widget` in the Reflection tab
- App launched and confirmed opening cleanly

### State of the code
- Database initialisation complete — `init_db()` in `db/database.py` is the single startup call
- Tool 2 UI boilerplate complete in `tool2_reflection/ui.py` — progressive reveal across 7 states, all widgets wired, DB save working
- End-to-end test passed — real reflection saved to `learning_tool.db` and confirmed correct in the database
- Typo fixed: `initial_reflectioon` → `initial_reflection` in `tool2_reflection/logic.py` (parameter name and f-string usage)

### Decisions made
- `DB_PATH` sits at the project root (`Learning_Tool/learning_tool.db`), resolved relative to `database.py`'s own position using `__file__`
- Flow stress-tested via Socratic session before code was written — all 7 states, edge cases, and widget types mapped
- API call in `_on_send()` is synchronous for now — marked for `QThread` when UI polish begins

### Tool 2 UI elements confirmed (7)
1. Box to paste source content
2. Box to paste initial reflection
3. Box displaying generated question from API
4. Box to write new reflection against the question
5. Combined box showing both reflections merged — end of session state
6. Fields for metadata: date, media type, source author, topic, character referenced
7. Notes box alongside additional reflection — stored in `Abstract_topic` column

### Design decisions confirmed
- The combined reflection box (element 5) marks the end of the session. No further question generation after that point.
- Green border signals confirmed metadata fields
- API failure exits the tool — if input validation passes and call still fails, it is an API-side error
- First press of finish button locks the session and reveals confirm button; second press writes to DB

### Prompt engineering problem identified
- Tested the current prompt against real content. The question looped the user back into the philosophical concept they had already resolved in their reflection
- Root cause: the prompt follows the intellectual thread rather than the personal one, and has no instruction to push toward action or situation
- Fix is a prompt rewrite, not a parameter change

### Next session

Restructure `tool2_reflection/logic.py` — the single API call is being replaced with two sequential calls. The architecture has changed significantly:

**Call 1 — Context question generation**

Takes source content and initial reflection. Returns exactly 3 questions, each on a new line, nothing else. Parse with `response.strip().split('\n')` — `questions[0]`, `questions[1]`, `questions[2]` populate three separate input fields in the UI.

System prompt for Call 1:
```
You are a reflection coach. The user will give you a piece of source content and their initial understanding of it.

Your job is to generate exactly 3 questions. Each question must be fully written from the specific content and the user's own understanding — not from a generic template.

The 3 questions must target:
1. Where this concept is present or absent in a specific situation in the user's actual life right now
2. The gap between how they actually behave and how the concept demands they behave
3. What is concretely blocking them from closing that gap

Rules:
- Each question must be rooted in something specific from the content or the user's reflection — no generic questions
- Push toward a real situation, decision, or behaviour — never back into the concept itself
- No preamble, no numbering labels, no headers
- Return the 3 questions each on a new line with no other text, formatting, or separators
```

**Call 2 — Final Socratic question**

Takes source content, initial reflection, the 3 questions, and the user's written responses to them. Returns one final probing question aimed at the friction point surfaced across all the user's writing. Prompt to be written next session.

**Restructure the UI in `tool2_reflection/ui.py` to match the new flow:**

- Initial reflection box reframed as "what did you understand from this content"
- After Call 1 fires, three input fields appear populated with the 3 contextualised questions — user writes into each
- Call 2 fires from those three responses, returns the final question
- Existing additional reflection box receives the final question output

**Fix the API call lag** — thread both calls using `QThread` so the UI does not freeze during generation

### Architecture decisions made this session

- Two API calls replace the original single call
- Initial reflection reframed as comprehension of content — zahir layer
- Three structured questions bridge zahir to batin by targeting friction, gap, and blocker
- Final question generated from the full picture — pushes toward action
- Questions are dynamically generated from content each time — not fixed templates

---

## Session 2 — June 2026

### What was done
- API function validated — runs cleanly, response extracted correctly
- Model changed from claude-sonnet-4-6 to claude-haiku-4-5-20251001 for cost efficiency
- System prompt refined — output constrained to a single probing question, no preamble, no analysis, no bullet points. Message structure updated to clearly separate source material from personal reflection using f-string formatting
- Typo fixed in parameter name: `initial_reflectioon` → `initial_reflection`
- Question quality validated against real content and personal reflection — output confirmed good enough to build around

### State of the code
- API function in `tool2_reflection/logic.py` is complete and validated
- Schema in `db/schema_design` is designed but not yet implemented in the database
- No UI exists yet

### Decisions made
- Haiku confirmed as the model for question generation throughout the build — sufficient quality, significantly cheaper than Sonnet
- System prompt rules: one question only, no preamble, follow the user's thread, do not challenge their framing, make them want to write more
- The question generated works at the Socratic level — it doesn't tell the user anything, it pulls the reflection from zahir to batin by following the personal thread rather than the intellectual content

### Next session
1. Implement the SQLite schema into the actual database — create the db initialisation function in `db/database.py`
2. Begin thinking through Tool 2 UI — what the writing interface actually needs to look like

---

## Session 1 — June 2026

### What was done
- Project structure created — four tool modules, db, shared, main.py
- SQLite schema designed for Tool 2 reflection entries, stored in `db/schema_design`
- Anthropic API function written in `tool2_reflection/logic.py` — takes content context and user's initial reflection as inputs, returns a Claude-generated reflection question

### State of the code
- Schema is designed, not yet implemented in the database
- API function is written, not yet validated or tested
- No UI exists yet

### Decisions made
- Two inputs into the API function: source content context + user's personal reflection. Combined into a single message. Claude works from both — source material prevents hallucination, user context surfaces the personal knot.
- Schema fields: Reflection_id, Given_prompt, Reflection_Writing, Date, Source_Author, Media, Topic_of_discussion, Abstract_topic, Character_referenced

### Next session
1. Validate the API function — test it runs, returns a real response, and the question quality is good enough to build around
2. Refine the system prompt inside the function — structure the message so Claude clearly distinguishes between source content and user reflection
3. Begin thinking through Tool 2 UI and what the writing interface actually needs to look like
