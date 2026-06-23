# Matrix-Orthogonalized Momentum for Neural Network Training: A Survey of Muon

Cutoff date: 2026-06-23  
Workbench corpus: `data/paper-registry.csv`, `docs/paper-notes/`, `data/optimizer-graph/`  
Status: formal survey draft, evidence-bounded and ready for iterative expansion

## Abstract

Muon is a new optimizer family for neural-network training built around a compact idea: take a momentum update for a matrix-shaped hidden-layer parameter, replace that matrix by an approximately orthogonal polar-factor direction, and then apply the update with practical scaling and regularization rules. The original public formulation, "MomentUm Orthogonalized by Newton-Schulz", uses a short Newton-Schulz polynomial iteration to approximate matrix orthogonalization without an SVD, making the method plausible for accelerator-heavy transformer training. In less than two years, Muon has moved from competitive small-model speedruns to large-scale language-model pretraining reports, while also spawning a rapidly expanding theoretical and systems literature.

This survey reviews Muon through three lenses. First, we place Muon in the optimizer lineage from SGD and momentum to AdaGrad, RMSProp, Adam, AdamW, Shampoo, SOAP, and matrix-orthogonalized updates. Second, we synthesize the mathematical views that currently explain Muon: polar factors, spectral flattening, spectral-norm trust regions, curvature penalties, finite Newton-Schulz approximation, and regime-dependent noise geometry. Third, we organize the 2025-2026 Muon ecosystem into variants for scaling, adaptivity, low-rank fine-tuning, quantization, distributed training, federated learning, and negative or boundary results.

The central conclusion is deliberately cautious. Muon is not simply "AdamW but better." It is a matrix-geometry optimizer whose advantages appear strongest when many hidden-layer spectral directions should remain active, when the cost of orthogonalization is amortized by large batches, and when baseline AdamW tuning is strong enough to make the comparison meaningful. The literature also contains credible warnings: Muon can be architecture-sensitive, workload-sensitive, and sensitive to exact implementation choices. A serious Muon survey must therefore treat theory, systems implementation, and negative results as co-equal parts of the story.

## 1. Scope and Method

This survey is based on a local Muon Research Workbench corpus and a targeted re-check on 2026-06-23. The Phase 2 registry contains 146 source records: 115 included, 28 candidate, and 3 excluded. Included records cover optimizer-lineage papers, Muon papers, official technical pages, theory notes, systems reports, implementation repositories, and closely related matrix-orthogonalization work. Candidate records remain in the registry when their title or abstract is relevant but the optimizer-specific evidence has not yet been checked deeply enough.

The corpus uses the following inclusion criteria:

- The source introduces, analyzes, scales, quantizes, distributes, or benchmarks Muon or a named Muon-family method.
- The source studies matrix orthogonalization, Newton-Schulz or polar approximation, spectral geometry, convergence, or negative behavior in a way that directly affects the Muon survey.
- The source historically anchors the optimizer lineage from SGD and AdamW to Shampoo, SOAP, and Muon.
- The source provides official code, an official technical report, or implementation details for Muon-like training.

The corpus uses the following exclusion criteria:

- Physics, detector, collider, spectrometer, or tomography records where "muon" is a particle keyword rather than an optimizer keyword.
- Secondary commentary without a primary paper, official page, official code repository, or author-controlled technical source.
- Weak application papers that merely mention Muon without a method, analysis, implementation, or benchmark contribution.

Search sources included arXiv pages, Semantic Scholar-oriented checks, OpenAlex-oriented checks, OpenReview search, GitHub repository search, author/project pages, and technical blogs. The survey does not claim full completeness beyond this bounded search. The literature is moving quickly, especially for 2026 arXiv preprints.

## 2. Historical Lineage: From Diagonal Adaptivity to Matrix Geometry

Muon is easiest to understand as the point where two optimizer histories meet: momentum-based first-order optimization and matrix-aware preconditioning.

### 2.1 SGD and Momentum

Stochastic gradient methods update parameters using noisy gradient estimates. Momentum adds a velocity state, often written

\[
m_t = \beta m_{t-1} + g_t, \qquad w_{t+1} = w_t - \eta m_t.
\]

The key idea is temporal smoothing: use previous gradients to reduce noise and build a persistent direction. Muon keeps this momentum template but changes the geometry of the update when the parameter is a matrix. Instead of applying the raw matrix momentum \(M_t\), Muon orthogonalizes it.

### 2.2 AdaGrad, RMSProp, Adam, and AdamW

AdaGrad introduced coordinate-wise scaling through accumulated squared gradients. RMSProp replaced pure accumulation by an exponential moving average of recent squared gradients. Adam combines a first-moment estimate and a second-moment estimate:

\[
m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t,
\]

\[
v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2,
\]

\[
w_{t+1} = w_t - \eta \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
\]

AdamW changed the regularization story by decoupling weight decay from the adaptive gradient step. This matters for Muon because AdamW is the practical default baseline in modern transformer training, and because Muon implementations often still use AdamW for embeddings, output heads, scalar parameters, and vector parameters.

### 2.3 Shampoo and SOAP

Shampoo generalizes diagonal adaptivity to structured tensor preconditioning. For a matrix or tensor parameter, it maintains preconditioner matrices along tensor dimensions and applies inverse-root transformations to the gradient. This is geometrically richer than AdamW, but it is also more complex: matrix inverse roots, eigendecompositions, memory layout, and distributed training are all harder than diagonal moment updates.

SOAP, "Shampoo with Adam in the preconditioner's eigenbasis", reduces some of this burden by combining Shampoo's matrix preconditioning with Adam-like second moments in the preconditioner eigenbasis. SOAP is important in the Muon lineage for two reasons. First, it reinforces that non-diagonal geometry can be useful in language-model pretraining. Second, it clarifies a design space between diagonal AdamW and full matrix preconditioning.

### 2.4 Muon as Accumulation-Free Matrix Geometry

Muon can be viewed as a cheaper, instantaneous member of this matrix-geometry family. The original Muon writeup observes that an accumulation-free form of Shampoo-like preconditioning leads to a polar-factor update \(UV^\top\) for a gradient matrix \(G = U\Sigma V^\top\). Muon then adds momentum before orthogonalization and uses Newton-Schulz iterations rather than an SVD.

This gives a useful conceptual chain:

\[
\text{AdamW: diagonal adaptive geometry}
\rightarrow
\text{Shampoo/SOAP: accumulated matrix preconditioning}
\rightarrow
\text{Muon: instantaneous polar-factor geometry on momentum}.
\]

The chain is conceptual, not a strict derivation. Muon is not simply Shampoo with a switch turned off; it is a practical optimizer recipe with its own parameter-selection rules, scaling rules, and implementation constraints.

## 3. Core Muon Formulation

Let \(W_t \in \mathbb{R}^{m \times n}\) be a hidden-layer weight matrix and \(G_t = \nabla_W L_t(W_t)\) be its stochastic gradient. A simplified Muon update has three stages.

Momentum:

\[
M_t = \beta M_{t-1} + G_t.
\]

Orthogonalization:

\[
O_t \approx \operatorname{polar}(M_t) = U V^\top,
\qquad M_t = U \Sigma V^\top.
\]

Parameter update:

\[
W_{t+1} = W_t - \eta\, s(W_t)\, O_t.
\]

Here \(s(W_t)\) denotes an implementation-dependent update scale. Real training recipes may include Nesterov-style momentum, decoupled weight decay, parameter-wise scaling, optimizer grouping, and separate AdamW updates for parameters outside Muon's intended scope.

### 3.1 Parameter Scope

Muon is designed for 2D hidden-layer matrices. The original implementation recommends using standard optimizers such as AdamW for scalar and vector parameters, input embeddings, output heads, and other parameters whose role or shape does not match the hidden-layer matrix assumption. Convolutional filters can sometimes be flattened into matrices, but this is a design choice rather than a theorem.

This scope restriction is not cosmetic. It is one of the main reasons Muon can be practical: the method spends extra computation on matrix orthogonalization only where the matrix structure is expected to matter.

### 3.2 Newton-Schulz Approximation

Exact polar decomposition by SVD is too expensive for routine optimizer steps. Muon instead uses a short polynomial Newton-Schulz-style iteration. Starting from a normalized matrix \(X\), one step can be written as

\[
X \leftarrow aX + b(XX^\top)X + c(XX^\top)^2X,
\]

where \(a,b,c\) are tuned coefficients. If \(X = U\Sigma V^\top\), the iteration transforms singular values by a scalar polynomial while preserving singular vectors:

\[
X \leftarrow U \varphi(\Sigma) V^\top.
\]

Repeated steps push singular values toward a near-flat target. This is the computational heart of Muon: replace a high-condition-number momentum matrix by a direction that retains singular vectors but flattens singular values.

### 3.3 Cost Model

The cost of Newton-Schulz orthogonalization is matrix multiplication. For a matrix \(n \times m\), each step costs roughly quadratic-to-cubic work in the smaller dimension. The original Muon writeup argues that for large language-model batches, the cost is often small relative to the full forward/backward pass. However, FLOPs are not the whole story. Distributed training adds communication and sharding constraints, low precision adds numerical stability questions, and implementation details such as Q/K/V grouping can matter.

## 4. Mathematical Views of Muon

The literature has not converged on a single explanation of Muon. Instead, several complementary views are emerging.

### 4.1 Polar Factor and Spectral Flattening

Given \(M = U\Sigma V^\top\), the polar-factor update \(UV^\top\) keeps the left and right singular directions but removes the singular-value spectrum. If the original update is dominated by a few singular directions, this operation increases the relative influence of weaker directions.

This is the simplest and most important mental model:

- AdamW changes coordinate-wise scales.
- Shampoo changes matrix geometry through accumulated preconditioners.
- Muon changes the spectrum of the instantaneous momentum update.

The Spectral Dynamics and Noise Geometry paper sharpens this view by studying the bias induced by polar-factor updates. It argues that Muon's flat-spectrum bias can help in regimes where many spectral directions need to remain active, but also reports settings where Muon is not universally superior. That regime dependence is central to the survey.

### 4.2 Spectral-Norm Trust Region

The non-Euclidean trust-region view treats orthogonalized gradients as solutions to first-order subproblems constrained by matrix spectral norm. In this framing, Muon is part of a broader family of normalized or norm-constrained gradient methods. The spectral norm is special because the dual norm is the nuclear norm, and the polar factor appears naturally as a steepest-descent direction for matrix-shaped updates.

This view is useful because it makes Muon less mysterious. Orthogonalization is not just an implementation trick; it corresponds to choosing a descent direction under a non-Euclidean matrix norm.

### 4.3 Relationship to Shampoo

The original Muon discussion relates Muon to Shampoo by removing preconditioner accumulation. In the idealized SVD case,

\[
(GG^\top)^{-1/4}G(G^\top G)^{-1/4} = UV^\top
\]

when \(G = U\Sigma V^\top\). This shows why matrix preconditioning and matrix orthogonalization are close. But there are also differences:

- Shampoo accumulates curvature-like statistics; Muon acts on the current momentum matrix.
- Shampoo uses inverse roots or eigendecompositions; Muon uses short Newton-Schulz polynomial iterations.
- Shampoo is a general tensor preconditioner; Muon is a practical hidden-layer matrix optimizer recipe.

### 4.4 Finite Newton-Schulz Versus Exact Polar Muon

Many theoretical papers analyze exact-polar Muon, while practical Muon uses finite polynomial iterations in low precision. This gap is now its own subfield. Relevant questions include:

- How many Newton-Schulz steps are enough?
- What coefficient choices are stable in bfloat16 or fp16?
- Does inexact orthogonalization change convergence guarantees?
- Can Chebyshev-type or matrix-sign iterations improve wall-clock performance?
- Can iteration-free approximations preserve the useful spectral bias?

Papers such as Polar Express, Convergence of Muon with Newton-Schulz, IFNSO, and Chebyshev-type Newton-Schulz acceleration directly target this implementation-theory gap.

### 4.5 Curvature and Directional Sharpness

The curvature-perspective literature studies why Muon may outperform Adam in local geometry. A representative claim is that Muon can achieve a smaller second-order curvature penalty than Adam at comparable update norm, driven by lower normalized directional sharpness. This suggests that Muon's advantage is not merely "taking smaller steps"; it may choose directions that interact more favorably with the local curvature of the training landscape.

This claim is promising but should be treated as context-specific until more independent studies establish when it holds.

## 5. Empirical Evidence

### 5.1 Competitive Small-Scale Tasks

Muon first became visible through competitive training settings such as NanoGPT speedrunning and CIFAR-10 speedrunning. The evidential logic is not just that Muon set records. It is that record-based competitive tasks reduce the chance that an optimizer appears good only because the baseline was undertuned. If AdamW could easily recover the record with better tuning, the benchmark community would have a direct incentive to demonstrate it.

This is not a replacement for controlled experiments, but it is a useful antidote to a long-standing problem in optimizer research: weak baselines.

### 5.2 LLM Scaling

Muon is Scalable for LLM Training reports that Muon can scale beyond small language models when two practical details are handled: weight decay and per-parameter update scale. The paper reports roughly two-times computational efficiency over AdamW under compute-optimal scaling-law experiments and introduces Moonlight MoE models trained with Muon.

Practical Efficiency of Muon for Pretraining shifts attention from sample efficiency to compute-time tradeoffs. Its main contribution is to study Muon on the Pareto frontier over wall-clock cost and data efficiency, with emphasis on large-batch training and muP transfer. This matters because an optimizer with better loss per token can still be unattractive if its per-step overhead destroys wall-clock efficiency.

### 5.3 Very Large Systems: MuonClip and Kimi K2

Kimi K2 is a large MoE technical report that introduces MuonClip, a Muon improvement using QK-clip to address training instability. The report states that K2 was pretrained on 15.5T tokens with zero loss spikes. This is important because it shows Muon-style ideas entering very large-scale model training.

At the same time, Kimi K2 is not only an optimizer paper. Its claims combine model architecture, data, post-training, infrastructure, and optimizer changes. For this survey, MuonClip should be treated as strong systems evidence that Muon-like training can be stabilized at scale, but not as isolated proof that Muon alone explains K2's performance.

### 5.4 Robustness and Transfer

Recent work studies whether Muon changes learned representations, not just training loss. Muon Learns More Robust and Transferable Features than Adam reports that Muon-trained features can be more robust and transferable than Adam or SGD features in the studied image and text settings. It also connects this to logit margins and effective rank.

This direction is valuable because it moves beyond optimizer speed. If Muon changes representation geometry, then its importance is not only computational but statistical. However, the claim needs broader replication across architectures, data distributions, and tuning budgets.

### 5.5 Negative and Regime-Dependent Evidence

The strongest version of the survey must include negative evidence. The workbench includes papers on non-convergence, "not that special" spectral controls, convex Lipschitz failures, and architecture-specific reversals. These papers are not embarrassing exceptions; they are essential for mapping Muon's domain of validity.

Current evidence supports the following cautious statement:

Muon is often competitive and sometimes strongly favorable in hidden-layer matrix-heavy pretraining regimes, especially with large-batch or scale-aware recipes. It is not yet established as a universally superior optimizer across architectures, tasks, fine-tuning regimes, or problem classes.

## 6. Taxonomy of Muon Research

The 2025-2026 literature can be organized into seven clusters.

### 6.1 Core Definition and Scaling

This cluster asks how to make Muon work as a practical optimizer:

- Muon original writeup: definition, Newton-Schulz implementation, parameter grouping, relationship to Shampoo.
- Muon is Scalable for LLM Training: weight decay, update scale, large LLM/MoE scaling.
- Practical Efficiency of Muon for Pretraining: compute-time Pareto frontier, batch scaling, muP transfer.
- Kimi K2 / MuonClip: very large-scale stabilization with QK-clip.

### 6.2 Theory and Geometry

This cluster asks what Muon is optimizing and why it can help:

- A Note on the Convergence of Muon.
- Muon Optimizes Under Spectral Norm Constraints.
- Understanding Gradient Orthogonalization via Non-Euclidean Trust-Region Optimization.
- Preconditioning Benefits of Spectral Orthogonalization in Muon.
- The Spectral Dynamics and Noise Geometry of Muon.
- Why Muon Outperforms Adam: A Curvature Perspective.
- Spectral Scaling Laws of Muon.

### 6.3 Finite Orthogonalization and Matrix-Sign Algorithms

This cluster studies the subroutine inside Muon:

- Polar Express.
- Convergence of Muon with Newton-Schulz.
- Accelerating Newton-Schulz Iteration for Orthogonalization.
- IFNSO: Iteration-Free Newton-Schulz Orthogonalization.
- How Much Orthogonalization Does Muon Need?

### 6.4 Adaptive and Preconditioned Muon

This cluster asks whether Muon should borrow Adam-like adaptivity:

- AdaMuon.
- Muon^2.
- Newton-Muon.
- Adam Improves Muon.
- AdaGrad Meets Muon.
- Mousse and related curvature-aware variants.

The central tension is clear: adaptivity can improve robustness, but too much elementwise scaling may undermine the spectral geometry that makes Muon distinct.

### 6.5 Low-Rank, Fine-Tuning, and Manifold Variants

This cluster extends Muon beyond dense hidden-layer pretraining:

- LoRA-Muon.
- LoRA meets Riemannion.
- Intrinsic Muon.
- NuMuon.
- Can Muon Fine-tune Adam-Pretrained Models?
- Uniform Spectral Growth and Convergence of Muon in LoRA-style matrix factorization.

LoRA-Muon is especially important because it translates Muon's spectral steepest-descent rule to the low-rank setting and argues that learning rates transfer across rank and factor scaling.

### 6.6 Systems, Distributed Training, and Quantization

This cluster asks how to run Muon efficiently:

- Dion and Dion2.
- MuonBP.
- FedMuon variants.
- SignMuon and communication-efficient variants.
- Effective Quantization of Muon Optimizer States.
- MuonQ.
- veScale-FSDP.

The unifying theme is that Muon is not an elementwise optimizer. Matrix orthogonalization complicates sharding, communication, optimizer-state storage, and mixed-precision implementation.

### 6.7 Diagnostics, Applications, and Boundary Papers

This cluster maps where Muon helps or fails:

- Muon Optimizer Accelerates Grokking.
- Muon Outperforms Adam in Tail-End Associative Memory Learning.
- Muon in Vision Transformers.
- When Muon Optimizer Meets Adversarial Training.
- Muon Does Not Converge on Convex Lipschitz Functions.
- Muon is Not That Special.
- Rethinking Muon Beyond Pretraining.

These papers should feed the survey's "boundary conditions" section rather than being treated as secondary.

## 7. Implementation Guidance

A practical Muon implementation should answer the following questions explicitly.

Parameter grouping:

- Which matrices receive Muon?
- Which parameters stay on AdamW?
- Are Q, K, and V optimized separately or as a combined projection?
- Are convolutional parameters flattened?

Orthogonalization:

- How many Newton-Schulz steps are used?
- What polynomial coefficients are used?
- What precision is used for the iteration?
- How are rectangular matrices oriented?

Scaling and regularization:

- Is decoupled weight decay used?
- Is update scale adjusted by parameter shape?
- Is muP or another transfer framework used?
- Are learning rates tuned jointly with AdamW fallback groups?

Systems:

- How are matrix updates sharded?
- Does orthogonalization require cross-device communication?
- Is optimizer state quantized?
- Are failures logged as loss spikes, NaNs, or divergence?

Benchmarking:

- Is AdamW strongly tuned?
- Are wall-clock and token efficiency both reported?
- Are runs seed-averaged?
- Are baselines matched for model size, data, batch size, and training budget?

## 8. Benchmarking Standards

Optimizer research is unusually vulnerable to bad comparisons. A Muon benchmark should avoid the following traps:

- Comparing against an undertuned AdamW baseline.
- Reporting only loss per token while ignoring wall-clock overhead.
- Reporting only wall-clock while ignoring sample efficiency.
- Tuning Muon more carefully than the baseline.
- Changing architecture, normalization, weight decay, batch size, or data order without isolating effects.
- Using small synthetic results to imply large transformer conclusions.
- Treating exact-polar theory as if it directly proves finite-step low-precision Muon behavior.

The best benchmark style is multi-axis: loss per token, wall-clock time, FLOPs, memory, communication, stability, tuning cost, and transfer to nearby scales.

## 9. Threats to Validity

Literature drift: the Muon literature is changing rapidly. Many 2026 papers are recent arXiv preprints with unstable versions, missing code, or no peer-reviewed venue status.

Evidence level: many corpus notes are abstract-level or metadata-level. They are useful for mapping the field, but detailed claims need theorem, algorithm, table, figure, or section locators.

Benchmark drift: model recipes and baseline tuning evolve quickly. A claim that Muon beats AdamW in one setup may become weaker if AdamW is retuned or if the architecture changes.

Implementation drift: "Muon" can mean exact polar Muon, finite Newton-Schulz Muon, Nesterov Muon, Muon with update scaling, Muon with AdamW fallback groups, or a named variant such as MuonClip or MuonQ.

Theory-practice gap: exact spectral-norm or polar-factor theory may not apply cleanly to finite-step, low-precision, sharded, large-scale training.

Selection bias: because Muon is exciting, positive results may appear faster than failed replications. Negative papers should be actively tracked.

## 10. Open Problems

1. Characterize the regime where spectral flattening helps. Is it driven by architecture, data imbalance, hidden-state rank, curvature, batch size, or a combination?
2. Prove results for finite-step Newton-Schulz Muon in low precision, not only exact-polar Muon.
3. Determine whether Adam-like adaptivity and Muon-style spectral geometry can be combined without one erasing the other.
4. Build distributed Muon implementations that are memory optimal, communication efficient, and easy to integrate into existing FSDP/tensor-parallel systems.
5. Understand Muon outside pretraining: fine-tuning, LoRA, RL, continual learning, recommendation, adversarial training, and scientific ML.
6. Standardize Muon benchmarks with tuned AdamW, tuned Shampoo/SOAP where feasible, wall-clock accounting, and seed-averaged results.
7. Convert negative results into design rules: when should one avoid Muon?
8. Build an ablation taxonomy for momentum placement, orthogonalization quality, update scaling, weight decay, QKV grouping, and fallback optimizer groups.

## 11. Conclusion

Muon is best understood as a practical matrix-geometry optimizer: momentum supplies temporal smoothing, Newton-Schulz supplies cheap approximate polar factors, and parameter grouping keeps the method focused on hidden-layer matrices. Its promise comes from combining a simple implementation with a nontrivial geometric bias: flattening the update spectrum while retaining singular directions.

The survey evidence supports a balanced view. Muon has credible empirical wins in competitive small-model tasks and strong reports in LLM pretraining, especially when scaling and weight decay are handled carefully. It has an expanding mathematical foundation through spectral-norm trust regions, spectral dynamics, curvature analysis, and convergence studies. It also has real open risks: architecture dependence, systems complexity, finite-precision approximation, and negative results in some problem classes.

The most useful next step is to convert the current workbench corpus from broad first-pass coverage into deep evidence cards. Each included paper should be upgraded with exact theorem assumptions, algorithm details, benchmark settings, and implementation notes. Only then should the survey move from this formal draft to a publication-grade manuscript with tables, figures, and claim-level citations.

## Appendix A. Representative Paper Map

| Cluster | Representative sources | Role in the survey |
|---|---|---|
| Lineage | Adam, AdamW, Shampoo, SOAP | Establish diagonal adaptivity and matrix preconditioning baselines |
| Muon definition | Keller Jordan Muon writeup | Defines Momentum Orthogonalized by Newton-Schulz and practical parameter grouping |
| Scaling | Muon is Scalable, Practical Efficiency, Kimi K2 | Tests Muon-style training at larger scale and wall-clock regimes |
| Trust-region theory | Gradient Orthogonalization, Spectral Norm Constraints | Interprets Muon as non-Euclidean or spectral-norm steepest descent |
| Spectral dynamics | Spectral Dynamics and Noise Geometry, Spectral Scaling Laws | Studies flat-spectrum bias and singular-value behavior |
| Curvature | Why Muon Outperforms Adam | Studies second-order penalties and directional sharpness |
| Orthogonalization subroutine | Polar Express, IFNSO, Newton-Schulz convergence | Studies the practical approximation replacing exact SVD |
| Adaptivity | AdaMuon, Muon^2, Newton-Muon | Combines Muon with Adam-like or Newton-like preconditioning |
| Low-rank | LoRA-Muon, Riemannion, Intrinsic Muon, NuMuon | Extends Muon to LoRA and matrix manifolds |
| Systems | Dion, MuonBP, FedMuon, MuonQ, veScale-FSDP | Addresses sharding, communication, quantization, and system integration |
| Boundary results | Muon Does Not Converge, Muon is Not That Special, ViT and RL/VLA papers | Maps where Muon may fail or require modification |

## Appendix B. Selected Bibliography

- Keller Jordan. [Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/), 2024.
- Diederik P. Kingma and Jimmy Ba. [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980), 2014/2015.
- Ilya Loshchilov and Frank Hutter. [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101), 2017/2019.
- Vineet Gupta, Tomer Koren, and Yoram Singer. [Shampoo: Preconditioned Stochastic Tensor Optimization](https://arxiv.org/abs/1802.09568), 2018.
- Nikhil Vyas et al. [SOAP: Improving and Stabilizing Shampoo using Adam](https://arxiv.org/abs/2409.11321), 2024/2025.
- Jingyuan Liu et al. [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982), 2025.
- Dmitry Kovalev. [Understanding Gradient Orthogonalization for Deep Learning via Non-Euclidean Trust-Region Optimization](https://arxiv.org/abs/2503.12645), 2025.
- Essential AI et al. [Practical Efficiency of Muon for Pretraining](https://arxiv.org/abs/2505.02222), 2025.
- Noah Amsel et al. [The Polar Express: Optimal Matrix Sign Methods and Their Application to the Muon Algorithm](https://arxiv.org/abs/2505.16932), 2025.
- Chongjie Si, Debing Zhang, and Wei Shen. [AdaMuon: Adaptive Muon Optimizer](https://arxiv.org/abs/2507.11005), 2025.
- Aman Gupta et al. [Effective Quantization of Muon Optimizer States](https://arxiv.org/abs/2509.23106), 2025.
- Ahmed Khaled et al. [MuonBP: Faster Muon via Block-Periodic Orthogonalization](https://arxiv.org/abs/2510.16981), 2025.
- Kimi Team. [Kimi K2: Open Agentic Intelligence](https://arxiv.org/abs/2507.20534), 2025/2026.
- Jiaxiang Li and Mingyi Hong. [A Note on the Convergence of Muon](https://arxiv.org/abs/2502.02900), 2025.
- Naoki Sato, Hiroki Naganuma, and Hideaki Iiduka. [Convergence Bound and Critical Batch Size of Muon Optimizer](https://arxiv.org/abs/2507.01598), 2025.
- Zhehang Du and Weijie Su. [The Newton-Muon Optimizer](https://arxiv.org/abs/2604.01472), 2026.
- Ziyue Liu et al. [Muon^2: Boosting Muon via Adaptive Second-Moment Preconditioning](https://arxiv.org/abs/2604.09967), 2026.
- Yupeng Su et al. [MuonQ: Enhancing Low-Bit Muon Quantization via Directional Fidelity Optimization](https://arxiv.org/abs/2605.11396), 2026.
- Jiacheng Li et al. [MONA: Muon Optimizer with Nesterov Acceleration for Scalable Language Model Training](https://arxiv.org/abs/2605.26842), 2026.
- Franz Louis Cesista, Katherine Crowson, Cedric Simal, and Stella Biderman. [LoRA-Muon: Spectral Steepest Descent on the Low-Rank Manifold](https://arxiv.org/abs/2606.12921), 2026.
- Pierfrancesco Beneventano, Mahmoud Abdelmoneum, and Tomaso Poggio. [The Spectral Dynamics and Noise Geometry of Muon](https://arxiv.org/abs/2606.08388), 2026.
- Shuche Wang et al. [Why Muon Outperforms Adam: A Curvature Perspective](https://arxiv.org/abs/2606.04662), 2026.
- Tianyu Ruan et al. [Muon Learns More Robust and Transferable Features than Adam](https://arxiv.org/abs/2606.09658), 2026.
