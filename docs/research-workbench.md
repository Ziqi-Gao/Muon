# Research Workbench Inventory

## Installed Skills

Project-local skills live under `.codex/skills/`.

- `academic-research-suite`
- `beautifulsoup-html-parse`
- `browser-page-verification`
- `conf-search`
- `daily-papers`
- `handoff-manager`
- `jupyter-notebook`
- `paper-analyze`
- `paper-reading-note`
- `paper-search`
- `pdf`
- `playwright`
- `research-pilot-memory`
- `risk-and-evidence-audit`
- `semantic-scholar`
- `web-source-capture`
- `muon-web-research`
- `muon-paper-reading`
- `muon-math-deep-dive`
- `muon-knowledge-graph`

## External Frameworks

These are tracked as submodules, not vendored source copies:

- `external-frameworks/paper-qa`: `https://github.com/Future-House/paper-qa.git`
- `external-frameworks/gpt-researcher`: `https://github.com/assafelovic/gpt-researcher.git`

## Added Research Libraries

- `pyalex`: OpenAlex metadata, semantic search, and content discovery.
- `networkx`: graph construction and analysis.
- `pyvis`: interactive HTML graph rendering.
- `rdflib`: optional RDF graph export path.
- `bibtexparser`: BibTeX parsing/export.

## API Keys

Optional keys are documented in `.env.example`.

- `FIRECRAWL_API_KEY`: web source capture fallback.
- `SEMANTIC_SCHOLAR_API_KEY`: avoids public Semantic Scholar rate limits.
- `OPENALEX_API_KEY`: required by OpenAlex for normal metadata searches.
- `OPENAI_API_KEY`: PaperQA and GPT Researcher LLM calls.
- `TAVILY_API_KEY`: GPT Researcher search backend.
- `CROSSREF_API_KEY`: optional paper metadata.

## Verified Local Capabilities

- Skill metadata validates with the Codex skill validator.
- PDF generation, text extraction, and PyMuPDF rendering work with project-local packages.
- Jupyter notebook scaffolding works.
- arXiv access works through Python/httpx.
- PaperQA and GPT Researcher import successfully from the project-local package set.
- PyAlex, NetworkX, PyVis, RDFLib, and BibTeXParser import successfully.
- The seed optimizer graph renders to Mermaid and interactive HTML.

## Known Boundaries

- Real `.env` is ignored and must stay local.
- `.tools/` is ignored; use the lock file in `requirements/` for reproducibility.
- Semantic Scholar public API can return rate limits without `SEMANTIC_SCHOLAR_API_KEY`.
- OpenAlex requires `OPENALEX_API_KEY` for normal metadata searches.
- Playwright CLI needs a complete Node/npm/npx setup; use the Codex Browser plugin first.
