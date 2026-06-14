---
name: paper-search
description: Literature and publication evidence search skill for Muon and optimization research. Use when Codex needs to find, deduplicate, and summarize recent papers for an optimizer, method family, research cluster, theorem, implementation choice, benchmark, or mathematical claim using public bibliographic sources.
---

# Paper Search

Inspired by `openags/paper-search-mcp` and adapted for Muon and optimizer research evidence.

## Procedure

1. Identify the exact method, paper, author, or keyword cluster before trusting paper matches.
2. Search across the best sources for the field: arXiv, Semantic Scholar, OpenAlex, Crossref, DBLP, conference proceedings, and official project pages.
3. Deduplicate by title, DOI, venue, year, and author list.
4. Keep papers only when they support a technical question, mathematical claim, implementation detail, benchmark comparison, or historical connection.
5. Summarize what each paper contributes to understanding Muon or related optimizers.

## Output Table

| Year | Paper | Venue | Source | Technical Evidence | Notes |
|---|---|---|---|---|---|

## Rules

- Do not create a generic literature dump.
- Do not cite inaccessible full text as if it was read.
- Use abstracts and metadata carefully when full text is unavailable.
- Mark author, title, version, or method-name uncertainty when names collide.
