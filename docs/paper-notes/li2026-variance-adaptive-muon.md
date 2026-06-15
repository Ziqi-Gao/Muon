# li2026-variance-adaptive-muon

## Metadata

- Title: Variance-Adaptive Muon: Accelerating LLM Pretraining with NSR-Modulated and Variance-Scaled Momentum
- Authors: Jingru Li; Yibo Fan; Huan Li
- Year: 2026
- Venue/status: arXiv
- URLs: https://arxiv.org/abs/2601.14603
- Identifiers: DOI=10.48550/arXiv.2601.14603; arXiv=2601.14603; OpenAlex=

## One-Sentence Role

Introduces variance-adaptive Muon variants that normalize momentum before orthogonalization for LLM pretraining.

## Core Ideas

First-pass extraction: the paper proposes Muon-NSR and Muon-VS, motivated by the view of Adam as a variance-adaptive sign update, and applies variance adaptation before Muon orthogonalization.

## Mathematical Objects

Track NSR modulation, variance-scaled momentum, orthogonalization target, and how the variants alter Muon's momentum matrix.

## Algorithmic Details

First-pass status only. Extract pseudocode and compare added state/memory against Muon, AdamW, AdaMuon, and Muon^2.

## Evidence and Limits

Verified on arXiv on 2026-06-14. Reported experiments include GPT-2 and LLaMA pretraining; full benchmark details need PDF-level extraction.

## Graph Updates

Add or keep method nodes for Muon-NSR and Muon-VS if the next phase extracts stable algorithm definitions.

## Open Questions

- Does the method introduce additional optimizer state beyond Muon?
- How is variance estimated and normalized across matrix shapes?
- Which baselines and model scales are most important for the survey table?

## Phase 2 Evidence Audit

- Search/cutoff date: 2026-06-14.
- Registry status: `included` / `core`.
- Evidence confidence: high.
- Evidence URLs: https://arxiv.org/abs/2601.14603.
- Audit note: Adds variance-adaptive normalization to Muon momentum before orthogonalization.

