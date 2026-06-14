# chen2025-spectral-norm-muon

## Metadata

- Title: Muon Optimizes Under Spectral Norm Constraints
- Authors: Lizhang Chen; Jonathan Li; Qiang Liu
- Year: 2025
- Venue/status: arXiv
- URLs: https://arxiv.org/abs/2506.15054
- Identifiers: DOI=10.48550/arXiv.2506.15054; arXiv=2506.15054; OpenAlex=

## One-Sentence Role

Places Muon in a spectral-norm constrained optimization perspective through the Lion-K family.

## Core Ideas

First-pass extraction: Muon corresponds to a Lion-K-style optimizer when equipped with the nuclear norm, yielding an implicit spectral-norm constraint view for weight matrices.

## Mathematical Objects

Track the convex map K, nuclear norm/spectral norm duality, decoupled weight decay assumptions, and relation to implicit regularization.

## Algorithmic Details

First-pass status only. Extract exact update mapping from Muon to the Lion-K family in the next PDF-level pass.

## Evidence and Limits

Verified on arXiv on 2026-06-14. This note is not yet a full proof read.

## Graph Updates

Keep as a core Muon theory source; link to Muon and spectral-norm trust-region/constrained optimization concepts.

## Open Questions

- Does the theory cover the common Newton-Schulz approximation or an idealized orthogonalization?
- What role does decoupled weight decay play in the stated constrained problem?
- Which later Muon variants inherit this interpretation?
