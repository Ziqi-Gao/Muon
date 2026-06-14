---
name: semantic-scholar
description: Semantic Scholar based literature workflow for Muon and optimization research. Use when Codex needs paper disambiguation, author disambiguation, citation context, influential papers, recent paper lists, related-work trails, or citation graphs for optimizer and ML systems analysis.
---

# Semantic Scholar

Adapted from `Agents365-ai/semanticscholar-skill` as a workflow note. Use live API access only when it is available in the environment.

## Procedure

1. Search for the paper, method, author, or keyword cluster and confirm identity with title, authors, venue, year, abstract, topics, and official page when available.
2. Pull recent papers, influential papers, citation counts, references, citations, and related papers when available.
3. Compare Semantic Scholar results against at least one other source for important claims.
4. Use citation trails to identify neighboring methods, baselines, theory papers, implementation papers, and benchmark papers.
5. Feed serious papers into `paper-reading-note`, `paper-analyze`, or a project knowledge graph.

## Good Uses

- Finding related papers through citation and reference networks.
- Checking whether a method, benchmark, or implementation claim is supported by the literature.
- Identifying papers for a Muon reading queue or knowledge graph.

## Cautions

- Author and paper profiles can merge, split, or miss versions incorrectly.
- Citation counts are not evidence of correctness.
- Missing metadata should be marked as unknown.
