---
title: "Park et al. 2024 - The Linear Representation Hypothesis"
date: 2026-03-22
tags: [linear-representation, geometry, LLM, theory, directions]
doi: "arXiv:2311.03658"
---

## Summary

Provides formal grounding for the "linear representation hypothesis" — that high-level concepts are encoded as linear directions in representation space. Uses counterfactual formalism to give two formalizations (output word space and input context space), proves these connect to linear probing and model steering respectively, and identifies a non-Euclidean inner product that makes geometric operations meaningful.

## Key Findings

- The linear representation hypothesis can be formalized via counterfactual interventions
- Linear probing and steering are provably connected to the two formalizations
- A non-Euclidean inner product (derived from the model's structure) makes cosine similarity and projection geometrically meaningful
- This means naively using Euclidean cosine similarity on representations may be misleading

## Relevance to This Work

**Provides theoretical justification for concept-as-direction.** If we build Type II anamorphs using concept directions as privileged subspaces, this paper tells us the mathematical conditions under which that's well-defined.

The non-Euclidean inner product finding is important: if the "correct" geometry of the representation space is non-Euclidean, then our observer maps should use the correct metric, not just Euclidean projection. This could affect:
- How we define the alignment metric between subspaces
- Whether linear projection (Type I) is the right observer map for learned embedding spaces
- Whether we need metric-aware observer maps for Type II anamorphs

## Questions & Follow-ups

- Does the non-Euclidean structure matter for our constructed (not learned) point sets?
- For Type II anamorphs in actual model activations, should we use the model-specific inner product?
