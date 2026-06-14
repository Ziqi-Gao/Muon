---
name: risk-and-evidence-audit
description: Evidence matrix and risk audit skill for Muon and optimization research. Use when Codex needs to verify that technical claims, paper summaries, benchmark interpretations, implementation notes, math derivations, source logs, or knowledge-graph edges are source-backed, dated, confidence-labeled, and free of hallucinated claims.
---

# Risk And Evidence Audit

## Procedure

1. Read the relevant notes, source logs, paper cards, experiment records, knowledge graph rows, and memory snapshots if present locally.
2. For every important judgment, identify source URL, source ID when available, checked date, confidence, and evidence note.
3. Update or propose rows for `data/evidence-matrix.csv` or `knowledge/evidence-matrix.csv` when those trackers exist.
4. Append or propose memory events for evidence additions, evidence revisions, risk additions, and risk resolutions when a project memory folder is available.
5. Flag missing sources, stale sources, weak inferences, name-collision risks, version drift, benchmark drift, and overconfident math or implementation claims.
6. Separate fact, inference, unknown, and risk lead.
7. Recommend downgrade, removal, or further checking when evidence is weak.

## Criteria

- source_identity
- method_claim
- math_claim
- implementation_claim
- benchmark_claim
- version_or_commit_context
- full_text_access
- evidence_confidence
- open_question

## Output

- Evidence matrix updates.
- Memory event IDs or proposed events for evidence/risk changes, when memory exists.
- Unsupported claims.
- Risk list.
- Priority recommendation.

## Rule

Structured trackers and source notes are operational truth. Memory events explain how and why evidence or risk state changed. Memory snapshots are not the source of truth.
