# Research Outline

## Working Title
Latent Anamorphs: Observer-Conditioned Structure in High-Dimensional Geometric Media

## Research Question
Can we design high-dimensional point sets that reveal distinct coherent visual forms under different projection lenses, with intended structure emerging only for privileged observers or clues — and what are the mathematical properties, construction methods, and application domains of such objects?

## Thesis Statement
We introduce the *latent anamorph*, a high-dimensional geometric object designed to be intentionally polysemantic: distinct observers, projection keys, or semantic queries reveal distinct coherent structures, with one or more privileged readings embedded among decoys. We formalize this object class, present construction algorithms for direct-projection, semantic-keyed, and relational variants, and demonstrate applications spanning interactive art, concept-guided embedding exploration, and latent provenance marking.

## I. Introduction
- High-dimensional representations (embeddings, latent spaces) are central to modern ML, but are typically treated as opaque containers — structure is extracted, never designed in
- Anamorphosis in physical art: images that resolve only from a privileged viewpoint (historical precedent from Renaissance perspective art)
- Core idea: extend anamorphosis to high-dimensional space — design point sets where meaningful form is revealed only under the right projection, query, or decoding path
- This is not dimensionality reduction, not steganography, not hidden-subspace toys — the emphasis is on *appearance*, *observer dependence*, *designed legibility*, *decoy views*, and *recoverability through clue or semantics*
- The object is an **observer-conditioned latent form**: a structure with multiple possible appearances, where meaningful form requires a privileged family of projections or relational decodings
- **Contributions**: (1) We define the latent anamorph as a formal object class with ambient dimension, observer maps, legibility scores, privileged and decoy observer sets. (2) We present construction algorithms for three variants of increasing complexity: direct projection, semantic-keyed, and relational. (3) We demonstrate three application tracks: interactive geometric puzzles, concept-guided embedding exploration, and latent provenance signatures

## II. Related Work
- **Anamorphic art**: Physical perspective anamorphosis (De Caus, Niceron, Pozzo); cylindrical and conical mirror anamorphs; modern computational anamorphosis
- **Dimensionality reduction and projection**: PCA, t-SNE, UMAP — designed to *find* structure, not *embed* it; concept-guided projections (e.g., TCAV, concept bottleneck models)
- **Steganography and information hiding**: Classical steganography in images/audio; neural network steganography; watermarking in model weights — focused on concealment, not designed legibility or polysemantic form
- **Hidden structures in high dimensions**: Johnson-Lindenstrauss and random projections; compressed sensing and sparse recovery; subspace clustering
- **Embedding space geometry**: Representation engineering, steering vectors, linear probes — extracting structure from learned spaces vs. designing structure into constructed spaces
- **Gap**: No prior work designs high-dimensional point sets to be intentionally polysemantic with observer-conditioned legibility, decoy structures, and clue-guided recovery. We bridge anamorphic art, projection geometry, and embedding space analysis into a new object class

## III. Formal Definition
- **Definition of a latent anamorph**:
  - Ambient dimension $d$
  - Point set $X = \{x_1, \dots, x_n\} \subset \mathbb{R}^d$
  - Family of observer maps $\mathcal{O} = \{f_\theta\}$
  - Legibility score $L(f_\theta(X))$ — measures how coherent the projected structure appears
  - Privileged observer set $\Theta^*$ — projections that reveal intended structure
  - Decoy observer set $\Theta^D$ — projections that reveal coherent but misleading structure
  - For generic $\theta$, $f_\theta(X)$ appears unstructured
- **Properties**: polysemantic capacity (number of distinct coherent views), decoy density, legibility contrast (ratio of privileged to generic legibility), recovery difficulty
- **Observer map types**: linear projections ($f_\theta(X) = U_\theta^\top X$), semantic projections (basis derived from concept directions), relational decodings (neighbor graph, diffusion, thresholding)

## IV. Construction Methods

### 4.1 Direct Projection Anamorph (Version 1)
- Assign each intended image to a different 2D subspace of $\mathbb{R}^d$
- Embed image point sets into the common ambient space
- Add controlled noise and inter-subspace coupling to create decoy views
- Optimization: maximize legibility under privileged projections while minimizing legibility under random projections
- Clue channel: textual hint, example projection, or sequence of transformations pointing to the correct subspace

### 4.2 Semantic-Keyed Anamorph (Version 2)
- The correct projection basis is derived from concept directions rather than arbitrary coordinates
- Example: the intended view appears along a direction like "organic minus mechanical plus radial symmetry"
- Construction uses embedding-space concept vectors (e.g., difference vectors, TCAV-style directions) to define the privileged subspace
- Clue is linguistic — a phrase or set of examples that defines the projection lens
- Recovery requires semantic understanding, not brute-force search

### 4.3 Relational Anamorph (Version 3)
- The hidden structure is not visible in any coordinate projection
- Instead, under the correct metric, distance function, or graph construction:
  - Nearest-neighbor graph reveals the hidden form
  - Sorted pairwise distances reveal a pattern
  - Diffusion over the point-cloud graph draws the image
- Most novel variant — least reducible to "just a secret projection"
- Hardest to construct and explain; strongest intellectual contribution

## V. Implementation and Demonstrations

### 5.1 MVP System
- Input: 1 intended image + 2-3 decoy images, $d = 256$, $N = 2000$ points
- Construction pipeline: image-to-point-set, subspace assignment, ambient embedding, noise injection
- Interactive viewer: user rotates/searches projection space, coherent form appears at the correct viewpoint
- Clue system: textual hints guide the user toward the privileged projection

### 5.2 Semantic-Keyed Demo
- Puzzle where words or concept examples define the projection lens
- User provides a semantic query; system computes the concept-conditioned projection
- Correct query reveals the intended form; nearby queries reveal partial structure

### 5.3 Embedding Explorer
- Apply the same machinery to real embedding datasets (e.g., word embeddings, image embeddings, SAE features)
- "Here are three coherent latent views of your dataset under different concept lenses"
- Practical tool for researchers exploring vector spaces

## VI. Applications

### 6.1 Art and Puzzle Objects
- Interactive installations where users navigate latent objects and discover hidden forms
- Aesthetic payoff: the moment of recognition when the correct view resolves
- Gallery / web-based presentation

### 6.2 Embedding-Space Microscope
- Concept-guided exploration of high-dimensional datasets
- Language-guided projections reveal different valid structures in the same data
- Connection to interpretability and representation analysis

### 6.3 Latent Provenance Signatures
- Embed recoverable geometric markers in representations
- Provenance, watermarking, system identity
- Robustness considerations and limitations

## VII. Discussion
- **What is actually new**: a design framework for high-dimensional hidden-form objects; an interactive metaphor for embeddings and latent spaces; a new class of polysemantic geometric puzzles
- **Relationship to existing fields**: extends anamorphic art into high dimensions; complements embedding interpretability with designed (vs. discovered) structure; distinct from steganography in emphasis on legibility, polysemy, and clue-guided recovery
- **Limitations**: concealment is not cryptographic — no formal hardness guarantees; decoy quality depends on construction method; semantic-keyed version depends on quality of concept directions; relational version is computationally expensive
- **What not to claim**: not new cryptography, not strong concealment guarantees, not universal interpretability of dense spaces

## VIII. Conclusion
- Summary: latent anamorphs as a new class of observer-conditioned geometric media
- The core contribution is the combination of observer-conditioned reveal, decoy structure, relational decoding, and polysemantic objecthood
- Art-first, tool-second: the aesthetic and puzzle applications demonstrate the concept; the embedding explorer extends it to practical use
- Future work: formal legibility metrics, adversarial decoy construction, multi-modal anamorphs (text + image subspaces), connection to mechanistic interpretability, large-scale interactive installations

---
**Target venue:** arXiv preprint (initially); CHI, SIGGRAPH, or NeurIPS Creative AI track
**Target length:** 6000-8000 words
**Key deadlines:** None — move at our pace
