# loshchilov2017-adamw

## Metadata

- Title: Decoupled Weight Decay Regularization
- Authors: Ilya Loshchilov; Frank Hutter
- Year: 2017
- Venue/status: ICLR 2019; arXiv
- URLs: https://arxiv.org/abs/1711.05101; https://openreview.net/forum?id=Bkg6RiCqY7
- Identifiers: DOI=10.48550/arXiv.1711.05101; arXiv=1711.05101; OpenAlex=

## One-Sentence Role

Separates weight decay from adaptive-gradient update; AdamW baseline for Muon comparisons.

## Core Ideas

First-pass extraction: Decoupled Weight Decay Regularization is tagged as AdamW; decoupled weight decay; optimizer lineage. It is included because it anchors the optimizer lineage, directly defines/analyzes Muon, or introduces a Muon-family variant.

## Mathematical Objects

Track the update equation, state variables, norm or preconditioner, and limiting assumptions in the next PDF-level pass. For Muon-family records, prioritize momentum handling, matrix shape, orthogonalization target, Newton-Schulz or polar approximation, scaling, and weight decay.

## Algorithmic Details

First-pass status only. Convert the source into executable pseudocode and compare against SGD, Momentum SGD, AdamW, Shampoo/SOAP, and Muon once the PDF/body text is read.

## Evidence and Limits

Evidence source: https://arxiv.org/abs/1711.05101; https://openreview.net/forum?id=Bkg6RiCqY7. This note is not yet a full paper read; it records discovery, role, and graph intent. Separate proved claims from empirical claims in the next phase.

## Graph Updates

Promote to graph as a core optimizer/Muon source with typed evidence edges.

## Open Questions

- What exact assumptions or benchmark settings support the headline claim?
- Which graph edges need stronger source locators?
- Does the method extend Muon, compare to Muon, or only share matrix/spectral machinery?
