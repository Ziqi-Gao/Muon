---
name: handoff-manager
description: Long-running research handoff skill for Muon and optimization learning. Use when Codex finishes a substantial web research, paper reading, math derivation, experiment, framework setup, knowledge graph, or source audit session and needs to preserve state for the next session.
---

# Handoff Manager

Adapted from `mattpocock/skills` handoff pattern and long-running research workflows.

## Procedure

1. Review what changed in this session.
2. Use `templates/session-handoff.md` if present; otherwise write a concise markdown handoff.
3. Write the handoff under `docs/handoffs/YYYY-MM-DD-short-topic.md`.
4. Include files updated, sources checked, papers read, experiments run, knowledge graph changes, open unknowns, and exact next actions.
5. Keep it short enough that the next session can read it first.

## Rule

If a decision matters later, write it to a file. Do not leave it only in chat history.
