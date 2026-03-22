# Search Queue

## Status Key
- `[ ]` — Not started
- `[~]` — Found candidate, not yet downloaded/read
- `[x]` — Done — paper found, noted

---

## P0 — Must Have Before Drafting

### Literature positioning (establish novelty)

- `[~]` **De Nicola et al. 2015** — "Anamorphic Projection: Analogical/Digital Algorithms" (Nexus Network Journal). Computational anamorphosis using descriptive geometry and procedural algorithms. DOI: 10.1007/s00004-014-0225-5
- `[~]` **Bermano et al. 2023** — "Bending the light: Next generation anamorphic sculptures" (Computers & Graphics). Extends anamorphic art to freeform reflective/refractive media with raytracing. DOI: 10.1016/j.cag.2023.05.023
- `[~]` **Friedman & Tukey 1974** — "A Projection Pursuit Algorithm for Exploratory Data Analysis" (IEEE Trans Computers). Foundational work on finding interesting projections in high-d data. The closest classical precedent — they search for structure, we design it.
- `[~]` **Asimov 1985** — "The Grand Tour: A Tool for Viewing Multidimensional Data" (SIAM J Sci Comput). Smooth animation through projection space — directly related to our viewer interaction.
- `[~]` **Fernandez et al. 2023** — "The Stable Signature: Rooting Watermarks in Latent Diffusion Models" (ICCV 2023). Embeds recoverable marks in latent representations — closest steganography precedent.
- `[~]` **LaWa 2024** — "Using Latent Space for In-Generation Image Watermarking" (ECCV 2024). Watermark embedding in latent space of diffusion models.

### Core framing (Sections I, III)

- `[~]` **Kim et al. 2018** — "Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV)" (ICML 2018). Defines concept directions in neural network latent spaces. Foundation for our Type II (semantic-keyed) anamorphs. arXiv: 1711.11279
- `[~]` **Koh et al. 2020** — "Concept Bottleneck Models" (ICML 2020). Interpretable networks that predict via intermediate concept representations. arXiv: 2007.04612
- `[~]` **Zou et al. 2023** — "Representation Engineering: A Top-Down Approach to AI Transparency." Steering vectors and population-level representations in LLMs. Geometric/topological structure in latent space. arXiv: 2310.01405

### Section III — Formal Definition (Grassmannian geometry)

- `[~]` **Ye & Lim 2016** — "Schubert varieties and distances between subspaces" (SIAM J Matrix Anal). Principal angles as the fundamental invariant of subspace geometry. arXiv: 1407.0900
- `[~]` **Mandolesi 2019** — "Grassmann angles between real or complex subspaces." Extends angular metrics on Grassmannians. arXiv: 1910.00147
- `[~]` **Johnson & Lindenstrauss 1984** — "Extensions of Lipschitz mappings into a Hilbert space." The JL lemma: random projections preserve distances. Supports our generic illegibility condition (C2).
- `[~]` **Hamm & Lee 2008** — "Grassmann Discriminant Analysis: a Unifying View on Subspace-Based Learning" (ICML 2008). Machine learning on Grassmannians.

---

## P1 — Search While Drafting

### Section II — Related Work
- `[ ]` Subspace clustering survey (Vidal 2011 or similar)
- `[ ]` Neural network steganography survey
- `[ ]` Anamorphosis history (Baltrušaitis "Anamorphic Art" 1977 or similar art history source)

### Section IV — Construction Methods
- `[ ]` Optimization on Grassmannians (Edelman, Arias, Smith 1998)
- `[ ]` Noise injection / signal-to-noise in high-d embeddings

### Section V — Implementation
- `[ ]` Interactive visualization of high-d data (tourr package, Cook & Buja)

---

## P2 — Only If Needed Later

- Compressed sensing (Candes, Donoho) — useful if we formalize recovery guarantees, not essential for art/tool framing
- Topological data analysis — useful if we pursue relational anamorphs (Type III)
- Sparse autoencoders / mechanistic interpretability — useful if we connect to SAE features in Discussion

---

## Good-Enough-to-Draft Threshold

**Start drafting once the P0 literature positioning papers are noted and the Grassmannian/principal angle references are confirmed.** The formal definition (Section III) is the most citation-dependent section. Sections I and V can be drafted from the prototype.

---

## Sources Already Collected

(none yet — all candidates identified, need reading notes)
