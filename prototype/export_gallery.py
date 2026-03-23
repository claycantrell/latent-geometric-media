#!/usr/bin/env python3
"""
Export a multi-shape latent sculpture for interactive exploration.

Multiple geometric forms embedded in their own subspaces of R^48.
Low noise, high signal — shapes are clearly visible when projected
onto their native subspace.
"""

import json
import numpy as np
from shapes import (
    helix, torus, linked_rings, lissajous, trefoil_knot,
    sphere_surface, mobius_strip, star_polygon,
)

rng = np.random.default_rng(42)
AMBIENT_DIM = 48

shapes = [
    {"name": "helix",     "color": "#ff4444", "pts": helix(1000, turns=5)},
    {"name": "torus",     "color": "#44aaff", "pts": torus(1500)},
    {"name": "trefoil",   "color": "#44ff88", "pts": trefoil_knot(1000)},
    {"name": "möbius",    "color": "#ffaa44", "pts": mobius_strip(1000)},
    {"name": "sphere",    "color": "#aa44ff", "pts": sphere_surface(1000)},
    {"name": "lissajous", "color": "#ff44aa", "pts": lissajous(800, a=3, b=4)},
    {"name": "star",      "color": "#ffff44", "pts": star_polygon(600, points=7)},
]

# Generate fully orthogonal basis
full_basis = np.linalg.qr(rng.standard_normal((AMBIENT_DIM, AMBIENT_DIM)))[0]

all_points = []
all_shape_ids = []
shape_bases = []  # store (d, 3) or (d, 2) basis for each shape's "best view"

dims_per_shape = 3
stride = 3  # NO overlap — each shape gets its own clean subspace

for i, shape in enumerate(shapes):
    start = i * stride
    basis = full_basis[:, start:start + dims_per_shape]  # (48, 3)

    pts = shape["pts"]
    native_dim = pts.shape[1]

    # Pad 2D shapes to 3D
    if native_dim == 2:
        pts = np.column_stack([pts, np.zeros(len(pts))])

    # Strong signal scale
    pts *= 3.0

    # Embed into ambient space
    embedded = pts @ basis.T  # (n, 3) @ (3, 48) = (n, 48)

    # Very low noise
    embedded += rng.standard_normal(embedded.shape) * 0.02

    all_points.append(embedded)
    all_shape_ids.extend([i] * len(pts))

    # Store the best 2D view basis (first 2 columns of the shape's subspace)
    shape_bases.append(basis[:, :2].tolist())

points = np.vstack(all_points)
shape_ids = np.array(all_shape_ids)

# Shuffle
perm = rng.permutation(len(points))
points = points[perm]
shape_ids = shape_ids[perm]

print(f"Built {len(points)} points from {len(shapes)} shapes in R^{AMBIENT_DIM}")

# --- Export ---
data = {
    "ambient_dim": AMBIENT_DIM,
    "n_points": len(points),
    "points": np.round(points, 3).tolist(),
    "shape_ids": shape_ids.tolist(),
    "shapes": [
        {"name": s["name"], "color": s["color"], "count": len(s["pts"]),
         "basis": shape_bases[i]}
        for i, s in enumerate(shapes)
    ],
}

out_path = "web/gallery_data.json"
with open(out_path, "w") as f:
    json.dump(data, f, separators=(",", ":"))

size_mb = len(json.dumps(data, separators=(",", ":"))) / 1e6
print(f"Exported to {out_path} ({size_mb:.1f} MB)")
