# wang2026-vescale-fsdp

## Metadata

- Title: veScale-FSDP: Flexible and High-Performance FSDP at Scale
- Authors: Zezou Wang; Youjie Li; Zhiqi Lin; Jiacheng Yang; Cong Xie; Guanyu Feng; Zheng Zhong; Ziyue Huang; Hongyu Zhu; Zhi Zhang; Yanghua Peng; Xin Liu
- Year: 2026
- Venue/status: arXiv
- URLs: https://arxiv.org/abs/2602.22437
- Identifiers: DOI=10.48550/arXiv.2602.22437; arXiv=2602.22437; OpenAlex=

## One-Sentence Role

Phase 2 web search found the veScale-FSDP report; its abstract explicitly lists Muon as a non-element-wise optimizer that current FSDP systems struggle to support.

## Core Ideas

Phase 2 first-pass note. This source is classified as `included` / `adjacent` for the Muon survey because it directly addresses Muon, a Muon-family variant, matrix orthogonalization machinery, or systems support for non-element-wise Muon-style optimizers.

## Mathematical Objects

Extract in the next PDF-level pass: parameter matrix, momentum buffer, orthogonalization or polar map, Newton-Schulz or alternative approximation, scaling rule, weight decay, adaptive state, and the norm or trust-region geometry used in the paper.

## Algorithmic Details

Record pseudocode, optimizer state memory, communication pattern, matrix-shape assumptions, and comparison baselines. For systems reports, separate optimizer design from implementation/sharding constraints.

## Evidence and Limits

- Search/cutoff date: 2026-06-14.
- Evidence confidence: high.
- Evidence URLs: https://arxiv.org/abs/2602.22437.
- This is a corpus-audit note, not yet a full paper read. Claims should be upgraded only after reading the PDF/body text and locating theorem, algorithm, table, or figure references.

## Graph Updates

Add or verify paper node `wang2026-vescale-fsdp`, source row `wang2026-vescale-fsdp`, and typed graph edges to Muon, method variants, or concepts with source-backed confidence.

## Open Questions

- Which exact theorem assumptions, benchmark settings, or implementation details support the headline claim?
- Does the paper introduce a new optimizer, analyze existing Muon, or report an application/system use?
- Which survey table should this paper feed: theory, variants, systems, quantization, scaling, or empirical behavior?
