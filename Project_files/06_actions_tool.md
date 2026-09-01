# Actions Tool — Planning Note
*Part of the Knowledge Transfer Project planning series — August 2026*
*Status: node classes built (Reflection, Belief, Action) with a working adjacency-list proof-of-concept; Edge class is the immediate next step, not yet coded.*

---

## The idea

A new, separate tool (not folded into Tool 3) that stores the **action** generated from a reflection's final Socratic question — the concrete thing you go and do to act against the extreme of the belief you've been avoiding.

Not a flat action log. The point is that actions link back to the reflections and beliefs that produced them, and the tool should let you look at that linkage over time — what you're trying to work on, how it's evolved, whether the same belief keeps resurfacing.

---

## Current build state (as of 2026-08-25)

- `tool4_actions/reflection_node.py` — built, working. Reads a single reflection row from the DB (`get_exact_reflection`) into a node object: `id` plus 8 fields (prompt, writing, date, source, media, topic, abstract topic, character).
- `tool4_actions/belief_node.py` / `action_node.py` — minimal versions built: `id`, a single content string (`belief`/`action`), `edit_*`/`return_*` accessor methods, `__repr__` for debugging. **No placeholder/merge logic yet** — deliberately deferred (see to-do list).
- `tool4_actions/graph.py` — a scratch proof-of-concept, not the real module yet: three hardcoded node instances (one of each type), a plain list-of-pairs adjacency list, converted via `adj_list_create` into `dict[node_object] -> list[node_object]`. Confirmed working end-to-end (`python -m tools.tool4_actions.graph`).
- **Location note**: this tool was originally scoped to live in `shared/DSA/graph.py`, matching where `hashmap.py`/`tree.py` live (see "Why this is worth the extra difficulty" below). The current file is in `tools/tool4_actions/` instead. Not yet decided whether to move it — see to-do list.
- `Edge` class — not built. This is the next step (see "Next step").

---

## Why a graph, not a table

A flat table (one row per action, maybe a foreign key to a reflection) would be enough to store the data, but not enough to answer the question this tool actually exists for: *which belief have I been neglecting, and which ones keep coming back?*

That requires modeling relationships, not just rows:
- A **belief** can be surfaced by more than one reflection (it resurfaces)
- An **action** addresses a belief, and a later action can be a retry of an earlier one
- The interesting queries are relational — "show me everything connected to this belief" — which is graph traversal (BFS/DFS), not a single lookup

Rough node/edge sketch (not final):
- **Nodes:** Reflection, Belief, Action
- **Edges:** Reflection → surfaces → Belief; Belief → addressed by → Action; Action → retry of → earlier Action
- Unanswered/unresolved thoughts are **not** modeled as edges or as their own node type — they live as a plain attribute on a node (comparable to `TreeNode.text` in Tool 1), so traversal and degree-counting code never has to special-case an edge with a missing endpoint.

---

## Node and edge design (resolved)

- **Reflection → Belief cardinality:** every reflection has exactly one outgoing edge, always. If the final Socratic question doesn't cleanly name a belief, the reflection points to its own distinct placeholder Belief node (keyed by reflection ID) instead of having zero edges.
- **Resurfacing mechanism:** resurfacing is **human-recognized, not automatic**. When you notice a placeholder is the same belief as an existing node, you manually merge it — the placeholder's edge is deleted and redirected to the existing Belief node, and the placeholder node is deleted. There is no automated duplicate/similarity detection planned.
- **Node mutability:** node content is mutable in place — a placeholder can be edited with real belief content while keeping the same node identity/ID.
- **Edge mutability:** edges themselves are not edited in place. On a merge, the old edge is deleted and a new one created to the real node — two distinct mechanisms (edit node vs. delete+recreate edge) for two distinct outcomes, not one blanket mutability rule.
- **Frequency metric:** in-degree on a Belief node (count of Reflection edges pointing at it) — specifically in-degree, not out-degree or combined, since it's meant to measure "how many times has this belief been raised," not "how many actions have addressed it." Entirely dependent on how promptly placeholders get merged — an unmerged placeholder undercounts silently, and that's an accepted tradeoff, not a gap to fix.
- **Node identity:** every node needs an explicit `id` field distinct from its content — implemented on all three node classes. This is what makes the merge mechanism above actually buildable: a placeholder's *content* changes on merge/edit, so identity can't be derived from content.
- **Edge shape:** an edge is `Edge(from_id, to_id, edge_type)` — references node `id`s, not node objects directly. The adjacency list is keyed by `id` (`dict[node_id] -> list[Edge]`), with a separate `nodes` dict (`{id: node_object}`) for looking up the actual object. This indirection is what lets a merge redirect a connection by editing one `Edge.to_id` field rather than hunting down every reference to the old object.

---

## Why this is worth the extra difficulty

Per the hardcode/vibe-code split (`03_product_architecture.md`), this is squarely hardcode territory — same category as `shared/DSA/hashmap.py` and `shared/DSA/tree.py`. Two structures not yet fully built anywhere in this project:

1. **Graph** (adjacency list, hand-rolled) — traversal to answer "everything connected to this belief". Node classes and a proof-of-concept adjacency list exist; the `Edge` class and the id-keyed refactor are still to come.
2. **Priority queue / min-heap** — to rank "which belief has been neglected longest" or "which belief keeps recurring most" into something the UI can actually surface, rather than just letting you scroll a list. Not started.

Both are standard placement-interview DSA territory (`01_who_and_context.md` — DSA baseline currently covers stacks/queues/linked lists/arrays/hashmap only) and neither has a home anywhere else in this project yet.

---

## Relationship to Tool 3

Deliberately kept **separate** from Tool 3 (Narrative & Character Store), per the decision made when this was discussed — not an extension of Tool 3's own long-term "Phase 3" graph direction (`03_product_architecture.md`: "graph connecting knowledge nodes — characters → principles → personal situations"). That graph is about characters/narratives; this one is about beliefs/actions. They may eventually reference each other (an action could plausibly link to a character who modeled the behaviour), but that's a future integration question, not a starting assumption.

---

## Open questions to resolve before scoping a build

Resolved — see "Node and edge design" above:
- ~~Does a resurfacing belief create a new Belief node, or add an edge back to an existing one?~~ Neither by default — a new placeholder node is created per unresolved reflection; an edge back to an existing node only happens via manual merge.
- ~~Does every reflection produce a Belief node, or only ones where the final Socratic question actually names one?~~ Every reflection produces an edge to *some* Belief node — a real one or a placeholder.
- ~~What does "neglected longest" actually rank on?~~ Partially resolved — frequency is in-degree on Belief nodes. The "days since last action" half of this question is still open (see below).
- ~~How does a node get referenced without holding a direct object reference?~~ Resolved — explicit `id` field per node, `Edge` references `id`s, not objects.

Still open:
- What triggers an action being marked "done" — a fixed checkbox, a follow-up reflection, something else?
- "Neglected longest" by *time* (days since last action) — not yet decided how this combines with, or trades off against, the resolved frequency (in-degree) metric.
- Where does this live in `main.py` — a fifth tab, or does the tab count/naming need rethinking?
- Does this need its own SQLite tables, or can it reuse/extend the existing `Reflections` table structure?

---

## Next step (when this is picked back up)

Node-first approach worked as planned — Reflection, Belief, and Action node classes all exist now (see "Current build state" above), each with an `id`, a content string, and edit/return accessor methods. Belief and Action nodes are minimal only — no placeholder/merge handling yet, deliberately deferred (see to-do list).

**Immediate next step: build the `Edge` class**, per the shape resolved above (`from_id`, `to_id`, `edge_type`), and refactor `graph.py`'s adjacency list from its current proof-of-concept form (`dict[node_object] -> list[node_object]`) to the real form (`dict[node_id] -> list[Edge]` plus a `nodes` lookup dict).

Search-to-traversal adaptation (needed for the human-recognition merge step to actually browse existing beliefs) and the visual graph view both still come later, deliberately after the node/edge shapes exist — not before.

---

## Project to-do list

- [x] Find out how graphs work in python so i can sketch the basic node to node relationship for my one reflection and action — done via the theoretical grounding and requirements-tension session (see "Node and edge design" above).
- [x] Build Reflection, Belief, and Action node classes (minimal — `id` + content + edit/return methods) and confirm a basic adjacency list works end to end.
- [ ] Build the `Edge` class (`from_id`, `to_id`, `edge_type`) and refactor `graph.py`'s adjacency list to be id-keyed and store `Edge` objects (replacing the current node-object-keyed proof-of-concept).
- [ ] Decide: does `graph.py` move to `shared/DSA/graph.py` per the original scope (matching `hashmap.py`/`tree.py`), or stay in `tools/tool4_actions/`?
- [ ] Edit tool 2 so i can articulate the beleif ive realsied i hold and that i can store that as a node for the grasph
- [ ] Build the placeholder Belief node and its merge-into-existing-node mechanism — deferred until node_search is adapted into graph traversal (with visited-node tracking, since this graph has cycles that Tool 1's tree-based search never had to handle) and a visual graph view exists to browse existing beliefs against
