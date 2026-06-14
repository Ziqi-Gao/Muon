---
name: muon-math-deep-dive
description: Perform deep mathematical reasoning for Muon and optimizer theory, including update equations, Newton-Schulz orthogonalization, matrix norms, spectral analysis, convergence bounds, momentum, weight decay, adaptive variants, and critical batch size. Use when Codex needs derivations, proof sketches, sanity checks, or math-first comparisons across optimizers.
---

# Muon Math Deep Dive

Use this skill when the task is to understand, derive, compare, or stress-test optimizer mathematics.

## Reasoning Protocol

1. State the exact object being analyzed: parameter matrix, gradient, momentum buffer, preconditioner, orthogonalized update, loss assumptions, and norm.
2. Write the update equations before interpreting them.
3. Track dimensions and invariances explicitly.
4. Separate:
   - established facts from cited sources,
   - derivations made in the current analysis,
   - conjectures or intuition.
5. Check limiting cases: scalar parameter, diagonal matrix, rank-deficient gradient, zero momentum, large/small batch, and no weight decay.
6. Compare against baseline optimizers with matched notation: SGD, momentum SGD, RMSProp/Adam, AdamW, Shampoo/SOAP, and Muon variants.
7. End with implications for the survey and graph: which relation or claim should be recorded, and with what confidence.

## Useful Lenses

- Geometry: update direction, norm constraints, spectral flattening, rank effects.
- Optimization: descent direction, smoothness assumptions, stochastic noise, convergence rate.
- Systems: memory state, communication cost, distributed implementation, quantization.
- Empirical scaling: batch size, model size, architecture coverage, training efficiency.

## Output Discipline

- Use equations and short prose, not vague analogy.
- Mark any unstated assumption before using it.
- If a theorem is being summarized, preserve the theorem's assumptions and conclusion shape.
