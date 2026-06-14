# Framework Search Findings

Search date: 2026-06-13.

## Directly Added

- `pyalex`: OpenAlex client for scholarly metadata, citation expansion, semantic search, and PDF/TEI discovery where available. OpenAlex requires an API key for normal use as of 2026-02-13.
- `networkx`: local graph construction, validation, and analysis.
- `pyvis`: interactive HTML graph rendering from NetworkX graphs.
- `rdflib`: optional RDF export path if the graph later needs semantic-web interoperability.
- `bibtexparser`: simple BibTeX import/export support alongside existing `pybtex`.

## Already Present

- `paper-qa`: retrieval-augmented question answering over scientific papers.
- `gpt-researcher`: autonomous web research framework.
- `arxiv`, `semanticscholar`, PDF extraction/rendering libraries, and project-local paper reading skills.

## Useful But Not Added Yet

- AutoSurvey: strong public automated survey generation baseline, but it expects a large local database and GPU-oriented embedding workflow.
- ARISE: useful agentic survey-writing architecture and rubric idea, but early/small repository and better treated as design inspiration first.
- LiRA and SurveyForge: current literature-review generation papers worth tracking, but no mature drop-in local framework was found during this pass.
- LinkML: good candidate if the knowledge graph schema becomes large and needs generated validators.
- Kuzu: useful embedded graph database if CSV/NetworkX becomes too small, but unnecessary for the first graph iteration.
- SemOpenAlex: too heavy for this project stage; full RDF loading is designed for infrastructure-scale hardware.

## Project Decision

No mature ready-made Codex skill was found for "Muon optimizer survey plus optimizer-history knowledge graph." The project therefore keeps general research skills and adds four project-specific Muon skills:

- `muon-web-research`
- `muon-paper-reading`
- `muon-math-deep-dive`
- `muon-knowledge-graph`

The first practical graph backend is CSV + NetworkX + PyVis, because it is transparent, easy to version, and enough for a hand-curated research graph.

## Sources Checked

- PyAlex: https://github.com/J535D165/pyalex
- NetworkX: https://networkx.org/documentation/stable/
- PyVis: https://pyvis.readthedocs.io/en/latest/
- AutoSurvey: https://github.com/AutoSurveys/AutoSurvey
- ARISE: https://github.com/ziwang11112/ARISE
- PaperQA: https://arxiv.org/abs/2312.07559
- Muon is Scalable for LLM Training: https://arxiv.org/abs/2502.16982
- Convergence Bound and Critical Batch Size of Muon Optimizer: https://arxiv.org/abs/2507.01598
- AdaMuon: https://arxiv.org/abs/2507.11005
- Effective Quantization of Muon Optimizer States: https://arxiv.org/abs/2509.23106
- FedMuon: https://arxiv.org/abs/2510.27403
- Delving into Muon and Beyond: https://arxiv.org/abs/2602.04669
