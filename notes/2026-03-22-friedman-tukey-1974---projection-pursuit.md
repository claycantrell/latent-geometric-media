---
title: "Friedman & Tukey 1974 - Projection Pursuit"
date: 2026-03-22
tags: [projection-pursuit, high-dimensional, visualization, foundational]
doi: "10.1109/T-C.1974.224051"
---

## Summary

Coined the term "projection pursuit." Presents an algorithm to find one- and two-dimensional linear projections of multivariate data that are "relatively highly revealing." The key idea: define a numerical index measuring how "interesting" a projection is (amount of structure/density variation), then optimize over projection parameters to maximize that index.

## Key Findings

- Most projections of high-dimensional data are uninteresting (approximately Gaussian — later proved formally by Diaconis & Freedman 1984)
- "Interesting" projections are those departing from normality — containing clusters, outliers, nonlinear structure
- The method is one of very few that bypasses the curse of dimensionality, ignoring noisy/information-poor variables

## Methodology

- Assign a numerical "projection index" to every 1D or 2D projection
- Maximize this index via numerical optimization over projection parameters
- The index captures data density variation in the projected view

## Relevance to This Work

**This is our closest classical precedent, and also our sharpest contrast.** Friedman & Tukey's framework *searches* for interesting structure that already exists in data. Our latent anamorphs *design* structure into point sets so that it appears only under privileged projections. The relationship is:

- They define "interesting projections" as departures from Gaussianity → we define "privileged projections" as those revealing designed legible forms
- Their projection index measures how much structure exists → our legibility function $L$ measures how coherent the designed form is
- Their optimization finds the best view of existing data → our construction embeds forms that are invisible from most views
- They search the Grassmannian for signal → we place signal at specific points on the Grassmannian

The inversion is the key contribution: from *finding* to *designing* structure in projection space.

## Questions & Follow-ups

- How does their projection index relate to our legibility function $L$? Could we use a PP index as one instantiation of $L$?
- Their concept of "interestingness" could inform our notion of "decoy coherence" — a decoy view should score high on a PP index but resolve to the wrong form
