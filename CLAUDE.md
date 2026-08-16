# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose and constraints

This is a personal-use, self-learning project (not a commercial product). Per `Project_files/03_product_architecture.md`, there is an explicit **hardcode vs vibe-code split** the user wants respected:

- **Hardcode manually (do not casually rewrite or "simplify" for the user):** question-generation prompt engineering (`tools/tool2_reflection/logic.py`), data structures (`shared/DSA/hashmap.py`, `shared/DSA/tree.py`, and the tree-building/traversal logic in `tools/tool1_contents/logic.py`), core schema design (`docs/schema_design.sql`).
- **Fine to generate/edit freely:** PyQt6 UI boilerplate, file I/O, API call wrappers, config/setup.

The hand-rolled `HashMap` in `shared/DSA/hashmap.py` is intentional — it exists so the user practises implementing hashing/collision handling themselves, not because Python's `dict` is insufficient. Don't replace it with a plain `dict` unless asked.

`session_log.md` (in `Learning_Tool/`) is a running dev diary, most-recent-session-first. Check it for the latest intent before assuming the codebase matches the last commit — the log is sometimes ahead or behind the actual code state.

## Commands

Run from the `Learning_Tool/` directory (this is the actual Python package root; the repo root one level up just holds planning docs).

```bash
cd Learning_Tool

# Run the app
python main.py

# Manual smoke test of the Tool 2 Claude pipeline (no test framework/pytest in use)
python -m scripts.test_api
```

There is no `requirements.txt`/`pyproject.toml`, no linter, and no automated test suite configured — dependencies (`PyQt6`, `anthropic`, `python-dotenv`) are only discoverable via `import` statements. A `.env` file in `Learning_Tool/git/` holds `ANTHROPIC_API_KEY`, loaded via `python-dotenv`.

## Architecture

The app is a **hub of four planned tools**, only one of which is built:

- **Tool 2 — Prompted Reflection Writer** (`tools/tool2_reflection/`) — fully implemented, the only tab with real functionality.
- **Tool 1 (Contents)** (`tools/tool1_contents/`) — `logic.py` has the hand-built tree (`shared/DSA/tree.py`'s `TreeNode`, built from a static `domain_theme_map` via `add_nodes_dictionary`/`Root_node`), a complete `dfs_traversal`, and `node_search(n_list, index_node)` (linear search by `node.theme` string, returns `node.text` on a match or implicitly `None` on no match — hand-built by the user, Claude-reviewed only, per the hardcode/vibe-code split). `ui.py` (`Tool1Widget`) is now built and wired into `main.py`'s Contents tab.
- **Tool 3 (Narratives)**, **Tool 4 (Notes)** — `logic.py`/`ui.py` in their respective folders are one-line stubs; `main.py` shows a placeholder `QLabel` for each. Build order is intentionally Tool 2 → 1 → 3 → 4 (each later tool consumes the previous one's output).
  - Tool 1 was previously called "Consumption" — renamed to "Contents" (folder `tools/tool1_contents/`, `main.py` placeholder/tab label).

### Data flow through Tool 2

`tools/tool2_reflection/ui.py` (`Tool2Widget`) is a `QStackedWidget` with 4 pages: Menu → Add Reflection → Delete Reflection → View Reflections. The Add flow:

1. User enters source content + metadata + an initial reflection.
2. `logic.generate_context_questions()` — Claude call #1 — returns 3 contextual probing questions (run off the UI thread via a `_Worker`/`QThread`).
3. User answers all 3.
4. `logic.generate_final_question()` — Claude call #2 — synthesizes one Socratic question meant to surface an unconscious belief.
5. User's response to that becomes the stored reflection; on save the UI writes a `Reflections` row directly via `db.database` **and** calls `Hash.hash_insertion` to keep the in-memory cache in sync.

Both Claude calls use model `claude-haiku-4-5-20251001` and live only in `tools/tool2_reflection/logic.py`, which has no dependency on `db`/`shared` — it's a pure API wrapper.

### Tool 1 UI — graph view and search

`tools/tool1_contents/ui.py`'s `Tool1Widget` renders the tree as a `QGraphicsScene`/`QGraphicsView` diagram rather than an indented list: every node is its own box (recursive layout — children placed left-to-right, each parent centered above its own children, depth sets the row), with a line from each parent's bottom-center to every child's top-center. A `QStackedWidget` swaps between this graph page and a detail overlay page (header + name box + empty text box + X-to-close). Two entry points feed the same overlay, both routed through `node_search`: clicking a box (`QGraphicsScene.selectionChanged`, node reference stored directly on the box) and a typed search bar above the graph. `node_search`'s return value is relied on directly to distinguish states — `None` means no match, `""` means found but no content yet.

### Storage layer — two paths, kept manually in sync

- `db/database.py` is the source of truth: a single SQLite table `Reflections` (schema mirrored in `docs/schema_design.sql` — keep these two in sync when changing columns). Direct CRUD helpers: `get_connection()`, `get_character_name()`, `delete_reflection()`, `get_all_character()`.
- `shared/DSA/hashmap.py` (`HashMap`) is an in-memory read cache over that table, keyed by `Character_referenced`, populated at startup via `hashmap_initialise()` (called once in `main.py`) and kept warm by explicit `hash_insertion`/`delete_reflection` calls from the UI — it is **not** auto-refreshed from the DB on every read.
- `shared/hash_instance.py` holds the single module-level `Hash = HashMap()` instance. It exists purely to break a circular import (`shared/DSA/hashmap.py` imports from `db.database`; both `main.py` and `tools/tool2_reflection/ui.py` need the same instance) — import `Hash` from here, never instantiate `HashMap()` directly elsewhere.

Because two access paths exist, when touching reflection CRUD logic check both `db/database.py` and `shared/DSA/hashmap.py` for the operation you're changing — they are not automatically consistent with each other (e.g. `HashMap.read_character`/`delete_reflection` only catch `KeyError`, not the `TypeError` that results from a `None`/empty slot or a `None` `character_name`, e.g. from a reflection saved with no character referenced).

### Known rough edges worth knowing before editing nearby code

- `Character_referenced` is nullable in the schema and the UI allows saving without one, but `get_all_character()` / dropdown population don't filter out the resulting `NULL` group — selecting it can crash `hash_formula` (`len(None)`).
- `HashMap.reflection_storage` is dead code and inconsistent with the `{character_name: rows}` structure the rest of the class assumes — don't call it, and don't use it as a reference for the expected slot shape.
- `PRAGMA foreign_keys = ON` in `init_db()` is currently a no-op (single table, no FKs) — relevant once Tool 3/4 add related tables.
- `TreeNode.text` (`shared/DSA/tree.py`) defaults to `""` for every node and nothing writes to it yet — the JSON-backed Seerah content described in `tools/tool1_contents/logic.py`'s docstring isn't built, so both the click and search detail views currently always show empty content regardless of theme.
