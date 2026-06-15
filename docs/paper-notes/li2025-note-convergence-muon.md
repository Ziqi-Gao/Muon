# li2025-note-convergence-muon

## Metadata

- Title: A Note on the Convergence of Muon
- Authors: Jiaxiang Li; Mingyi Hong
- Year: 2025
- Venue/status: arXiv
- URLs: https://arxiv.org/abs/2502.02900
- Identifiers: DOI=10.48550/arXiv.2502.02900; arXiv=2502.02900; OpenAlex=

## One-Sentence Role

Early theory note connecting Muon to spectral-norm steepest descent and convergence analysis.

## Core Ideas

First-pass extraction: the paper interprets Muon as a specialized steepest descent method whose update direction minimizes a quadratic approximation under a spectral-norm constraint.

## Mathematical Objects

Track the objective approximation, spectral norm constraint, Muon variants analyzed, and convergence assumptions in the next PDF-level pass.

## Algorithmic Details

First-pass status only. Compare the update equations against base Muon, momentum Muon, AdamW, and spectral/nuclear norm steepest descent.

## Evidence and Limits

Verified on arXiv on 2026-06-14. This note is not yet a full theorem-level read.

## Graph Updates

Keep as a core Muon theory source with an `analyzes` edge to Muon.

## Open Questions

- Which Muon variant does each convergence statement cover?
- What assumptions differ from practical LLM training settings?
- How should the spectral-norm view connect to later trust-region and Lion-K analyses?

## Phase 2 Evidence Audit

- Search/cutoff date: 2026-06-14.
- Registry status: `included` / `core`.
- Evidence confidence: medium.
- Evidence URLs: https://arxiv.org/abs/2502.02900.
- Audit note: Early theory note connecting Muon to spectral-norm steepest descent.

