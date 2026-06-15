# Muon Research Workbench

This repository is a local Codex workspace for learning, reading, testing, and mapping the Muon optimizer and related optimization research.

## Contents

- `.codex/skills/`: project-local Codex skills for PDF reading, paper search, source capture, browser verification, paper analysis, notebook scaffolding, evidence audit, memory, and handoff workflows.
- `external-frameworks/`: external research frameworks tracked as Git submodules.
  - `paper-qa`: scientific paper question answering and retrieval workflows.
  - `gpt-researcher`: autonomous web research framework.
- `data/optimizer-graph/`: lightweight CSV graph for optimizer lineage, Muon papers, concepts, and evidence.
- `docs/artifacts/`: generated, shareable HTML/PDF artifacts, including the interactive optimizer graph and lecture output.
- `scripts/render_optimizer_graph.py`: renders the graph to Mermaid and an interactive HTML view.
- `requirements/research-requirements.lock`: Python package snapshot for the local research tooling.
- `.env.example`: optional API key template. Real `.env` stays local and ignored.

## After Cloning

```powershell
git submodule update --init --recursive
```

Use `.env.example` as a template for local secrets:

```powershell
Copy-Item .env.example .env
```

Never commit real API keys.

## Local Runtime Notes

The local working environment uses `.tools/python-packages`, which is intentionally ignored. Recreate it from `requirements/research-requirements.lock` when needed.

The Codex in-app Browser is preferred for rendered webpage checks. The Playwright CLI skill is kept, but it needs a complete Node/npm/npx Playwright setup before terminal-driven browser automation is available.

Render the seed optimizer graph with:

```powershell
& 'C:\Users\PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\render_optimizer_graph.py
```

Current shareable outputs:

- `docs/artifacts/optimizer-graph.html`
- `docs/artifacts/optimizer-graph.mmd`
- `docs/artifacts/sgd_to_muon_lecture_01.html`
- `docs/artifacts/sgd_to_muon_lecture_01.pdf`
