# Muon Research Pipeline - Phase 1

Search date: 2026-06-14. The local shell context was America/Chicago and displayed 2026-06-13 during execution; this registry uses the project cutoff requested as current on 2026-06-14.

## Phase 1 Scope

This phase does not write survey prose. It establishes the working pipeline, first registry, first evidence graph, and first paper-note skeletons for two lines of work:

- Optimizer lineage: SGD, Momentum SGD, AdaGrad, RMSProp, Adam, AdamW, Shampoo, SOAP, Muon.
- Muon survey: Muon optimizer papers, theory, systems, variants, official pages, and code through the search date.

## Local Readiness Check

- Project skills read: muon-web-research, muon-paper-reading, muon-math-deep-dive, muon-knowledge-graph.
- Workbench docs read: docs/research-workbench.md and data/optimizer-graph/README.md.
- Local graph seed existed and was replaced by an evidence-backed first version.
- Python research packages exist under .tools/python-packages and bundled runtime.
- Real .env is ignored and was not read or printed.
- Git executable was not found in PATH or common install locations; commit/push requires a fallback path.

## Search Sources

- arXiv API and arXiv abstract pages.
- Semantic Scholar public Graph API.
- OpenAlex public Works API.
- OpenReview for workshop/forum Muon entries.
- Official author pages and official code repositories when surfaced by papers/pages.
- Targeted web search for optimizer lineage and Muon variants.

Semantic Scholar public API returned HTTP 429 on some queries; successful queries are represented in the registry evidence notes, and rate-limit risk is recorded as a boundary.

## Exact Query Families

- arXiv: `ti:Muon AND (cat:cs.LG OR cat:stat.ML OR cat:math.OC OR cat:cs.AI OR cat:cs.CL)`.
- arXiv: `abs:"Muon optimizer" AND (cat:cs.LG OR cat:stat.ML OR cat:math.OC OR cat:cs.AI OR cat:cs.CL)`.
- arXiv: `abs:"matrix orthogonalization" AND abs:Muon`.
- arXiv: `abs:"Newton-Schulz" AND abs:Muon`.
- Semantic Scholar: `Muon optimizer`, `Muon optimizer AdamW orthogonalization`, `Muon optimizer LLM training`.
- OpenAlex: `Muon orthogonalization optimizer`, `Muon AdamW optimizer`, `SOAP Shampoo Adam optimizer`, `Shampoo optimizer AdamW`.
- Web search: exact titles for Muon scalable, AdaMuon, Effective Quantization, FedMuon, Delving into Muon, MONA, LoRA-Muon, SOAP, Shampoo, AdamW, Adam, and Keller Jordan Muon.

## Inclusion Criteria

Included records must satisfy at least one condition:

- Introduces or historically anchors a named optimizer in the SGD-to-Muon lineage.
- Directly introduces, analyzes, implements, scales, quantizes, distributes, or benchmarks Muon or a Muon variant.
- Provides official source code or author documentation for Muon or a Muon-family method.
- Provides theory or systems context needed to interpret Muon's matrix orthogonalization.

## Exclusion Criteria

Excluded or deferred records include:

- Physics muon/collider/spectrometer papers surfaced by keyword collision.
- Papers that merely mention Muon without optimizer relevance.
- Secondary summaries without primary-source support.
- Records whose abstract/title is too ambiguous for graph promotion before full reading.

## Pipeline

1. Discovery: run dated searches across arXiv, Semantic Scholar, OpenAlex, OpenReview, official pages, and official repos.
2. Deduplication: use arXiv ID, DOI, OpenAlex ID, normalized title, and author/year.
3. Triage: assign inclusion_status (`included`, `candidate`, `excluded`) and relevance (`core`, `adjacent`, `background`, `excluded`).
4. Registry: write `data/paper-registry.csv` with source, query, inclusion, and evidence fields.
5. Reading notes: create one Markdown note per core paper in `docs/paper-notes/` using the project Muon note template.
6. Graph update: add source rows first, then paper/method/concept nodes, then evidence-backed typed edges.
7. Validation: render with `scripts/render_optimizer_graph.py` and inspect generated Mermaid/HTML for obvious disconnected or mislabeled records.
8. Next phase: deepen notes with PDF section/page locators, then draft survey sections only after graph and registry stabilize.

## First-Pass Priority Buckets

- Lineage anchors: Robbins-Monro, Polyak heavy-ball, AdaGrad, RMSProp, Adam, AdamW, Shampoo, SOAP.
- Muon body: Keller Jordan Muon page and modded-nanogpt, Old Optimizer/New Norm, Modular Duality.
- 2025 Muon core: convergence note, scalable Muon, non-Euclidean trust-region analysis, practical efficiency, Polar Express, critical batch, AdaMuon, quantized Muon, MuonBP.
- 2026 Muon core: spectral preconditioning benefits, Newton-Schulz convergence, Delving into Muon, Newton-Muon, Muon^2, MuonQ, MONA, LoRA-Muon.

## Known Boundaries

- The registry is a first-pass search artifact, not a claim of final completeness.
- arXiv title searches are high-recall and include noisy physics records; these are marked excluded when obvious.
- Some 2026 papers are very recent and may have unstable versions, code links, or conference status after the search date.
- OpenAlex can duplicate arXiv records and miss recent preprints; IDs are filled only when verified in the first pass.
