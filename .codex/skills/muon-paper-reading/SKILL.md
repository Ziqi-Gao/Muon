---
name: muon-paper-reading
description: Read and extract structured notes from Muon optimizer papers, optimizer-history papers, PDFs, arXiv papers, and related ML optimization literature. Use when Codex needs definitions, assumptions, algorithms, theorem statements, experiments, ablations, limitations, and citation-quality notes from papers.
---

# Muon Paper Reading

Use this skill to turn papers into reusable survey and graph evidence.

## Reading Passes

1. Metadata pass: title, authors, year, venue/status, URLs, code, datasets, models, and citation identifiers.
2. Contribution pass: problem, claimed novelty, baseline optimizers, where Muon or related methods enter.
3. Technical pass: definitions, update equations, assumptions, algorithm boxes, complexity, memory, communication, and hyperparameters.
4. Evidence pass: theorem/proof obligations, experiments, ablations, negative results, limitations, and reproducibility notes.
5. Graph pass: entities and relations to add to the optimizer knowledge graph.

## Note Template

Use concise Markdown:

```markdown
# Paper Slug

## Metadata

## One-Sentence Role

## Core Ideas

## Mathematical Objects

## Algorithmic Details

## Evidence and Limits

## Graph Updates

## Open Questions
```

## Extraction Rules

- Quote sparingly. Prefer paraphrase with page, section, theorem, algorithm, or figure references.
- Separate what the paper proves from what it empirically suggests.
- When a claim is important to the survey, attach at least one source locator.
- For Muon-family papers, always extract: orthogonalization method, momentum handling, normalization/scaling, weight decay, matrix shapes covered, optimizer-state memory, and comparison baselines.
