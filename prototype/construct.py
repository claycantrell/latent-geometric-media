"""
Latent Anamorph — Construction

Builds high-dimensional point clouds that reveal coherent 2D forms
only under privileged projections, with decoy views under other subspaces.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass


@dataclass
class LatentAnamorph:
    """A constructed latent anamorph with its metadata."""
    points: np.ndarray          # (N, d) ambient point cloud
    ambient_dim: int            # d
    bases: list                 # list of (d, 2) orthonormal bases — one per embedded image
    labels: list                # list of str — name for each embedded image
    privileged_index: int       # which basis is the "intended" one
    point_origins: np.ndarray   # (N,) int — which image each point belongs to


def text_to_points(text: str, n_points: int = 500, font_size: int = 60) -> np.ndarray:
    """Render text as a set of 2D points by sampling from dark pixels."""
    canvas_w, canvas_h = 400, 120
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
    dark = np.argwhere(pixels < 128)  # (row, col)

    if len(dark) == 0:
        raise ValueError(f"No dark pixels found for text '{text}'")

    indices = np.random.choice(len(dark), n_points, replace=True)
    points = dark[indices].astype(float)
    # Convert (row, col) to (x, y) with y flipped so text reads correctly
    points = np.column_stack([points[:, 1], -points[:, 0]])
    # Center and normalize to [-1, 1] range
    points = (points - points.mean(axis=0)) / (points.std() + 1e-8)
    return points


def shape_to_points(shape: str, n_points: int = 500) -> np.ndarray:
    """Generate 2D points forming a geometric shape."""
    if shape == "circle":
        theta = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
        noise = np.random.randn(n_points) * 0.03
        r = 1.0 + noise
        return np.column_stack([r * np.cos(theta), r * np.sin(theta)])

    elif shape == "star":
        theta = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
        # 5-pointed star: alternate between inner and outer radius
        r = np.where(np.sin(5 * theta / 2) > 0, 1.0, 0.4)
        # Smooth it slightly and add noise
        r += np.random.randn(n_points) * 0.05
        return np.column_stack([r * np.cos(theta), r * np.sin(theta)])

    elif shape == "spiral":
        t = np.linspace(0, 4 * np.pi, n_points)
        r = t / (4 * np.pi)
        x = r * np.cos(t) + np.random.randn(n_points) * 0.02
        y = r * np.sin(t) + np.random.randn(n_points) * 0.02
        return np.column_stack([x, y])

    elif shape == "triangle":
        # Sample points along edges of an equilateral triangle
        vertices = np.array([
            [0, 1],
            [-np.sqrt(3) / 2, -0.5],
            [np.sqrt(3) / 2, -0.5],
        ])
        points = []
        per_edge = n_points // 3
        for i in range(3):
            t = np.random.uniform(0, 1, per_edge)
            edge_pts = vertices[i] * (1 - t)[:, None] + vertices[(i + 1) % 3] * t[:, None]
            edge_pts += np.random.randn(per_edge, 2) * 0.02
            points.append(edge_pts)
        pts = np.concatenate(points, axis=0)
        return pts[:n_points]

    elif shape == "grid":
        side = int(np.sqrt(n_points))
        x = np.linspace(-1, 1, side)
        y = np.linspace(-1, 1, side)
        xx, yy = np.meshgrid(x, y)
        pts = np.column_stack([xx.ravel(), yy.ravel()])
        pts += np.random.randn(len(pts), 2) * 0.02
        indices = np.random.choice(len(pts), n_points, replace=True)
        return pts[indices]

    else:
        raise ValueError(f"Unknown shape: {shape}")


def random_orthonormal_basis(d: int, k: int = 2, rng=None) -> np.ndarray:
    """Generate a random k-dimensional orthonormal basis in R^d."""
    if rng is None:
        rng = np.random.default_rng()
    A = rng.standard_normal((d, k))
    Q, _ = np.linalg.qr(A)
    return Q[:, :k]  # (d, k)


def construct_anamorph(
    images: list[tuple[str, np.ndarray]],
    privileged_index: int = 0,
    ambient_dim: int = 256,
    noise_scale: float = 0.3,
    seed: int = 42,
) -> LatentAnamorph:
    """
    Construct a latent anamorph from a list of named 2D point sets.

    Args:
        images: list of (name, points) where points is (n, 2)
        privileged_index: which image is the "intended" one
        ambient_dim: dimension of ambient space
        noise_scale: std of Gaussian noise added in all dimensions
        seed: random seed for reproducibility

    Returns:
        LatentAnamorph with the constructed point cloud and metadata
    """
    rng = np.random.default_rng(seed)
    d = ambient_dim

    # Generate orthogonal subspaces for each image
    # We use a single large orthogonal matrix to ensure subspaces don't overlap
    n_images = len(images)
    if 2 * n_images > d:
        raise ValueError(f"Need at least {2 * n_images} ambient dims for {n_images} images")

    # Generate a random orthogonal matrix and carve out 2D subspaces
    full_basis = np.linalg.qr(rng.standard_normal((d, d)))[0]
    bases = []
    for i in range(n_images):
        basis = full_basis[:, 2 * i : 2 * i + 2]  # (d, 2)
        bases.append(basis)

    # Embed each 2D point set into ambient space
    all_points = []
    all_origins = []
    for i, (name, pts_2d) in enumerate(images):
        # pts_2d: (n, 2), basis: (d, 2)
        # Embedded: (n, 2) @ (d, 2).T = (n, d)
        embedded = pts_2d @ bases[i].T

        # Add noise in ALL dimensions
        embedded += rng.standard_normal(embedded.shape) * noise_scale

        all_points.append(embedded)
        all_origins.append(np.full(len(pts_2d), i, dtype=int))

    points = np.concatenate(all_points, axis=0)
    origins = np.concatenate(all_origins, axis=0)

    # Shuffle point order so origins aren't trivially grouped
    perm = rng.permutation(len(points))
    points = points[perm]
    origins = origins[perm]

    return LatentAnamorph(
        points=points,
        ambient_dim=d,
        bases=bases,
        labels=[name for name, _ in images],
        privileged_index=privileged_index,
        point_origins=origins,
    )
