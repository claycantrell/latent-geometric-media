---
title: "Bjorck & Golub 1973 - Principal Angles Between Subspaces"
date: 2026-03-22
tags: [principal-angles, subspaces, SVD, foundational, alignment]
doi: "10.2307/2005662"
---

## Summary

The foundational paper on numerically computing principal angles and principal vectors between subspaces. Develops algorithms based on QR factorization and SVD. Establishes the connection between principal angles and canonical correlations in statistics.

## Key Findings

- Principal angles $\theta_1, \dots, \theta_k$ between two $k$-dimensional subspaces are computed via SVD of $U_1^\top U_2$
- $\cos \theta_i$ = $i$-th singular value of the cross-product matrix
- These angles are the fundamental invariants of the relative position of two subspaces
- Any rotation-invariant distance between subspaces must be a function of the principal angles

## Relevance to This Work

**Our alignment metric is directly based on principal angles.** The prototype's alignment function computes $\|U^\top V\|_F / \sqrt{k}$, which is the root-mean-square cosine of the principal angles. This paper:

- Provides the algorithm we use (SVD of the cross-product matrix)
- Justifies our alignment metric as the natural distance measure
- Our principal angle slider decomposition in the web viewer is a direct application: the two sliders control the two principal angles independently
- The principal vectors define the orthogonal rotation planes we use for independent navigation

## Questions & Follow-ups

- Should we cite Bjorck & Golub explicitly when defining the alignment metric in Section III?
- Yes — this is the canonical reference for the computation we use
