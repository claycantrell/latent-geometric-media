---
title: "Johnson & Lindenstrauss 1984 - JL Lemma"
date: 2026-03-22
tags: [random-projection, dimensionality-reduction, distance-preservation, foundational]
doi: "Contemporary Mathematics Vol. 26"
---

## Summary

Establishes the Johnson-Lindenstrauss lemma: any $n$ points in high-dimensional Euclidean space can be embedded into $O(\log n / \epsilon^2)$ dimensions while preserving all pairwise distances within a factor of $(1 \pm \epsilon)$. The embedding is a random orthogonal projection.

## Key Findings

- Random projections approximately preserve pairwise distances
- The target dimension depends only on $\log n$ (number of points), not on the original dimension
- The projection can be a random Gaussian matrix (later simplified by Dasgupta & Gupta 2003, Achlioptas 2003)

## Relevance to This Work

**Supports the theoretical foundation of our construction in two ways:**

1. **Generic illegibility (C2):** Random projections compress structure — a random 2D projection of our $d$-dimensional point cloud maps all points into a small region where distances are approximately preserved but designed spatial structure (text, shapes) is destroyed. This is why generic views look like blobs.

2. **Noise design:** The JL lemma tells us how much noise we can add in ambient dimensions without destroying the signal in the privileged subspace. If pairwise distances are preserved up to $(1 \pm \epsilon)$ under random projection, then the noise components in non-signal dimensions contribute bounded distortion.

Not directly cited for the construction, but foundational context for why high-dimensional point clouds are "safe" hiding places for designed structure.
