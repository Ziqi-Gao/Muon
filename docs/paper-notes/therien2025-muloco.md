# therien2025-muloco

## Metadata

- Title: MuLoCo: Muon is a practical inner optimizer for DiLoCo
- Authors: Benjamin Therien; Xiaolong Huang; Aaron Defazio; Irina Rish; Eugene Belilovsky
- Year: 2025
- Venue/status: arXiv
- URLs: https://arxiv.org/abs/2505.23725
- Identifiers: DOI=10.48550/arXiv.2505.23725; arXiv=2505.23725; OpenAlex=

## One-Sentence Role

Uses Muon as the inner optimizer in distributed low-communication training.

## Core Ideas

Phase 2 first-pass note. This source is classified as `included` / `adjacent` for the Muon survey because it directly addresses Muon, a Muon-family variant, matrix orthogonalization machinery, or systems support for non-element-wise Muon-style optimizers.

## Mathematical Objects

Extract in the next PDF-level pass: parameter matrix, momentum buffer, orthogonalization or polar map, Newton-Schulz or alternative approximation, scaling rule, weight decay, adaptive state, and the norm or trust-region geometry used in the paper.

## Algorithmic Details

Record pseudocode, optimizer state memory, communication pattern, matrix-shape assumptions, and comparison baselines. For systems reports, separate optimizer design from implementation/sharding constraints.

## Evidence and Limits

- Search/cutoff date: 2026-06-14.
- Evidence confidence: medium.
- Evidence URLs: https://arxiv.org/abs/2505.23725.
- This is a corpus-audit note, not yet a full paper read. Claims should be upgraded only after reading the PDF/body text and locating theorem, algorithm, table, or figure references.

## Graph Updates

Add or verify paper node `therien2025-muloco`, source row `therien2025-muloco`, and typed graph edges to Muon, method variants, or concepts with source-backed confidence.

## Open Questions

- Which exact theorem assumptions, benchmark settings, or implementation details support the headline claim?
- Does the paper introduce a new optimizer, analyze existing Muon, or report an application/system use?
- Which survey table should this paper feed: theory, variants, systems, quantization, scaling, or empirical behavior?
