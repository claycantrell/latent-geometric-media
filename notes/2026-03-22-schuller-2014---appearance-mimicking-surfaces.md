---
title: "Schuller et al. 2014 - Appearance-Mimicking Surfaces"
date: 2026-03-22
tags: [anamorphosis, computational, 3D, optimization, SIGGRAPH]
doi: "10.1145/2661229.2661267"
---

## Summary

A unified optimization framework for creating surfaces that depict target shapes from prescribed viewpoints (generalizing bas-reliefs). Finds a globally optimal surface with per-vertex depth bounds. Published at SIGGRAPH Asia 2014.

## Relevance to This Work

This is the closest computational precedent in 3D — it solves the inverse problem of viewpoint-dependent appearance. But it operates on physical 3D surfaces, not high-dimensional point clouds:

- They optimize a surface to look like a target from one viewpoint → we construct a point cloud to reveal a form under one projection
- They work in $\mathbb{R}^3$ with perspective projection → we work in $\mathbb{R}^d$ with orthogonal projection onto $\text{Gr}(2, d)$
- They don't support multiple designed views or decoys
- No concept of polysemy or clue-guided recovery
