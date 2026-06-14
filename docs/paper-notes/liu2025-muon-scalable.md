# liu2025-muon-scalable

## Metadata

- Title: Muon is Scalable for LLM Training
- Authors: Jingyuan Liu; Jianlin Su; Xingcheng Yao; Zhejun Jiang; Guokun Lai; Yulun Du; Yidao Qin; Weixin Xu; Enzhe Lu; Junjie Yan; Yanru Chen; Huabin Zheng; Yibo Liu; Shaowei Liu; Bohong Yin; Weiran He; Han Zhu; Yuzhi Wang; Jianzhou Wang; Mengnan Dong; Zheng Zhang; Yongsheng Kang; Hao Zhang; Xinran Xu; Yutao Zhang; Yuxin Wu; Xinyu Zhou; Zhilin Yang
- Year: 2025
- Venue/status: arXiv
- URLs: https://arxiv.org/abs/2502.16982
- Identifiers: DOI=10.48550/arXiv.2502.16982; arXiv=2502.16982; OpenAlex=https://openalex.org/W4414846785

## One-Sentence Role

Scales Muon to large LLM/MoE training with weight decay and update scaling.

## Core Ideas

First-pass extraction: Muon is Scalable for LLM Training is tagged as Muon; LLM pretraining; Moonlight; scaling; weight decay. It is included because it anchors the optimizer lineage, directly defines/analyzes Muon, or introduces a Muon-family variant.

## Mathematical Objects

Track the update equation, state variables, norm or preconditioner, and limiting assumptions in the next PDF-level pass. For Muon-family records, prioritize momentum handling, matrix shape, orthogonalization target, Newton-Schulz or polar approximation, scaling, and weight decay.

## Algorithmic Details

First-pass status only. Convert the source into executable pseudocode and compare against SGD, Momentum SGD, AdamW, Shampoo/SOAP, and Muon once the PDF/body text is read.

## Evidence and Limits

Evidence source: https://arxiv.org/abs/2502.16982. This note is not yet a full paper read; it records discovery, role, and graph intent. Separate proved claims from empirical claims in the next phase.

## Graph Updates

Promote to graph as a core optimizer/Muon source with typed evidence edges.

## Open Questions

- What exact assumptions or benchmark settings support the headline claim?
- Which graph edges need stronger source locators?
- Does the method extend Muon, compare to Muon, or only share matrix/spectral machinery?
