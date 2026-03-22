#!/usr/bin/env python3
"""Export a latent anamorph as JSON for the web viewer."""

import json
import numpy as np
from construct import construct_anamorph, text_to_points, shape_to_points

N = 3000
AMBIENT_DIM = 64  # smaller dim for web perf, still plenty for 4 images

images = [
    ("HELLO", text_to_points("HELLO", N, font_size=90) * 3.0),
    ("spiral", shape_to_points("spiral", N) * 3.0),
    ("triangle", shape_to_points("triangle", N) * 3.0),
    ("circle", shape_to_points("circle", N) * 3.0),
]

anamorph = construct_anamorph(
    images,
    privileged_index=0,
    ambient_dim=AMBIENT_DIM,
    noise_scale=0.05,
    seed=42,
)

# Round to 3 decimals for compact JSON
data = {
    "ambient_dim": AMBIENT_DIM,
    "n_points": len(anamorph.points),
    "n_images": len(anamorph.bases),
    "labels": anamorph.labels,
    "privileged_index": anamorph.privileged_index,
    "points": np.round(anamorph.points, 3).tolist(),
    "bases": [np.round(b, 6).tolist() for b in anamorph.bases],
    "point_origins": anamorph.point_origins.tolist(),
}

out_path = "web/data.json"
with open(out_path, "w") as f:
    json.dump(data, f, separators=(",", ":"))

size_mb = len(json.dumps(data, separators=(",", ":"))) / 1e6
print(f"Exported {anamorph.points.shape[0]} points x {AMBIENT_DIM}d to {out_path} ({size_mb:.1f} MB)")
