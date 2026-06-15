# zhang2026-teon

## Metadata

- Title: TEON: Tensorized Orthonormalization Beyond Layer-Wise Muon for Large Language Model Pre-Training
- Authors: Ruijie Zhang; Yequan Zhao; Ziyue Liu; Zhengyang Wang; Dongyang Li; Yupeng Su; Sijia Liu; Zheng Zhang
- Year: 2026
- Venue/status: arXiv
- URLs: https://arxiv.org/abs/2601.23261
- Identifiers: DOI=; arXiv=2601.23261; OpenAlex=

## One-Sentence Role

Generalizes Muon's layer-wise matrix orthogonalization to structured higher-order tensor orthonormalization.

## Core Ideas

First-pass extraction: TEON models neural-network gradients as structured higher-order tensors and applies tensorized orthonormalization beyond independent layer-wise Muon updates.

## Mathematical Objects

Track tensor representation, orthonormalization objective, approximation method, and convergence comparison against layer-wise Muon.

## Algorithmic Details

First-pass status only. Extract practical instantiation details, approximate SVD schemes, and compatibility with GPT/LLaMA architectures.

## Evidence and Limits

Verified via arXiv search result on 2026-06-14. Full paper-level extraction is still needed.

## Graph Updates

Keep TEON as a method node extending Muon.

## Open Questions

- What tensor structure is assumed for gradients?
- How much additional compute and communication does TEON require?
- Which results should enter the Muon survey comparison table?

## Phase 2 Evidence Audit

- Search/cutoff date: 2026-06-14.
- Registry status: `included` / `core`.
- Evidence confidence: high.
- Evidence URLs: https://arxiv.org/abs/2601.23261.
- Audit note: Generalizes layer-wise Muon to structured higher-order gradient tensors.

