---
title: "Diaconis & Freedman 1984 - Asymptotics of Graphical Projection Pursuit"
date: 2026-03-22
tags: [projection-pursuit, theory, gaussian, high-dimensional, foundational]
doi: "10.1214/aos/1176346703"
---

## Summary

Proves that under suitable conditions, most low-dimensional projections of high-dimensional data are approximately Gaussian. This is the theoretical foundation for why projection pursuit works — and for why our latent anamorphs can hide structure.

## Key Findings

- For a random vector in $\mathbb{R}^d$ with independent coordinates and finite moments, almost all one-dimensional projections are approximately normal as $d \to \infty$
- This is a concentration-of-measure phenomenon: the space of "interesting" projections has vanishingly small measure on the Grassmannian

## Relevance to This Work

**This result directly supports our Condition C2 (generic illegibility).** If most projections of a high-dimensional point cloud look Gaussian (i.e., unstructured), then a designed form that appears only under a specific projection is naturally hidden — not by encryption, but by the geometry of high-dimensional space itself.

- Provides the theoretical justification for why $\mathbb{E}_{\theta \sim \text{Uniform}(\Theta)}[L(f_\theta(X))] \leq \tau_0$ — generic projections are unstructured by default
- The "needle in a haystack" quality of finding the privileged projection is a consequence of this theorem, not an artifact of our construction
- Quantifies recovery difficulty $\rho$: the fraction of the Grassmannian that reveals structure is vanishingly small

## Questions & Follow-ups

- What are the precise conditions under which this holds? Our constructed points are not independent (they have embedded structure) — does the result still apply to the noise components?
- Can we cite specific convergence rates to make our $\tau_0$ bound concrete?
