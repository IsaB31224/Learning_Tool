# Actions Tool — Planning Note
*Part of the Knowledge Transfer Project planning series — August 2026*
*Status: in early build — Reflection node shape started, Belief/Action node and edge design resolved on paper, not yet coded.*

---

## The idea

A new, separate tool (not folded into Tool 3) that stores the **action** generated from a reflection's final Socratic question — the concrete thing you go and do to act against the extreme of the belief you've been avoiding.

Not a flat action log. The point is that actions link back to the reflections and beliefs that produced them, and the tool should let you look at that linkage over time — what you're trying to work on, how it's evolved, whether the same belief keeps resurfacing.

Build has started: `tool4_actions/reflection_node.py` reads a single reflection into a node shape. Belief/Action node and edge design is now resolved on paper (see "Node and edge design" below) but not yet coded.

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

## Node and edge design (resolved this session)

- **Reflection → Belief cardinality:** every reflection has exactly one outgoing edge, always. If the final Socratic question doesn't cleanly name a belief, the reflection points to its own distinct placeholder Belief node (keyed by reflection ID) instead of having zero edges.
- **Resurfacing mechanism:** resurfacing is **human-recognized, not automatic**. When you notice a placeholder is the same belief as an existing node, you manually merge it — the placeholder's edge is deleted and redirected to the existing Belief node, and the placeholder node is deleted. There is no automated duplicate/similarity detection planned.
- **Node mutability:** node content is mutable in place — a placeholder can be edited with real belief content while keeping the same node identity/ID.
- **Edge mutability:** edges themselves are not edited in place. On a merge, the old edge is deleted and a new one created to the real node — two distinct mechanisms (edit node vs. delete+recreate edge) for two distinct outcomes, not one blanket mutability rule.
- **Frequency metric:** in-degree on a Belief node (count of Reflection edges pointing at it) — specifically in-degree, not out-degree or combined, since it's meant to measure "how many times has this belief been raised," not "how many actions have addressed it." Entirely dependent on how promptly placeholders get merged — an unmerged placeholder undercounts silently, and that's an accepted tradeoff, not a gap to fix.

---

## Why this is worth the extra difficulty

Per the hardcode/vibe-code split (`03_product_architecture.md`), this is squarely hardcode territory — same category as `shared/DSA/hashmap.py` and `shared/DSA/tree.py`. Two structures not yet built anywhere in this project:

1. **Graph** (adjacency list, hand-rolled in a new `shared/DSA/graph.py`) — traversal to answer "everything connected to this belief"
2. **Priority queue / min-heap** — to rank "which belief has been neglected longest" or "which belief keeps recurring most" into something the UI can actually surface, rather than just letting you scroll a list

Both are standard placement-interview DSA territory (`01_who_and_context.md` — DSA baseline currently covers stacks/queues/linked lists/arrays/hashmap only) and neither has a home anywhere else in this project yet.

---

## Relationship to Tool 3

Deliberately kept **separate** from Tool 3 (Narrative & Character Store), per the decision made when this was discussed — not an extension of Tool 3's own long-term "Phase 3" graph direction (`03_product_architecture.md`: "graph connecting knowledge nodes — characters → principles → personal situations"). That graph is about characters/narratives; this one is about beliefs/actions. They may eventually reference each other (an action could plausibly link to a character who modeled the behaviour), but that's a future integration question, not a starting assumption.

---

## Open questions to resolve before scoping a build

Resolved this session — see "Node and edge design" above:
- ~~Does a resurfacing belief create a new Belief node, or add an edge back to an existing one?~~ Neither by default — a new placeholder node is created per unresolved reflection; an edge back to an existing node only happens via manual merge.
- ~~Does every reflection produce a Belief node, or only ones where the final Socratic question actually names one?~~ Every reflection produces an edge to *some* Belief node — a real one or a placeholder.
- ~~What does "neglected longest" actually rank on?~~ Partially resolved — frequency is in-degree on Belief nodes. The "days since last action" half of this question is still open (see below).

Still open:
- What triggers an action being marked "done" — a fixed checkbox, a follow-up reflection, something else?
- "Neglected longest" by *time* (days since last action) — not yet decided how this combines with, or trades off against, the resolved frequency (in-degree) metric.
- Where does this live in `main.py` — a fifth tab, or does the tab count/naming need rethinking?
- Does this need its own SQLite tables, or can it reuse/extend the existing `Reflections` table structure?

---

## Next step (when this is picked back up)

Don't start with the graph. Start the same way Tool 2 started: sketch the minimum schema/node shape needed for one action to exist and link to one reflection, get that working end to end, then layer in traversal and ranking once there's real data to traverse.

Underway: `reflection_node.py` is the first piece of this. Next up per the resolved design above — Belief node (with placeholder/merge handling), then Action node, then the Edge class itself.

Search-to-traversal adaptation (needed for the human-recognition merge step to actually browse existing beliefs) and the visual graph view both come later, deliberately after the node/edge shapes exist — not before.


#Project to do list

- [x] Find out how graphs work in python so i can sketch the basic node to node relationship for my one reflection and action — done via the theoretical grounding and requirements-tension session (see "Node and edge design" above).
- [ ] Edit tool 2 so i can articulate the beleif ive realsied i hold and that i can store that as a node for the grasph
- [ ] Build the placeholder Belief node and its merge-into-existing-node mechanism — deferred until node_search is adapted into graph traversal (with visited-node tracking, since this graph has cycles that Tool 1's tree-based search never had to handle) and a visual graph view exists to browse existing beliefs against
