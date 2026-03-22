---
section: "III. Formal Definition"
status: draft
last_updated: 2026-03-22
---

## Argument

This section establishes the latent anamorph as a formal mathematical object, distinguishing it from existing constructs (steganography, dimensionality reduction, subspace methods) by defining its unique properties: observer-conditioned legibility, designed polysemy, decoy structure, and clue-guided recovery. The formalism should be precise enough to support the construction methods in Section IV while remaining accessible to readers from art, HCI, and ML backgrounds.

## Gaps

- Need to cite Grassmannian geometry for the observer map space
- Need to cite principal angles for the alignment metric
- Legibility score $L$ needs a concrete instantiation (probably silhouette score or structural similarity)
- Decoy quality metric needs more thought

## Draft

### Definition 1: Latent Anamorph

A **latent anamorph** is a tuple $\mathcal{A} = (X, d, \mathcal{O}, L, \Theta^*, \Theta^D)$ where:

- $X = \{x_1, \dots, x_N\} \subset \mathbb{R}^d$ is a **point set** in ambient dimension $d$.
- $\mathcal{O} = \{f_\theta : \mathbb{R}^d \to \mathbb{R}^k \mid \theta \in \Theta\}$ is a family of **observer maps** parameterized by $\theta$, where $k \ll d$ is the observation dimension (typically $k = 2$ or $k = 3$).
- $L : \mathbb{R}^{N \times k} \to [0, 1]$ is a **legibility function** that scores how much coherent structure is present in a projected point set.
- $\Theta^* \subset \Theta$ is the **privileged observer set** — parameters under which the intended structure is legible.
- $\Theta^D \subset \Theta$ is the **decoy observer set** — parameters that yield coherent but misleading structure.

These satisfy three conditions:

**(C1) Privileged legibility.** For $\theta \in \Theta^*$, the projected points $f_\theta(X)$ exhibit high legibility:

$$\forall \theta \in \Theta^* : L(f_\theta(X)) \geq \tau^*$$

where $\tau^*$ is a legibility threshold (e.g., $\tau^* = 0.8$).

**(C2) Generic illegibility.** For generic $\theta$ sampled uniformly from $\Theta$, the projected points appear unstructured:

$$\mathbb{E}_{\theta \sim \text{Uniform}(\Theta)}[L(f_\theta(X))] \leq \tau_0$$

where $\tau_0 \ll \tau^*$ (e.g., $\tau_0 = 0.1$).

**(C3) Decoy coherence.** For $\theta \in \Theta^D$, the projected points exhibit intermediate legibility with a different coherent form than the privileged view:

$$\forall \theta \in \Theta^D : L(f_\theta(X)) \geq \tau^D, \quad \text{where } \tau_0 < \tau^D \leq \tau^*$$

and the structure revealed under $\Theta^D$ is distinguishable from that under $\Theta^*$.

### Definition 2: Observer Map Types

The family $\mathcal{O}$ admits several instantiations of increasing complexity:

**Type I — Linear projection.** The observer map is a linear projection onto a $k$-dimensional subspace:

$$f_\theta(x) = U_\theta^\top x, \quad U_\theta \in \mathbb{R}^{d \times k}, \quad U_\theta^\top U_\theta = I_k$$

The parameter space $\Theta$ is the Grassmannian $\text{Gr}(k, d)$, the manifold of $k$-dimensional subspaces of $\mathbb{R}^d$. For $k = 2, d = 64$, this is a 124-dimensional manifold. The privileged observer $\Theta^*$ is a point (or small neighborhood) on this manifold.

**Type II — Semantic projection.** The projection basis is derived from concept directions in a learned embedding space rather than arbitrary coordinates:

$$U_\theta = g(\text{concept}_1, \text{concept}_2, \dots, \text{concept}_k)$$

where $g$ maps semantic descriptors (words, examples, difference vectors) to an orthonormal basis. Recovery requires semantic understanding — the correct projection is specified linguistically rather than numerically.

**Type III — Relational decoding.** The observer map operates on the relational structure of $X$ rather than coordinates:

$$f_\theta(X) = h_\theta(\mathcal{G}(X, \theta))$$

where $\mathcal{G}(X, \theta)$ constructs a graph (e.g., $k$-nearest neighbor graph under metric $\theta$) and $h_\theta$ extracts structure from the graph (e.g., community detection, diffusion, spectral embedding). The hidden form is not visible in any coordinate projection but emerges from the topology of the point cloud under the correct metric or graph construction.

### Definition 3: Properties of a Latent Anamorph

**Polysemantic capacity** $\kappa(\mathcal{A})$: the number of distinct coherent views supported by the object. This includes both privileged and decoy views:

$$\kappa = |\Theta^*| + |\Theta^D|$$

For a Type I anamorph in $\mathbb{R}^d$ with $k = 2$, the theoretical maximum is $\lfloor d/2 \rfloor$ orthogonal 2D subspaces. In practice, noise coupling limits this to substantially fewer legible views.

**Legibility contrast** $\lambda(\mathcal{A})$: the ratio of privileged legibility to generic legibility:

$$\lambda = \frac{\min_{\theta \in \Theta^*} L(f_\theta(X))}{\mathbb{E}_{\theta \sim \text{Uniform}(\Theta)}[L(f_\theta(X))]}$$

Higher $\lambda$ means the privileged view stands out more sharply against the noise floor. Our Phase 1 prototype achieves $\lambda > 10$ for text forms and $\lambda > 20$ for geometric shapes.

**Recovery difficulty** $\rho(\mathcal{A})$: the probability that a random search strategy discovers a privileged view within $T$ steps. For Type I anamorphs, this depends on the volume of $\Theta^*$ relative to $\text{Gr}(k, d)$. Without clues, $\rho$ is vanishingly small for $d \gg k$ — our prototype at $d = 64, k = 2$ requires guided search (principal angle decomposition) rather than random exploration.

**Alignment metric.** The distance between an observer $\theta$ and the nearest privileged observer $\theta^* \in \Theta^*$ is measured by the Frobenius norm of the subspace inner product matrix. For two $k$-dimensional subspaces with bases $U, V$:

$$\text{align}(U, V) = \frac{\|U^\top V\|_F}{\sqrt{k}}$$

This equals 1 when the subspaces coincide and approaches 0 when they are orthogonal. It is equivalent to the root-mean-square cosine of the principal angles between the subspaces.

### Definition 4: Clue Channel

A **clue channel** is a function $c : \Theta^* \to \mathcal{H}$ that maps the privileged observer to a hint in some representation space $\mathcal{H}$. The clue provides information that reduces recovery difficulty without directly revealing the privileged projection.

Examples:
- **Textual clue** ($\mathcal{H}$ = natural language): "The form is a greeting."
- **Example clue** ($\mathcal{H}$ = point set): a small subset of points that, when projected correctly, give a partial preview.
- **Semantic clue** ($\mathcal{H}$ = concept space): a set of concept terms whose embedding directions span or approximate the privileged subspace. This is the bridge from Type I to Type II anamorphs.
- **Gradient clue** ($\mathcal{H} = T_\theta \Theta$): a direction in the observer parameter space pointing toward increased legibility. This is what our interactive viewer provides.

The clue channel converts the anamorph from a pure search problem (intractable for $d \gg k$) into a guided discovery (tractable and aesthetically satisfying).

## Sources Used

| Paper | Key contribution to this section |
|-------|--------------------------------|
| (Grassmannian geometry — TBD) | Formal structure of the observer parameter space |
| (Principal angles — TBD) | Alignment metric between subspaces |
| (Johnson-Lindenstrauss — TBD) | Random projection properties, generic illegibility |
