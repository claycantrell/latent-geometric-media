"""
Type III: Relational Anamorph

Points in R^d where no linear projection reveals the hidden form,
but the k-NN graph under a specific distance metric traces it.

Construction: embed the target graph's neighbor structure into a
secret subspace of dimensions, then randomize everything else.
"""

import numpy as np
from scipy.spatial import KDTree
from PIL import Image, ImageDraw, ImageFont


def text_to_skeleton(text: str, n_points: int = 300, font_size: int = 70) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """
    Render text as a point set with k-NN edges defining the target graph.
    """
    canvas_w, canvas_h = 500, 120
    img = Image.new("L", (canvas_w, canvas_h), 255)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (canvas_w - text_w) // 2
    y = (canvas_h - text_h) // 2
    draw.text((x, y), text, fill=0, font=font)

    pixels = np.array(img)
    dark = np.argwhere(pixels < 128)

    if len(dark) == 0:
        raise ValueError(f"No dark pixels for '{text}'")

    indices = np.random.choice(len(dark), n_points, replace=len(dark) < n_points)
    points = dark[indices].astype(float)
    points = np.column_stack([points[:, 1], -points[:, 0]])
    points = (points - points.mean(axis=0)) / (points.std() + 1e-8)

    # Build target neighbor graph
    tree = KDTree(points)
    edges = set()
    for i in range(len(points)):
        dists, idxs = tree.query(points[i], k=5)
        for j in idxs[1:]:
            edges.add((min(i, j), max(i, j)))

    return points, list(edges)


def construct_relational_anamorph(
    target_points_2d: np.ndarray,
    target_edges: list[tuple[int, int]],
    ambient_dim: int = 100,
    secret_dims: tuple[int, int] = (30, 42),
    seed: int = 42,
) -> dict:
    """
    Construct a Type III relational anamorph.

    Strategy (direct embedding, no iterative optimization):
    1. Place the target graph layout into a random 2D subspace within
       the secret dimensions. This ensures k-NN in the secret subspace
       recovers the target neighbors.
    2. Fill ALL dimensions (including secret) with Gaussian noise at a
       level that masks coordinate structure but preserves neighbor ordering.
    3. The secret subspace has signal + noise; other dims have only noise.
       Since signal dims are a minority, any projection mixing all dims
       is dominated by noise.

    The key insight: we don't need iterative optimization. We just need
    the signal-to-noise ratio in the secret subspace to be high enough
    that k-NN there recovers the graph, but low enough in any full-space
    projection that the structure is invisible.
    """
    rng = np.random.default_rng(seed)
    n = len(target_points_2d)
    d = ambient_dim
    s_start, s_end = secret_dims
    s_dim = s_end - s_start

    # Normalize target layout
    target = target_points_2d.copy()
    target = (target - target.mean(axis=0)) / (target.std() + 1e-8)

    # Embed target layout into a random 2D subspace within the secret dims
    # This rotation within the secret subspace means even knowing which dims
    # are secret, you still need to find the right 2D projection within them
    secret_basis = np.linalg.qr(rng.standard_normal((s_dim, s_dim)))[0][:, :2]
    target_in_secret = target @ secret_basis.T  # (n, s_dim)

    # Signal scale in secret dims
    signal_scale = 3.0
    # Noise in secret dims (small — preserves k-NN structure)
    secret_noise = 0.3
    # Noise in non-secret dims: MATCH total variance of secret dims
    # so PCA can't distinguish them. Secret variance ≈ signal^2 + secret_noise^2
    # Non-secret variance should be similar
    nonsecret_noise = np.sqrt(signal_scale ** 2 + secret_noise ** 2)

    # Build the point cloud
    points = np.zeros((n, d))
    # Non-secret dims: high noise (matches secret dim variance)
    non_secret_dims = list(range(0, s_start)) + list(range(s_end, d))
    points[:, non_secret_dims] = rng.standard_normal((n, len(non_secret_dims))) * nonsecret_noise
    # Secret dims: signal + small noise
    points[:, s_start:s_end] = target_in_secret * signal_scale + rng.standard_normal((n, s_dim)) * secret_noise

    # Verify: check that k-NN in secret subspace recovers target edges
    secret_coords = points[:, s_start:s_end]
    tree = KDTree(secret_coords)
    recovered = 0
    edge_set = set(target_edges)
    for i in range(n):
        _, idxs = tree.query(secret_coords[i], k=5)
        for j in idxs[1:]:
            if (min(i, j), max(i, j)) in edge_set:
                recovered += 1

    total_edge_slots = n * 4  # 4 neighbors per point
    recovery_rate = recovered / (len(target_edges) * 2)  # each edge counted from both ends
    print(f"  Edge recovery rate (secret metric): {recovery_rate:.1%}")

    # Verify: check that k-NN in FULL space does NOT recover target edges
    tree_full = KDTree(points)
    recovered_full = 0
    for i in range(n):
        _, idxs = tree_full.query(points[i], k=5)
        for j in idxs[1:]:
            if (min(i, j), max(i, j)) in edge_set:
                recovered_full += 1

    recovery_rate_full = recovered_full / (len(target_edges) * 2)
    print(f"  Edge recovery rate (full Euclidean): {recovery_rate_full:.1%}")
    print(f"  Ratio: {recovery_rate / (recovery_rate_full + 1e-8):.1f}x better with secret metric")

    return {
        "points": points,
        "ambient_dim": d,
        "secret_dims": secret_dims,
        "secret_basis": secret_basis,
        "target_edges": target_edges,
        "target_layout": target_points_2d,
        "n_points": n,
        "noise_scale": secret_noise,
        "signal_scale": signal_scale,
    }
