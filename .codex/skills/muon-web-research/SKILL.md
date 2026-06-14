---
name: muon-web-research
description: Search, track, and capture current web sources for the Muon optimizer, optimizer-history literature, and related ML optimization research. Use when Codex needs up-to-date web discovery, source triage, arXiv/OpenAlex/Semantic Scholar lookups, conference/news checks, or evidence-backed paper registries for Muon and optimizers.
---

# Muon Web Research

Use this skill for source discovery and evidence capture before writing survey content or updating the graph.

## Workflow

1. Start with dated search queries and record the exact date of the search.
2. Prefer primary sources in this order: paper pages, arXiv/OpenReview/conference pages, official code repositories, author pages, then high-quality secondary commentary.
3. Query multiple indexes when possible: arXiv, Semantic Scholar, OpenAlex via `pyalex`, Crossref, and general web search.
4. Deduplicate by DOI, arXiv ID, OpenAlex ID, title normalization, and author/year.
5. For each candidate source, classify it as:
   - `core`: directly about Muon or an optimizer lineage milestone.
   - `adjacent`: relevant preconditioning, momentum, matrix orthogonalization, scaling, or optimizer state work.
   - `background`: useful for context only.
6. Capture citation metadata, abstract, source URL, PDF URL if available, code URL if available, and why it matters.
7. Mark claims that depend on recent or unstable information with the date checked.

## Output Shape

For each source, produce compact records with:

- `id`: stable local slug, such as `jordan2024muon`.
- `title`
- `authors`
- `year`
- `venue_or_status`
- `doi`
- `arxiv_id`
- `openalex_id`
- `urls`
- `topic_tags`
- `relevance`
- `evidence_notes`

## Boundaries

- Do not treat generated summaries as evidence.
- Do not claim "all papers" unless search queries, databases, and cutoff date are explicitly stated.
- Keep raw source links with the claim they support.
