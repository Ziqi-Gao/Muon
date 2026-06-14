# Optimizer Knowledge Graph Data

This folder stores the lightweight graph backing the optimizer-history and Muon survey work.

## Files

- `nodes.csv`: graph nodes for methods, papers, concepts, components, systems, and results.
- `edges.csv`: typed relations between nodes.
- `sources.csv`: evidence sources used by graph nodes and edges.

## Node Columns

- `id`: stable local identifier.
- `label`: human-readable label.
- `type`: `method`, `paper`, `concept`, `algorithmic_component`, `system_component`, or `result`.
- `year`: year if known.
- `summary`: one-line description.
- `source_ids`: semicolon-separated source IDs.
- `status`: `seed`, `active`, `needs_review`, or `deprecated`.

## Edge Columns

- `source`: source node ID.
- `target`: target node ID.
- `type`: relation label, such as `introduced_by`, `extends`, `uses`, `analyzes`, or `compares_to`.
- `summary`: short evidence note.
- `source_ids`: semicolon-separated source IDs.
- `confidence`: `high`, `medium`, or `low`.

## Source Columns

- `id`: stable source slug.
- `title`
- `authors`
- `year`
- `venue_or_status`
- `url`
- `doi`
- `arxiv_id`
- `openalex_id`
- `notes`

Render outputs:

```powershell
& 'C:\Users\PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\render_optimizer_graph.py
```
