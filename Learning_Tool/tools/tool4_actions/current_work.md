# Current Work — Trace of Thought

**Last touched:** 2026-09-02

**Where I left off:** The page-3 Submit button is wired — `_submit_workflow` reads the four
inputs and calls `graph.reflection_workflow`. `ActionNode` / `BeliefNode` / `ReflectionNode` now
define `__eq__`/`__hash__` (id + class based), and `edge_creation` registers both of its nodes
into `node_dict` itself, so `reflection_workflow` no longer needs a separate registration loop —
both open questions from the prior session are resolved (see below). The in-memory graph
(`node_dict` / `adj_dict`) builds correctly but is **not persisted** — it resets every time
`main.py` closes. Next decision is which persistence path to take (options laid out below,
nothing chosen yet). Nothing renders the real graph on screen yet — the graph page (stack index 1)
still shows the "No data yet" placeholder and `_graph_has_data()` is still hardcoded `False`.

**Not yet verified against a live app run** — changes pass `py_compile` and `import`, but the
Submit flow hasn't been driven through the running UI with a real reflection id.

## What changed this session

- **Page 3 (workflow-entry) gained the real inputs:**
  - `QLabel("Reflection ID")` added above `workflow_id_field` (was placeholder-text only).
  - `workflow_belief_box` (`QTextEdit`, multi-line) under *"What belief have you realised you hold from this?"*
  - `workflow_action_box` (`QTextEdit`, multi-line) under *"What action will you take to oppose the belief?"*
  - `workflow_submit_btn` ("Submit") → `_submit_workflow`.
  - `workflow_status_label` under the button for pass/fail feedback.
- **Persistence across the Back button:** the page is built once in `_build_ui`, so the text
  boxes already keep their content across navigation. The one leak was `_open_workflow_id_page`
  clearing + repopulating the character combo every visit (resetting to index 0) — it now saves
  `currentText()` before the clear and restores it after.
- **Character pickers on page 2 and page 3 kept independent** — deliberate decision ("won't fix
  what's not broken"). Page 3 does not inherit page 2's selection.
- **`_submit_workflow` implemented.** Contract lives as its header comment. Flow:
  1. `int(self.workflow_id_field.text())` — `ValueError` → "Reflection ID must be a whole number." and stop.
  2. `Hash.read_character(character_name)` wrapped in `try/except TypeError` (empty / NULL-character
     slot — CLAUDE.md rough edge); `None` or falsy → "No reflections stored for '<name>'." and stop.
  3. `graph.node_extraction(reflections, reflection_id) is None` → "No reflection with ID <id> for
     '<name>'." and stop.
  4. else `graph.reflection_workflow(reflection_id, reflections, belief, action)` (return ignored),
     status → "Sequence added to graph for reflection <id>."
  `belief` / `action` passed through as-is, blank allowed for now.
- **Old `self._workflow_inputs` pause-point stash removed** — the real call supersedes it.
- **New import in `ui.py`:** `from tools.tool4_actions import graph`. Confirmed no circular import —
  `graph.py` → edge / *_node / collections only, never reaches back to `ui.py`.
- **`graph.reflection_workflow` no longer returns the root `ReflectionNode`** (removed by hand this
  session). Success and not-found now both look like `None` from outside — that's why the not-found
  check moved *up front* into the UI (guard 3) instead of keying off the return.
- **`__eq__` / `__hash__` added to `ActionNode`, `BeliefNode`, `ReflectionNode`** (`action_node.py`,
  `belief_node.py`, `reflection_node.py`) — identical pattern in all three, deliberately duplicated
  rather than pulled into a shared base (the three classes don't share one today; that's a bigger
  structural change than this was). Equality/hash are keyed on `(type(self).__name__, self.id)` —
  the same tuple `node_dict` already uses. `__eq__` returns `NotImplemented` for a non-matching
  type rather than `False`, per convention. Verified: two independently-built `BeliefNode(5, ...)`
  instances now compare equal, hash equal, and a dict keyed on one resolves via the other.
  **Why:** without this, node objects only compared equal by memory identity — a node rebuilt from
  persisted data (same id, same class, new object) would never match the pre-restart node in
  `node_dict`/`adj_dict`. This was a live blocker for every persistence path being considered below.
- **Node registration folded into `edge_creation`.** `edge_creation(node1, node2, info=None)` now
  registers both endpoints into `node_dict` before building the `Edge`/appending to `adj_dict`.
  `reflection_workflow`'s separate `for node in (...): node_dict[...] = node` loop was deleted —
  registration now happens purely as a side effect of connecting nodes. **Why:** the old split kept
  `node_dict` in sync with `adj_dict` only by caller discipline (remembering to run the loop before
  calling `edge_creation`); a future caller that skipped the loop would produce an edge pointing at
  an unregistered node, failing silently until something tried to resolve it. Folding registration
  into the one function that creates connections makes that invariant impossible to violate instead
  of just documented. Verified: `reflection_workflow` still populates `node_dict` with all three
  entries and `adj_dict` with both edges, now via one path instead of two.
  **Known limitation, not fixed:** a node passed to `node_creation` but never passed to
  `edge_creation` (an isolated node) would never get registered. Not a real case in the current
  fixed reflection→belief→action chain; would matter if a future node type can exist without edges.

## Deviation from the confirmed `_submit_workflow` contract

Guard (3) as agreed keyed off `reflection_workflow`'s return value. With the return removed, that
signal is gone, so the not-found check is now done **before** the call via `graph.node_extraction`
— graph's own lookup, not a reimplementation in the UI. Cost: the reflections list is scanned
twice (once by the guard, once inside `reflection_workflow`). Flagged at implementation time, not
changed silently.

## Confirmed decisions this session (don't re-litigate)

- Belief + action are entered on the **same page** as the ID + character picker (page 3), not a
  separate step/page.
- Prompt wording is fixed: *"What belief have you realised you hold from this?"* and
  *"What action will you take to oppose the belief?"*
- Submit **collects all four and calls the workflow**, then we pause — no graph-page rendering,
  no navigation change on success yet.
- **Growing graph is wanted:** `node_dict` / `adj_dict` accumulate across workflow runs within one
  app session and are never reset in-process.
- `QTextEdit` (multi-line) for belief and action, not `QLineEdit`.

## Graph persistence — discussed, NOT decided

Key realisation: the only genuinely new data a workflow run produces is **the belief string, the
action string, and their attachment to a `reflection_id`**. `ReflectionNode` is a copy of a
`Reflections` row; the edge chain shape is fixed (reflection → belief → action). So most paths
collapse to something small.

- **Path 1 — SQLite, one row per sequence.** `Action_Sequences(reflection_id FK, belief_text,
  action_text, created_at)`. Rebuild nodes/edges at startup, one call per row. Smallest; matches
  existing storage layer; makes `PRAGMA foreign_keys = ON` finally mean something. Encodes the
  "always a 3-node chain" assumption.
- **Path 2 — SQLite, generic `Graph_Nodes` + `Graph_Edges`.** Node table + edge list; adjacency
  built in memory at load. Shape-agnostic, teaches adjacency-list vs edge-list. More machinery
  than the data currently justifies (reflection nodes carry a NULL payload).
- **Path 3 — belief/action as columns on `Reflections`** (or a sidecar keyed by `reflection_id`).
  No separate graph persistence at all — the graph becomes a rebuilt in-memory index over
  reflections that have belief+action filled in, exactly like `HashMap` over `Reflections`. Most
  consistent with existing architecture. Commits hard to one-belief-one-action-per-reflection.
- **Path 4 — JSON file.** Needs `to_dict` / `from_dict` per node class + tuple-key coercion
  (`adj_dict` is keyed by node objects, `node_dict` by tuples — neither is JSON-native). Human
  readable; hand-rolled serialization to maintain.
- **Path 5 — `pickle`.** Rejected as a durable format: brittle across class renames/moves, not
  human-readable.
- **Path 6 — `networkx` / graph DB.** Overkill for a fixed 3-node chain; noted for awareness only.

**Leaning:** path 3 or path 1 for consistency. Whichever: **do not persist the full
`ReflectionNode`** — store only `reflection_id` and rebuild it from the `Reflections` row at load
(one-shape-per-concept).

## What's still true — keep this

- 4-page `QStackedWidget` (`Tool4Widget`, `tools/tool4_actions/ui.py`), wired into `main.py`'s
  Notes tab: Menu / Graph placeholder / Add-sequence (Tool 2 View-Reflections format) / Workflow-entry.
- `Edge` v1, `node_creation` factory, `node_extraction`, `edge_creation`, and the
  `node_dict` (`{(type_name, id): node}`) / `adj_dict` (`node object → list[Edge]` outgoing)
  shapes all still stand from the prior session.
- `node_creation` match strings are `"Action"` / `"Reflection"` / `"Belief"`; the three call
  sites in `reflection_workflow` match.
- `BeliefNode` / `ActionNode` ids are hand-passed the `reflection_id`, nothing backing them;
  `ReflectionNode.id` comes from `data[0]` of the real DB row.
- Hashmap structure: `array[hash(character_name)]` → `{character_name: [row, ...]}`, each row a
  full 9-field DB tuple. Reflection ids are global autoincrement — unique everywhere, never equal
  to list position.

## Open questions (still open)

- What does a successful Submit do for the UI — navigate to / refresh the graph page? Deferred.
- Persistence path not chosen (above).

## Resolved this session (don't re-derive)

- ~~Should `edge_creation` be the single entry point that registers its two nodes into `node_dict`
  *and* builds+appends the `Edge`?~~ **Yes, done.** See "Node registration folded into
  `edge_creation`" above.
- ~~`adj_dict` keyed by node object relies on identity hashing~~ **Fixed.** `__eq__`/`__hash__`
  added to all three node classes, keyed on `(type(self).__name__, self.id)` — matching values now
  compare/hash equal regardless of object identity. This was specifically unblocking persistence:
  any DB-backed path rebuilds nodes at startup, and those rebuilt nodes now correctly match their
  pre-restart counterparts.

## Immediate next step

Pick a persistence path — or explicitly defer it and build the graph-page rendering against the
in-memory `node_dict` / `adj_dict` first (and replace the hardcoded `_graph_has_data()` with a
real check). The identity-hashing blocker that would have hit any DB-backed path is now resolved
(`__eq__`/`__hash__` in place), so persistence is no longer blocked on that — just on picking a path.

## Habits this session (end-of-session check)

- **Contract-first (current focus):** stated `_submit_workflow`'s contract, got sign-off, then
  wrote the body; contract kept as the method header. The one forced deviation (guard 3, after the
  return value was removed) was flagged and explained, not silently applied. Same pattern repeated
  for `__eq__`/`__hash__` — contract stated and confirmed before writing.
- **One shape per concept:** `reflection_id` as widget text vs the `int` passed onward — input
  parsing, not a competing stored representation, so fine. Flagged that persistence must not store
  the full `ReflectionNode` (would duplicate a `Reflections` row).
- **Building ahead of consumers:** removed the now-superseded `self._workflow_inputs` stash rather
  than leaving dead holding state in the file.
- **Name the pattern (implicit contracts):** the `node_dict`/`adj_dict` sync problem was framed and
  talked through explicitly — "a rule enforced by caller discipline instead of by the function
  itself" — via Socratic questions before folding the fix into `edge_creation`, rather than just
  silently refactoring it.

**Full design record:** `Project_files/06_actions_tool.md` — still stale, update once a persistence
path is chosen and the graph page renders real data.
