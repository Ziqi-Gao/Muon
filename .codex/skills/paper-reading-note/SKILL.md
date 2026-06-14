---
name: paper-reading-note
description: Structured paper reading note skill for Muon and optimization research. Use when Codex needs to turn a paper into a concise card covering problem, method, assumptions, equations, experiments, contribution, relevance to Muon, implementation implications, and follow-up questions.
---

# Paper Reading Note

Adapted from PaperPilot and Research-Pilot style reading workflows.

## Procedure

1. Confirm the paper identity, version, authors, venue/preprint status, and relationship to the research question.
2. Record title, authors, year, venue, DOI or URL, and source checked date.
3. Record full-text access type and locator: open PDF URL, open HTML URL, arXiv source, repo-relative local PDF path, user-provided lawful PDF, or none.
4. Summarize the problem, method, assumptions, equations, experiments, and contribution.
5. Explain how the paper connects to Muon, related optimizers, optimization theory, implementation, or benchmarks.
6. Identify concrete follow-up questions for math, code, experiments, or knowledge-graph updates.
7. Mark whether the paper was fully read, targeted-full-read, abstract-read, or metadata-only.

## Output

| Field | Note |
|---|---|
| Problem | |
| Method | |
| Assumptions | |
| Key equations | |
| Experiments | |
| Contribution | |
| Muon relevance | |
| Implementation or math hook | |
| Question | |
| Source | |
| Full-text access | |
| Full-text locator | |
| Read status | |

## Rule

Do not claim to have read full text if only metadata or abstract was available. `targeted_full_read` and `full_read` require a lawful open full-text URL, arXiv source, or a repo-relative local PDF path.
