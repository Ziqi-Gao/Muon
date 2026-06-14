---
name: muon-knowledge-graph
description: Build, maintain, validate, and render the optimizer knowledge graph for SGD-to-Muon history and Muon survey research. Use when Codex needs graph schemas, nodes, edges, evidence links, optimizer lineage, paper-method relationships, timeline views, Mermaid diagrams, PyVis HTML exports, NetworkX analysis, or RDF/JSON graph exports.
---

# Muon Knowledge Graph

Use this skill for evidence-backed graph updates and visualization.

## Local Files

- Graph data lives in `data/optimizer-graph/`.
- The schema is documented in `data/optimizer-graph/README.md`.
- Render graph outputs with `scripts/render_optimizer_graph.py`.

## Graph Principles

1. Every non-obvious node and edge needs an evidence source.
2. Prefer small, typed records over prose blobs.
3. Keep method nodes separate from paper nodes.
4. Use edge labels that answer a specific relation, such as `introduced_by`, `extends`, `uses`, `analyzes`, `quantizes`, or `compares_to`.
5. Distinguish optimizer lineage from citation links. A paper can cite another paper without the method extending it.

## Update Workflow

1. Read the source or paper note.
2. Add or update source records first.
3. Add paper and method nodes.
4. Add typed edges with `source_ids` and a short evidence note.
5. Validate with the render script.
6. Inspect the generated Mermaid or HTML view for obvious disconnected or mislabeled nodes.

## Minimal Node Types

- `method`
- `paper`
- `concept`
- `algorithmic_component`
- `system_component`
- `result`

## Minimal Edge Types

- `introduced_by`
- `extends`
- `uses`
- `analyzes`
- `improves`
- `quantizes`
- `compares_to`
- `motivates`
- `has_component`
- `has_result`

## Confidence

Use `high`, `medium`, or `low`.

- `high`: directly supported by primary source text.
- `medium`: supported by paper context but requires mild interpretation.
- `low`: hypothesis, weak secondary source, or awaiting paper reading.
