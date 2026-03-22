---
title: "Edelman, Arias & Smith 1998 - Geometry of Algorithms with Orthogonality Constraints"
date: 2026-03-22
tags: [grassmannian, manifold, optimization, geometry, foundational]
doi: "10.1137/S0895479895290954"
---

## Summary

Develops Newton and conjugate gradient algorithms on the Grassmann and Stiefel manifolds. Provides the foundational geometric framework — geodesics, exponential map, distances, parallel transport — for these manifolds. ~2,880 citations. The standard reference for Grassmannian geometry in numerical linear algebra and ML.

## Key Findings

- The Grassmannian $\text{Gr}(k, n)$ is a smooth Riemannian manifold of dimension $k(n-k)$
- Geodesics, distances, and the exponential map have closed-form expressions via SVD
- Newton's method and conjugate gradient can be formulated directly on the manifold
- Provides the mathematical machinery for optimization over subspaces

## Relevance to This Work

**This is our primary reference for the observer parameter space.** Our observer maps are parameterized by points on $\text{Gr}(2, d)$:

- The Grassmannian dimension $k(n-k) = 2(d-2)$ gives us the "search space size" — for $d = 64$, it's 124-dimensional
- Geodesics on the Grassmannian = smooth paths between projections → our viewer interpolation uses these
- The exponential map provides the right way to "move" in projection space → our principal angle sliders implement exactly this
- Distances on the Grassmannian (via principal angles) define our alignment metric

This paper also supports the construction side: optimizing the anamorph's properties (maximize legibility contrast, minimize decoy confusion) is an optimization problem on the Grassmannian.

## Questions & Follow-ups

- Should we use Grassmannian geodesic interpolation (proper) instead of our current "lerp and re-orthogonalize" approach in the viewer?
- Can we formulate anamorph construction as an optimization problem on $\text{Gr}(2, d)^m$ (product of Grassmannians for $m$ embedded views)?
