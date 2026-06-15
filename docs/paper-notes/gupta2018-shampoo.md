# gupta2018-shampoo

## Metadata

- Title: Shampoo: Preconditioned Stochastic Tensor Optimization
- Authors: Vineet Gupta; Tomer Koren; Yoram Singer
- Year: 2018
- Venue/status: ICML 2018; arXiv
- URLs: https://arxiv.org/abs/1802.09568
- Identifiers: DOI=10.48550/arXiv.1802.09568; arXiv=1802.09568; OpenAlex=

## One-Sentence Role

Introduces structured tensor preconditioning and inverse-root matrix updates.

## Core Ideas

First-pass extraction: Shampoo: Preconditioned Stochastic Tensor Optimization is tagged as Shampoo; matrix preconditioning; tensor optimization. It is included because it anchors the optimizer lineage, directly defines/analyzes Muon, or introduces a Muon-family variant.

## Mathematical Objects

Track the update equation, state variables, norm or preconditioner, and limiting assumptions in the next PDF-level pass. For Muon-family records, prioritize momentum handling, matrix shape, orthogonalization target, Newton-Schulz or polar approximation, scaling, and weight decay.

## Algorithmic Details

First-pass status only. Convert the source into executable pseudocode and compare against SGD, Momentum SGD, AdamW, Shampoo/SOAP, and Muon once the PDF/body text is read.

## Evidence and Limits

Evidence source: https://arxiv.org/abs/1802.09568. This note is not yet a full paper read; it records discovery, role, and graph intent. Separate proved claims from empirical claims in the next phase.

## Graph Updates

Promote to graph as a core optimizer/Muon source with typed evidence edges.

## Open Questions

- What exact assumptions or benchmark settings support the headline claim?
- Which graph edges need stronger source locators?
- Does the method extend Muon, compare to Muon, or only share matrix/spectral machinery?

## Phase 2 Evidence Audit

- Search/cutoff date: 2026-06-14.
- Registry status: `included` / `core`.
- Evidence confidence: medium.
- Evidence URLs: https://arxiv.org/abs/1802.09568.
- Audit note: Introduces structured tensor preconditioning and inverse-root matrix updates.

