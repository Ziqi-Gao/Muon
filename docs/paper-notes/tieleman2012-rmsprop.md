# tieleman2012-rmsprop

## Metadata

- Title: Lecture 6.5 RMSProp: Divide the gradient by a running average of its recent magnitude
- Authors: Tijmen Tieleman; Geoffrey Hinton
- Year: 2012
- Venue/status: Coursera Neural Networks for Machine Learning lecture notes
- URLs: https://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf
- Identifiers: DOI=; arXiv=; OpenAlex=

## One-Sentence Role

Commonly cited original RMSProp lecture source; not a peer-reviewed paper.

## Core Ideas

First-pass extraction: Lecture 6.5 RMSProp: Divide the gradient by a running average of its recent magnitude is tagged as RMSProp; exponential moving average; optimizer lineage. It is included because it anchors the optimizer lineage, directly defines/analyzes Muon, or introduces a Muon-family variant.

## Mathematical Objects

Track the update equation, state variables, norm or preconditioner, and limiting assumptions in the next PDF-level pass. For Muon-family records, prioritize momentum handling, matrix shape, orthogonalization target, Newton-Schulz or polar approximation, scaling, and weight decay.

## Algorithmic Details

First-pass status only. Convert the source into executable pseudocode and compare against SGD, Momentum SGD, AdamW, Shampoo/SOAP, and Muon once the PDF/body text is read.

## Evidence and Limits

Evidence source: https://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf. This note is not yet a full paper read; it records discovery, role, and graph intent. Separate proved claims from empirical claims in the next phase.

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
- Evidence URLs: https://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf.
- Audit note: Commonly cited original RMSProp lecture source; not a peer-reviewed paper.

