# Current Work — Trace of Thought

**Last touched:** 2026-09-01

**Where I left off:** Session split in two halves. First half built out the Tool 4 UI end-to-end for menu → pick-a-reflection → begin-workflow entry. Second half reviewed `reflection_workflow` in `graph.py` and found it still broken — not fixed, left as questions to trace through next. The UI's "Begin Reflection Workflow Sequence" button doesn't call into `graph.py` yet; it just collects character + reflection_id on screen.

**What's actually right in this version (keep this):**
- `Tool4Widget` (`tools/tool4_actions/ui.py`) is built and wired into `main.py`'s Notes tab, replacing the old placeholder label. Four-page `QStackedWidget`:
  1. Menu — two nav boxes: "View Graph" / "No data yet" (label reflects `_graph_has_data()`, hardcoded `False` until `graph.py` has real persistence) and "Add Reflection Sequence to Graph".
  2. Graph page — placeholder "No data yet" centred, reachable but not yet backed by real graph data.
  3. Add-sequence page — reuses Tool 2's View Reflections format on purpose: character combo → reflection list → read-only details box, same row unpack and details string as Tool 2. Data path is `Hash.read_character(name)`, same as Tool 2. Confirmed choice: two-step character-then-reflection picker (not a flat list), and the NULL-character group shows in the dropdown same as Tool 2 (not filtered out).
  4. Workflow-entry page — reached via "Begin Reflection Workflow Sequence" button on the add-sequence page. Has "Which character do you want" + a character dropdown (`workflow_character_combo`, populated fresh each open via `_open_workflow_id_page`), and a `QLineEdit` (`workflow_id_field`) placeholder "Enter the reflection_id you choose". Nothing reads these values yet — no submit/confirm action wired.
- All four pages tested against the real DB (`init_db()` + `Hash.hashmap_initialise()`), navigation confirmed working both directions.
- `Edge` v1 (`edge.py`) still stands, still passed review from prior sessions.
- `node_creation` factory still stands, still routes all three node types through one function (case-sensitive lowercase match — see questions below).

**Questions worth tracing through `reflection_workflow`:**
- What does a `reflection_node` actually need in order to build itself — check its `__init__`. Does what `reflection_workflow` currently gathers and passes in match that, or is it fetching something by hand that's no longer needed?
- `node_creation` does exact string comparisons to decide which node type to build. Do the three call sites in this function match what it's actually comparing against?
- Look at the block that files the three nodes into `node_dict` — three lines building a key and appending. One of them does something to the name `node_dict` itself that changes how every other line in the function reads it. Find that line first, then check whether the other two are self-consistent with it, and whether the key shape matches what `edge_creation` builds elsewhere in the file.
- `edge_creation` is defined to take three arguments. Count what's passed at the two call sites here.

**Once it runs cleanly, two more things worth deciding:** what should happen if the typed `reflection_id` doesn't exist for the chosen character, and where the two built edges should actually end up (right now they're computed and never returned or stored).

**Open architecture questions (still not answered — carried over, plus one new):**
- (Carried over) Should `edge_creation` be the single entry point that both registers its two nodes into `node_dict` *and* builds+appends the `Edge` into `adj_dict`? Or keep node registration and edge creation as two deliberately separate calls?
- (Carried over) `node_dict` shape — key → single object, or key → list? `reflection_workflow` currently `.append`s nodes into it (list shape), which matches neither your stated design ("what is this," implying single object) nor is done consistently anywhere else.
- (New) Now that the UI collects `character_name` + `reflection_id` on the workflow-entry page, does `reflection_workflow` need a `belief`/`action` text input on that same page too, or is that a separate step/page? Right now the UI only gathers the first two of `reflection_workflow`'s four params.

**Conclusions reached (don't re-derive these — still valid):**
- `belief_node`/`action_node` ids are hand-typed with nothing backing them — unlike `reflection_node`, whose id is really read from the DB.
- Combining nodes into one `{id: object}` dict collides on bare id; fix is keying by `(type(obj).__name__, obj.id)`.
- Two separate structures needed: `node_dict` (key → object) and `adj_dict` (key → `list[Edge]`). Don't merge them.
- `Edge` itself never computes the combined key — the caller builds `(type, id)` at the point where the real node object is in hand.
- Naming note, still not resolved: `edge.py` uses `self.from_node_id`/`self.to_node_id`/`self.type`, design language elsewhere uses `from_id`/`to_id`/`edge_type`.
- The hashmap's own structure (clarified this session, not a code change): `array[hash(character_name)]` → `{character_name: [row, row, ...]}` → each row is a full 9-field DB tuple. Reflection IDs are global/autoincrement across the whole table, not per-character — unique everywhere but not contiguous within one character's list, and never equal to list position.
- `06_actions_tool.md` is still stale against this file and the actual code — update once `graph.py` runs cleanly.

**Immediate next step:** Work through the questions above on `reflection_workflow`, starting with the `reflection_node` data-source one since it reframes what the function even needs to do. Decide the two carried-over architecture questions since they affect how the fix should be written, then wire the UI's "Begin Reflection Workflow Sequence" flow to actually call it with the character + reflection_id already being collected (plus wherever belief/action input ends up living).

**Full design record:** `Project_files/06_actions_tool.md` (stale — see note above, don't treat its "Current build state" section as accurate right now)
