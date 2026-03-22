---
title: "Zou et al. 2023 - Representation Engineering"
date: 2026-03-22
tags: [representation-engineering, steering-vectors, LLM, interpretability, directions]
doi: "arXiv:2310.01405"
---

## Summary

Introduces "representation engineering" (RepE), a top-down approach to AI transparency inspired by cognitive neuroscience. Emphasizes population-level representations (not individual neurons) and geometric/topological structure in latent space. Two components: Representation Reading (extracting a linear direction capturing a concept) and Representation Steering (adding/subtracting that direction during inference to control behavior).

## Key Findings

- High-level cognitive properties (honesty, harmlessness, power-seeking) are encoded as linear directions in LLM activation space
- These directions can be extracted by contrasting activations on concept-positive vs. concept-negative prompts
- Adding/subtracting the direction during forward passes steers model behavior (e.g., +30pp on TruthfulQA)
- Grounded in "Hopfieldian view" of neural computation — population codes and geometric structure

## Relevance to This Work

**RepE validates the "concepts as directions" paradigm at scale in modern LLMs.** This supports our Type II anamorph design:

- If LLM representations have linear concept structure, then designed objects in those spaces can use concept directions as privileged projection bases
- Steering vectors show that directions are not just discoverable but *actionable* — you can move along them to change behavior → we move along them to change what's visible
- The population-level emphasis aligns with our approach: we design structure at the level of point clouds, not individual points

Also relevant to the embedding microscope application (Section VI.2): RepE's framework for reading and steering representations is exactly the kind of tool our concept-guided projection system would complement.

## Questions & Follow-ups

- Could a latent anamorph be embedded in an LLM's activation space? The "hidden form" would be visible only along a concept direction
- How does the linearity assumption hold up? If concept directions are approximately but not perfectly linear, how does this affect anamorph recovery?
