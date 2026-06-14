# duchi2011-adagrad

## Metadata

- Title: Adaptive Subgradient Methods for Online Learning and Stochastic Optimization
- Authors: John Duchi; Elad Hazan; Yoram Singer
- Year: 2011
- Venue/status: JMLR
- URLs: https://jmlr.org/papers/v12/duchi11a.html
- Identifiers: DOI=; arXiv=; OpenAlex=

## One-Sentence Role

Introduces AdaGrad and accumulated squared-gradient geometry.

## Core Ideas

First-pass extraction: Adaptive Subgradient Methods for Online Learning and Stochastic Optimization is tagged as AdaGrad; adaptive stepsizes; optimizer lineage. It is included because it anchors the optimizer lineage, directly defines/analyzes Muon, or introduces a Muon-family variant.

## Mathematical Objects

Track the update equation, state variables, norm or preconditioner, and limiting assumptions in the next PDF-level pass. For Muon-family records, prioritize momentum handling, matrix shape, orthogonalization target, Newton-Schulz or polar approximation, scaling, and weight decay.

## Algorithmic Details

First-pass status only. Convert the source into executable pseudocode and compare against SGD, Momentum SGD, AdamW, Shampoo/SOAP, and Muon once the PDF/body text is read.

## Evidence and Limits

Evidence source: https://jmlr.org/papers/v12/duchi11a.html. This note is not yet a full paper read; it records discovery, role, and graph intent. Separate proved claims from empirical claims in the next phase.

## Graph Updates

Promote to graph as a core optimizer/Muon source with typed evidence edges.

## Open Questions

- What exact assumptions or benchmark settings support the headline claim?
- Which graph edges need stronger source locators?
- Does the method extend Muon, compare to Muon, or only share matrix/spectral machinery?
