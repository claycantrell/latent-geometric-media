---
title: "Bolukbasi et al. 2016 - Debiasing Word Embeddings"
date: 2026-03-22
tags: [word-embeddings, semantic-directions, bias, linear-subspace, foundational]
doi: "arXiv:1607.06520"
---

## Summary

Demonstrates that gender bias in word2vec embeddings is captured by a single linear direction (the "gender direction") in the embedding space. Proposes projection-based debiasing by projecting embeddings onto the subspace orthogonal to the bias direction. ~3,456 citations. NeurIPS 2016.

## Key Findings

- Gender bias = a linear direction in word2vec space
- Gender-neutral words are linearly separable from gender-definitional words along this axis
- Projecting onto the orthogonal complement removes bias while preserving semantic utility
- Extends to other bias types (race, religion)

## Relevance to This Work

**Early and influential demonstration that semantic concepts correspond to linear directions in learned embedding spaces.** This is a precursor to TCAV, RepE, and the linear representation hypothesis:

- "Gender direction" = a concept direction → our Type II anamorph uses concept directions as privileged subspaces
- Projection onto / orthogonal to a concept direction changes what's visible → our observer maps project onto concept-defined subspaces to reveal or hide structure
- Their debiasing removes information along a direction → our construction embeds information along specific directions

This paper helped establish the principle that makes Type II anamorphs possible: if concepts live in linear subspaces of embedding spaces, then designed objects can use those subspaces as privileged views.
