---
title: "Debnath et al. 2025 - RASP: 3D Anamorphic Art via Differentiable Rendering"
date: 2026-03-22
tags: [anamorphosis, 3D, multi-view, differentiable-rendering, CVPR]
doi: "arXiv:2504.02465"
---

## Summary

A differentiable-rendering framework for arranging 3D objects within a bounded volume so that their shadows/silhouettes create meaningful images from multiple privileged viewpoints simultaneously. CVPR 2025.

## Relevance to This Work

**Most recent computational anamorphosis work, and the closest to supporting multiple views.** But still operates in physical 3D space with shadow/silhouette projections:

- They achieve multi-view anamorphosis (different images from different viewpoints) → our polysemantic capacity supports this natively
- They use differentiable rendering for optimization → we could use differentiable projection for construction optimization
- Still 3D Euclidean, still physical optics → no high-dimensional latent space, no semantic keying, no Grassmannian
- No concept of clue channels, decoy views, or recovery difficulty

This paper shows the field is moving toward multi-view and computational optimization of anamorphic objects. We extend this direction into abstract high-dimensional spaces.
