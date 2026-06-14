# kingma2014-adam

## Metadata

- Title: Adam: A Method for Stochastic Optimization
- Authors: Diederik P. Kingma; Jimmy Ba
- Year: 2014
- Venue/status: ICLR 2015; arXiv
- URLs: https://arxiv.org/abs/1412.6980
- Identifiers: DOI=10.48550/arXiv.1412.6980; arXiv=1412.6980; OpenAlex=

## One-Sentence Role

Introduces Adam with bias-corrected first and second moment estimates.

## Core Ideas

First-pass extraction: Adam: A Method for Stochastic Optimization is tagged as Adam; adaptive optimizer; first moment; second moment. It is included because it anchors the optimizer lineage, directly defines/analyzes Muon, or introduces a Muon-family variant.

## Mathematical Objects

Track the update equation, state variables, norm or preconditioner, and limiting assumptions in the next PDF-level pass. For Muon-family records, prioritize momentum handling, matrix shape, orthogonalization target, Newton-Schulz or polar approximation, scaling, and weight decay.

## Algorithmic Details

First-pass status only. Convert the source into executable pseudocode and compare against SGD, Momentum SGD, AdamW, Shampoo/SOAP, and Muon once the PDF/body text is read.

## Evidence and Limits

Evidence source: https://arxiv.org/abs/1412.6980. This note is not yet a full paper read; it records discovery, role, and graph intent. Separate proved claims from empirical claims in the next phase.

## Graph Updates

Promote to graph as a core optimizer/Muon source with typed evidence edges.

## Open Questions

- What exact assumptions or benchmark settings support the headline claim?
- Which graph edges need stronger source locators?
- Does the method extend Muon, compare to Muon, or only share matrix/spectral machinery?
