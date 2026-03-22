---
title: "Asimov 1985 - The Grand Tour"
date: 2026-03-22
tags: [grand-tour, visualization, grassmannian, high-dimensional]
doi: "10.1137/0906011"
---

## Summary

Introduces the grand tour — a method for viewing multivariate data via an animation of orthogonal projections onto a sequence of 2D subspaces. The sequence is chosen to be dense on the Grassmannian $\text{Gr}(2, d)$, meaning it comes arbitrarily close to every possible 2D view. Analogous to walking around a sculpture to view it from all angles.

## Key Findings

- The grand tour creates a smooth path through the Grassmannian, producing a continuous animation of 2D projections
- The path must be dense — eventually approaching every possible view
- Implemented in Dataviewer software (Buja, Asimov, Hurley 1986)

## Relevance to This Work

**The grand tour is the exploration metaphor our viewer implements.** Our interactive viewer lets users navigate the Grassmannian searching for the privileged projection — this is exactly a user-directed grand tour, but with a goal (find the hidden form) rather than open-ended exploration.

- Grand tour = exhaustive search of $\text{Gr}(2, d)$ → our viewer = clue-guided search of $\text{Gr}(2, d)$
- Their dense path guarantees every view is eventually seen → our principal angle sliders guarantee the privileged view is reachable
- The sculpture analogy maps directly: a latent anamorph IS a high-dimensional sculpture that looks different from every angle, with one (or a few) "correct" viewpoints

The connection to Cook et al. 1995 (guided tour = PP-steered grand tour) is also relevant: our clue channel is the analog of a PP index, steering the user toward the interesting view.

## Questions & Follow-ups

- Should we explicitly cite the grand tour as a precedent for our viewer interaction?
- Can we frame our clue-guided exploration as a "semantic guided tour" — a new member of the tour family?
