# Search Queue

## Status Key
- `[ ]` — Not started
- `[~]` — Found candidate, not yet downloaded/read
- `[x]` — Done — paper found, noted

---

## P0 — Must Have Before Drafting

### Literature positioning (establish novelty)

**Anamorphic art (closest art precedent — all in 3D physical space, none in high-d latent space):**
- `[~]` **Di Paola et al. 2015** — "Anamorphic Projection: Analogical/Digital Algorithms" (Nexus Network Journal). DOI: 10.1007/s00004-014-0225-5
- `[~]` **Bermano/Pratt et al. 2023** — "Bending the Light: Next Generation Anamorphic Sculptures" (Computers & Graphics / SIGGRAPH Asia). DOI: 10.1016/j.cag.2023.05.023
- `[~]` **Araujo 2020** — "Anamorphosis Reformed: From Optical Illusions to Immersive Perspectives" (Springer Handbook). DOI: 10.1007/978-3-319-57072-3_101. Comprehensive survey tracing Renaissance → modern.
- `[~]` **Schuller et al. 2014** — "Appearance-Mimicking Surfaces" (SIGGRAPH Asia). DOI: 10.1145/2661229.2661267. Inverse problem of viewpoint-dependent appearance — related framing.
- `[~]` **Debnath et al. 2025** — "RASP: Revisiting 3D Anamorphic Art for Shadow-Guided Packing" (CVPR 2025). arXiv: 2504.02465. Multi-view anamorphic via differentiable rendering — most recent.

**Projection pursuit (they find structure, we design it):**
- `[~]` **Friedman & Tukey 1974** — "A Projection Pursuit Algorithm for Exploratory Data Analysis" (IEEE Trans Computers). Coined the term.
- `[~]` **Diaconis & Freedman 1984** — "Asymptotics of Graphical Projection Pursuit" (Annals of Statistics). Proves most projections are Gaussian — theoretical foundation for our generic illegibility condition.
- `[~]` **Asimov 1985** — "The Grand Tour: A Tool for Viewing Multidimensional Data" (SIAM J Sci Comput). Dense paths on the Grassmannian — directly relates to our viewer.
- `[~]` **Cook et al. 1995** — "Grand Tour and Projection Pursuit" (J Computational & Graphical Statistics). Guided tour = PP-steered grand tour — our viewer is a clue-steered analog.

**Latent space steganography (they hide for concealment, we design for legibility):**
- `[~]` **Fernandez et al. 2023** — "The Stable Signature: Rooting Watermarks in Latent Diffusion Models" (ICCV 2023). Watermarks in latent space.
- `[~]` **Baluja 2017** — "Hiding Images in Plain Sight: Deep Steganography" (NeurIPS). Pioneering deep steganography.
- `[~]` **Boenisch 2021** — "A Systematic Review on Model Watermarking for Neural Networks" (Frontiers). Survey for positioning.

**Concept-guided directions (foundation for Type II semantic anamorphs):**
- `[~]` **Kim et al. 2018** — "TCAV: Testing with Concept Activation Vectors" (ICML 2018). Concept directions in activation space. arXiv: 1711.11279
- `[~]` **Zou et al. 2023** — "Representation Engineering" (arXiv: 2310.01405). Steering vectors, population-level representations.
- `[~]` **Park et al. 2024** — "The Linear Representation Hypothesis and the Geometry of Large Language Models" (ICML 2024). Formal grounding for concepts as linear directions. arXiv: 2311.03658
- `[~]` **Bolukbasi et al. 2016** — "Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings" (NeurIPS). Gender direction as a linear subspace — early semantic projection example.

### Core framing (Sections I, III — Grassmannian geometry)

- `[~]` **Edelman, Arias & Smith 1998** — "The Geometry of Algorithms with Orthogonality Constraints" (SIAM J Matrix Anal). Foundational geometry of Grassmann/Stiefel manifolds. ~2880 citations. DOI: 10.1137/S0895479895290954
- `[~]` **Bjorck & Golub 1973** — "Numerical Methods for Computing Angles Between Linear Subspaces" (Math Computation). Foundational paper on principal angles via SVD.
- `[~]` **Ye & Lim 2016** — "Schubert Varieties and Distances between Subspaces" (SIAM). DOI: 10.1137/15M1054201
- `[~]` **Johnson & Lindenstrauss 1984** — "Extensions of Lipschitz Mappings into a Hilbert Space." The JL lemma. Supports condition C2 (generic illegibility).
- `[~]` **Diaconis & Freedman 1984** — (see above; dual role: projection pursuit + theoretical foundation)

---

## P1 — Search While Drafting

### Section II — Related Work
- `[ ]` **Vidal 2011** — "Subspace Clustering" survey (IEEE Signal Processing Magazine)
- `[ ]` **Koh et al. 2020** — "Concept Bottleneck Models" (ICML). arXiv: 2007.04612
- `[ ]` **Alain & Bengio 2016** — "Understanding Intermediate Layers Using Linear Classifier Probes" (ICLR Workshop)
- `[ ]` **Bau et al. 2017** — "Network Dissection" (CVPR). Concept-unit alignment.
- `[ ]` Anamorphosis art history reference (Baltrušaitis 1977 or Araujo 2020 survey)

### Section IV — Construction Methods
- `[ ]` **Absil, Mahony & Sepulchre 2008** — "Optimization Algorithms on Matrix Manifolds" (Princeton). Optimization on Grassmannians.
- `[ ]` **Elhamifar & Vidal 2013** — "Sparse Subspace Clustering" (PAMI). SSC for context.

### Section V — Implementation
- `[ ]` **Wickham et al. 2011** — "tourr: An R Package for Exploring Multivariate Data with Projections" (J Statistical Software). Modern tour implementation.
- `[ ]` **Cook et al. 2008** — "Grand Tours, Projection Pursuit Guided Tours, and Manual Controls" (Handbook chapter).

---

## P2 — Only If Needed Later

- Compressed sensing (Candes/Donoho 2006) — if formalizing recovery guarantees
- Baraniuk & Wakin 2009 — "Random Projections of Smooth Manifolds" — if discussing manifold preservation
- Mikolov et al. 2013 — Word2Vec semantic arithmetic — if discussing concept directions history
- Papadimitriou et al. 2025 — SAEs on VLM embedding spaces — if connecting to mechanistic interpretability

---

## Good-Enough-to-Draft Threshold

**Start drafting once the P0 papers are noted. The formal definition (Section III) draft exists. Next: Sections I and II.**

---

## Sources Already Collected

(all P0 candidates identified — need reading notes before moving to Sources Already Collected)
