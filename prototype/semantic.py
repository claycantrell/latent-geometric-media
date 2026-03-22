"""
Latent Anamorph — Phase 2: Semantic-Keyed Construction

The privileged projection is defined by concept directions in a sentence
embedding space. Recovery requires providing the right semantic query.

Example: the hidden image lives in the 2D subspace spanned by
  direction("cold" - "warm") and direction("mechanical" - "organic")
A user who queries "frozen machinery" gets close; "tropical garden" does not.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from construct import construct_anamorph, text_to_points, shape_to_points, LatentAnamorph


# ---------------------------------------------------------------------------
# Concept direction extraction
# ---------------------------------------------------------------------------

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed a list of texts into the sentence-transformer space. Returns (n, d)."""
    model = get_model()
    return model.encode(texts, normalize_embeddings=True)


def concept_direction(positive: list[str], negative: list[str]) -> np.ndarray:
    """
    Compute a concept direction as mean(positive) - mean(negative), normalized.
    E.g., concept_direction(["cold", "frozen", "ice"], ["warm", "hot", "fire"])
    """
    pos = embed_texts(positive).mean(axis=0)
    neg = embed_texts(negative).mean(axis=0)
    direction = pos - neg
    direction /= np.linalg.norm(direction)
    return direction


def concept_basis(concepts: list[tuple[list[str], list[str]]]) -> np.ndarray:
    """
    Build an orthonormal basis from multiple concept directions.

    Args:
        concepts: list of (positive_words, negative_words) pairs
                  e.g., [(["cold"], ["warm"]), (["mechanical"], ["organic"])]

    Returns:
        (d, k) orthonormal matrix where k = len(concepts)
    """
    directions = []
    for pos, neg in concepts:
        directions.append(concept_direction(pos, neg))

    # Stack and orthogonalize via QR
    D = np.column_stack(directions)  # (d, k)
    Q, _ = np.linalg.qr(D)
    return Q


# ---------------------------------------------------------------------------
# Semantic anamorph construction
# ---------------------------------------------------------------------------

def construct_semantic_anamorph(
    intended_image: tuple[str, np.ndarray],
    decoy_images: list[tuple[str, np.ndarray]],
    privileged_concepts: list[tuple[list[str], list[str]]],
    decoy_concepts: list[list[tuple[list[str], list[str]]]] | None = None,
    noise_scale: float = 0.05,
    signal_scale: float = 3.0,
    seed: int = 42,
) -> dict:
    """
    Construct a semantic-keyed latent anamorph.

    The ambient space IS the sentence-transformer embedding space (384d for MiniLM).
    The privileged subspace is defined by concept directions.

    Args:
        intended_image: (name, 2D points) for the hidden form
        decoy_images: list of (name, 2D points) for decoy forms
        privileged_concepts: list of (positive, negative) word pairs defining the
                            privileged 2D subspace
        decoy_concepts: optional list of concept pairs for each decoy image's subspace.
                       If None, random orthogonal subspaces are used for decoys.
        noise_scale: noise in ambient dimensions
        signal_scale: scale factor for the 2D point sets
        seed: random seed

    Returns:
        dict with anamorph, bases, concept metadata, and the embedding model dimension
    """
    rng = np.random.default_rng(seed)

    # Get embedding dimension from the model
    d = get_model().get_sentence_embedding_dimension()

    # Build privileged basis from concepts
    priv_basis = concept_basis(privileged_concepts)  # (d, 2)

    # Build decoy bases
    all_bases = [priv_basis]
    if decoy_concepts:
        for dc in decoy_concepts:
            all_bases.append(concept_basis(dc))
    else:
        # Random bases orthogonal to privileged (and each other)
        # Use QR on a big matrix to get orthogonal subspaces
        used_dims = priv_basis.shape[1]
        remaining = d - used_dims
        for _ in decoy_images:
            rand_vecs = rng.standard_normal((d, 2))
            # Project out all used subspaces
            for b in all_bases:
                for col in range(b.shape[1]):
                    proj = rand_vecs.T @ b[:, col:col+1]
                    rand_vecs -= b[:, col:col+1] @ proj.T
            Q, _ = np.linalg.qr(rand_vecs)
            all_bases.append(Q[:, :2])

    # Scale images
    all_images = [
        (intended_image[0], intended_image[1] * signal_scale),
    ] + [
        (name, pts * signal_scale) for name, pts in decoy_images
    ]

    # Embed each image into its subspace
    all_points = []
    all_origins = []
    for i, ((name, pts_2d), basis) in enumerate(zip(all_images, all_bases)):
        embedded = pts_2d @ basis.T  # (n, 2) @ (2, d) = (n, d)
        embedded += rng.standard_normal(embedded.shape) * noise_scale
        all_points.append(embedded)
        all_origins.append(np.full(len(pts_2d), i, dtype=int))

    points = np.concatenate(all_points, axis=0)
    origins = np.concatenate(all_origins, axis=0)

    # Shuffle
    perm = rng.permutation(len(points))
    points = points[perm]
    origins = origins[perm]

    anamorph = LatentAnamorph(
        points=points,
        ambient_dim=d,
        bases=all_bases,
        labels=[name for name, _ in all_images],
        privileged_index=0,
        point_origins=origins,
    )

    return {
        "anamorph": anamorph,
        "privileged_concepts": privileged_concepts,
        "embedding_dim": d,
    }


# ---------------------------------------------------------------------------
# Semantic query → projection
# ---------------------------------------------------------------------------

def query_to_basis(query: str, n_components: int = 2) -> np.ndarray:
    """
    Convert a free-text query into a projection basis.

    For a single query string, we embed it and use it as one axis,
    then find an orthogonal direction in the embedding space for the second axis.
    """
    vec = embed_texts([query])[0]  # (d,)
    # For the second axis, use a random vector orthogonal to the first
    d = len(vec)
    rand = np.random.randn(d)
    rand -= np.dot(rand, vec) * vec
    rand /= np.linalg.norm(rand)
    return np.column_stack([vec, rand])


def query_pair_to_basis(query1: str, query2: str) -> np.ndarray:
    """
    Convert two query strings into a 2D projection basis.
    Each query becomes one axis (orthogonalized).
    """
    vecs = embed_texts([query1, query2])
    return np.linalg.qr(vecs.T)[0][:, :2]


def concept_query_to_basis(
    concepts: list[tuple[list[str], list[str]]]
) -> np.ndarray:
    """
    Convert concept pairs (same format as construction) into a projection basis.
    This is the "correct" query — should recover the privileged view.
    """
    return concept_basis(concepts)


def compute_alignment(basis_a: np.ndarray, basis_b: np.ndarray) -> float:
    """Alignment between two 2D bases (Frobenius of cross-product / sqrt(2))."""
    M = basis_a.T @ basis_b
    return min(1.0, np.linalg.norm(M, 'fro') / np.sqrt(2))
