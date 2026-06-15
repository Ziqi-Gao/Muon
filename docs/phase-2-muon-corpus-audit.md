# Phase 2 Muon Corpus Audit

Search and audit date: 2026-06-14

## Scope

This audit expands the Phase 1 Muon survey corpus through the cutoff date 2026-06-14. It does not claim that the literature is exhausted. It records a bounded search over arXiv, Semantic Scholar-oriented web/API checks, OpenAlex-oriented web checks, OpenReview search, GitHub repository search, author/project pages, and technical blogs/pages.

## Local Git Safety

- Local Git executable is available, but `.git-local` is still pinned to old commit `13bb52dc96c86fd233df08db8134130c622b198e`.
- `git fetch origin main` failed because `.git-local/FETCH_HEAD` is not writable in this environment.
- Shell network to GitHub is blocked, so this run avoids reset/rebase/fetch mutations and treats the local Phase 1 files as the working baseline already pushed to remote main `db240998a962be388e0532e3196d67e516c60377`.

## Search Sources

- arXiv abstract pages and arXiv-search result pages for Muon, Newton-Schulz, matrix orthogonalization, spectral Muon, and optimizer variants.
- Semantic Scholar targeted checks through web/API-style queries; direct shell API calls were blocked by network policy in this environment.
- OpenAlex targeted checks through web-indexed queries plus Phase 1 OpenAlex IDs; direct shell API calls were blocked by network policy.
- OpenReview targeted web search for `Muon optimizer`, `BlockMuon`, and orthogonalization-in-Muon phrases; no clear new OpenReview primary record was found in this pass.
- GitHub repository search for official or paper-linked code, especially MuonQ and modded-nanogpt/BeyondMuon-style repositories.
- Author/project pages and technical reports, including Keller Jordan's Muon page and Kimi K2/MuonClip search hits.

## Query Families

- `site:arxiv.org/abs Muon optimizer orthogonalization 2026`
- `site:arxiv.org/abs "Muon" "optimizer" "Newton-Schulz"`
- `"Muon optimizer" "2026" "arXiv" "orthogonalization"`
- `"Muon optimizer" "2025" "arXiv" "orthogonalization"`
- `"AMO: Adaptive Muon Orthogonalization"`
- `"NuMuon: Nuclear-Norm-Constrained Muon"`
- `"Spectral Scaling Laws of Muon"`
- `"Why Muon Outperforms Adam: A Curvature Perspective"`
- `"Denoise First, Orthogonalize Later" Muon`
- `"Kimi K2" Muon optimizer MuonClip`
- GitHub repository searches: `MuonQ optimizer`, `BeyondMuon optimizer`, `modded-nanogpt Muon`, `Muon optimizer Newton Schulz`.

## Inclusion Criteria

- Directly introduces, analyzes, scales, quantizes, distributes, or benchmarks Muon or a named Muon-family optimizer.
- Studies Muon's matrix orthogonalization, Newton-Schulz/polar approximation, spectral geometry, convergence, negative results, or momentum behavior.
- Provides systems evidence for implementing non-element-wise Muon-style optimizers.
- Historically anchors the SGD-to-Shampoo/SOAP-to-Muon optimizer lineage.

## Exclusion Criteria

- Physics/collider/tomography/spectrometer records where "muon" is not an optimizer.
- Weak application papers that mention Muon without optimizer evidence remain `candidate`.
- Secondary commentary without primary paper/page support is not promoted.

## Registry Delta

- Total registry rows: 146
- Included: 115
- Candidate: 28
- Excluded: 3
- Phase 2 promoted rows: 76
- Newly added rows: 3

## Newly Added Records

- `kimi2025-k2-muonclip`: Kimi K2: Open Agentic Intelligence (2025)
- `wang2026-vescale-fsdp`: veScale-FSDP: Flexible and High-Performance FSDP at Scale (2026)
- `lim2025-motif2-parallel-muon`: Motif 2 12.7B technical report (2025)

## Promoted Examples

- `arxiv-250416041-muon-optimizer-accelerates-grokking`: Muon Optimizer Accelerates Grokking
- `arxiv-250504005-iterative-orthogonalization-scaling-laws`: Iterative Orthogonalization Scaling Laws
- `arxiv-250604430-leveraging-coordinate-momentum-in-signsg`: Leveraging Coordinate Momentum in SignSGD and Muon: Memory-Optimized Zero-Order
- `arxiv-250610935-accelerating-newton-schulz-iteration-for`: Accelerating Newton-Schulz Iteration for Orthogonalization via Chebyshev-type Polynomials
- `arxiv-250902981-adagrad-meets-muon-adaptive-stepsizes-fo`: AdaGrad Meets Muon: Adaptive Stepsizes for Orthogonal Updates
- `arxiv-250911983-low-rank-orthogonalization-for-large-sca`: Low-rank Orthogonalization for Large-scale Matrix Optimization with Applications to Foundation Model Training
- `arxiv-250914562-limuon-light-and-fast-muon-optimizer-for`: LiMuon: Light and Fast Muon Optimizer for Large Models
- `arxiv-250915816-on-the-convergence-of-muon-and-beyond`: On the Convergence of Muon and Beyond
- `arxiv-250924406-muon-training-and-trade-offs-with-latent`: Muon: Training and Trade-offs with Latent Attention and MoE
- `arxiv-250926030-muon-outperforms-adam-in-tail-end-associ`: Muon Outperforms Adam in Tail-End Associative Memory Learning
- `arxiv-250926337-fedmuon-federated-learning-with-bias-cor`: FedMuon: Federated Learning with Bias-corrected LMO-based Optimization
- `arxiv-251000643-error-feedback-for-muon-and-friends`: Error Feedback for Muon and Friends
- `arxiv-251002239-drop-muon-update-less-converge-faster`: Drop-Muon: Update Less, Converge Faster
- `arxiv-251003866-on-provable-benefits-of-muon-in-federate`: On Provable Benefits of Muon in Federated Learning
- `arxiv-251005491-normuon-making-muon-more-efficient-and-s`: NorMuon: Making Muon more efficient and scalable
- `arxiv-251006627-pome-post-optimization-model-edit-via-mu`: POME: Post Optimization Model Edit via Muon-style Projection
- `arxiv-251009827-an-exploration-of-non-euclidean-gradient`: An Exploration of Non-Euclidean Gradient Descent: Muon and its Many Variants
- `arxiv-251019933-beyond-the-ideal-analyzing-the-inexact-m`: Beyond the Ideal: Analyzing the Inexact Muon Update
- `arxiv-251022980-how-muon-s-spectral-design-benefits-gene`: How Muon's Spectral Design Benefits Generalization: A Study on Imbalanced Data
- `arxiv-251106086-muonall-muon-variant-for-efficient-finet`: MuonAll: Muon Variant for Efficient Finetuning of Large Language Models
- `arxiv-251204632-turbo-muon-accelerating-orthogonality-ba`: Turbo-Muon: Accelerating Orthogonality-Based Optimization with Pre-Conditioning
- `arxiv-251216598-muon-is-provably-faster-with-momentum-va`: Muon is Provably Faster with Momentum Variance Reduction
- `arxiv-251216928-dion2-a-simple-method-to-shrink-matrix-i`: Dion2: A Simple Method to Shrink Matrix in Muon
- `arxiv-260101306-towards-a-principled-muon-under-mu-maths`: Towards a Principled Muon under $mu\mathsf{P}$: Ensuring Spectral Conditions throughout Training
- `arxiv-260109865-advancing-model-refinement-muon-optimize`: Advancing Model Refinement: Muon-Optimized Distillation and Quantization for LLM Deployment
- `arxiv-260119400-improved-convergence-rates-of-muon-optim`: Improved Convergence Rates of Muon Optimizer for Nonconvex Optimization
- `arxiv-260202500-ifnso-iteration-free-newton-schulz-ortho`: IFNSO: Iteration-Free Newton-Schulz Orthogonalization
- `arxiv-260205725-muon-in-associative-memory-learning-trai`: Muon in Associative Memory Learning: Training Dynamics and Scaling Laws
- `arxiv-260206385-uniform-spectral-growth-and-convergence-`: Uniform Spectral Growth and Convergence of Muon in LoRA-Style Matrix Factorization
- `arxiv-260211948-insights-on-muon-from-simple-quadratics`: Insights on Muon from Simple Quadratics
- `arxiv-260213498-trasmuon-trust-region-adaptive-scaling-f`: TrasMuon: Trust-Region Adaptive Scaling for Orthogonalized Momentum Optimizers
- `arxiv-260216167-muon-with-spectral-guidance-efficient-op`: Muon with Spectral Guidance: Efficient Optimization for Scientific Machine Learning
- `arxiv-260216340-the-implicit-bias-of-adam-and-muon-on-sm`: The Implicit Bias of Adam and Muon on Smooth Homogeneous Neural Networks
- `arxiv-260217080-adam-improves-muon-adaptive-moment-estim`: Adam Improves Muon: Adaptive Moment Estimation with Orthogonalized Momentum
- `arxiv-260221545-muon-towards-more-effective-muon-via-one`: MUON+: Towards More Effective Muon via One Additional Normalization Step for LLM Pre-training

## Remaining Risks And Open Questions

- Several 2026 arXiv records are very recent; version, code, and venue status may drift after 2026-06-14.
- Some Phase 2 promotions rely on title/abstract-level evidence and need PDF-level theorem/algorithm/table locators before survey prose.
- OpenReview and OpenAlex direct API access was not available from shell in this environment, so those checks are recorded as web-targeted rather than exhaustive API sweeps.
- Kimi K2/MuonClip and veScale-FSDP are important systems signals, but optimizer-specific details should be extracted from body sections before graph confidence is raised beyond the current source-level classification.
- Do not phrase the corpus as "complete"; phrase it as "bounded search through 2026-06-14 with recorded sources and query families."

## Next Reading Priority

- `li2025-note-convergence-muon`: A Note on the Convergence of Muon
- `arxiv-250902981-adagrad-meets-muon-adaptive-stepsizes-fo`: AdaGrad Meets Muon: Adaptive Stepsizes for Orthogonal Updates
- `si2025-adamuon`: AdaMuon: Adaptive Muon Optimizer
- `arxiv-251009827-an-exploration-of-non-euclidean-gradient`: An Exploration of Non-Euclidean Gradient Descent: Muon and its Many Variants
- `arxiv-251019933-beyond-the-ideal-analyzing-the-inexact-m`: Beyond the Ideal: Analyzing the Inexact Muon Update
- `sato2025-critical-batch-muon`: Convergence Bound and Critical Batch Size of Muon Optimizer
- `arxiv-251001377-demuon-a-decentralized-muon-for-matrix-o`: DeMuon: A Decentralized Muon for Matrix Optimization over Graphs
- `arxiv-251216928-dion2-a-simple-method-to-shrink-matrix-i`: Dion2: A Simple Method to Shrink Matrix in Muon
- `arxiv-251002239-drop-muon-update-less-converge-faster`: Drop-Muon: Update Less, Converge Faster
- `gupta2025-effective-quantization-muon`: Effective Quantization of Muon Optimizer States
- `arxiv-251000643-error-feedback-for-muon-and-friends`: Error Feedback for Muon and Friends
- `liu2025-fedmuon-accel`: FedMuon: Accelerating Federated Learning with Matrix Orthogonalization
- `arxiv-250926337-fedmuon-federated-learning-with-bias-cor`: FedMuon: Federated Learning with Bias-corrected LMO-based Optimization
- `arxiv-251022980-how-muon-s-spectral-design-benefits-gene`: How Muon's Spectral Design Benefits Generalization: A Study on Imbalanced Data
- `arxiv-250604430-leveraging-coordinate-momentum-in-signsg`: Leveraging Coordinate Momentum in SignSGD and Muon: Memory-Optimized Zero-Order
- `arxiv-250914562-limuon-light-and-fast-muon-optimizer-for`: LiMuon: Light and Fast Muon Optimizer for Large Models
- `bogachev2025-riemannion`: LoRA meets Riemannion: Muon Optimizer for Parametrization-independent Low-Rank Adapters
- `therien2025-muloco`: MuLoCo: Muon is a practical inner optimizer for DiLoCo
- `arxiv-251216598-muon-is-provably-faster-with-momentum-va`: Muon is Provably Faster with Momentum Variance Reduction
- `liu2025-muon-scalable`: Muon is Scalable for LLM Training
- `arxiv-250416041-muon-optimizer-accelerates-grokking`: Muon Optimizer Accelerates Grokking
- `chen2025-spectral-norm-muon`: Muon Optimizes Under Spectral Norm Constraints
- `arxiv-250926030-muon-outperforms-adam-in-tail-end-associ`: Muon Outperforms Adam in Tail-End Associative Memory Learning
- `arxiv-250924406-muon-training-and-trade-offs-with-latent`: Muon: Training and Trade-offs with Latent Attention and MoE
- `arxiv-251106086-muonall-muon-variant-for-efficient-finet`: MuonAll: Muon Variant for Efficient Finetuning of Large Language Models
- `khaled2025-muonbp`: MuonBP: Faster Muon via Block-Periodic Orthogonalization
- `arxiv-251005491-normuon-making-muon-more-efficient-and-s`: NorMuon: Making Muon more efficient and scalable
- `arxiv-251003866-on-provable-benefits-of-muon-in-federate`: On Provable Benefits of Muon in Federated Learning
- `arxiv-250915816-on-the-convergence-of-muon-and-beyond`: On the Convergence of Muon and Beyond
- `arxiv-251006627-pome-post-optimization-model-edit-via-mu`: POME: Post Optimization Model Edit via Muon-style Projection
- `shah2025-practical-efficiency-muon`: Practical Efficiency of Muon for Pretraining
- `amsel2025-polar-express`: The Polar Express: Optimal Matrix Sign Methods and Their Application to the Muon Algorithm
- `arxiv-251204632-turbo-muon-accelerating-orthogonality-ba`: Turbo-Muon: Accelerating Orthogonality-Based Optimization with Pre-Conditioning
- `arxiv-260404726-a-muon-accelerated-algorithm-for-low-sep`: A Muon-Accelerated Algorithm for Low Separation Rank Tensor Generalized Linear Models
- `arxiv-260217080-adam-improves-muon-adaptive-moment-estim`: Adam Improves Muon: Adaptive Moment Estimation with Orthogonalized Momentum
- `arxiv-260109865-advancing-model-refinement-muon-optimize`: Advancing Model Refinement: Muon-Optimized Distillation and Quantization for LLM Deployment
- `arxiv-260517806-amo-adaptive-muon-orthogonalization`: AMO: Adaptive Muon Orthogonalization
- `arxiv-260522432-amuse-anytime-muon-with-stable-gradient-`: AMUSE: Anytime Muon with Stable Gradient Evaluation
- `arxiv-260317970-beyond-muon-mud-momentum-decorrelation-f`: Beyond Muon: MUD (MomentUm Decorrelation) for Faster Transformer Training
- `arxiv-260510468-can-muon-fine-tune-adam-pretrained-model`: Can Muon Fine-tune Adam-Pretrained Models?
