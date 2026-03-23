#!/usr/bin/env python3
"""Export Type III relational anamorph for the web viewer."""

import json
import numpy as np
from relational import construct_relational_anamorph, text_to_skeleton

print("Building target skeleton...")
target_pts, target_edges = text_to_skeleton("HI", n_points=300, font_size=90)
print(f"  {len(target_pts)} points, {len(target_edges)} edges")

result = construct_relational_anamorph(
    target_points_2d=target_pts,
    target_edges=target_edges,
    ambient_dim=100,
    secret_dims=(30, 42),
    seed=42,
)

# Normalize target layout for rendering
layout = result["target_layout"]
layout = (layout - layout.mean(axis=0)) / (layout.std() + 1e-8)

data = {
    "ambient_dim": result["ambient_dim"],
    "n_points": result["n_points"],
    "points": np.round(result["points"], 3).tolist(),
    "secret_dims": list(result["secret_dims"]),
    "target_edges": [[int(i), int(j)] for i, j in result["target_edges"]],
    "target_layout": np.round(layout, 4).tolist(),
}

out_path = "web/relational_data.json"
with open(out_path, "w") as f:
    json.dump(data, f, separators=(",", ":"))

size_mb = len(json.dumps(data, separators=(",", ":"))) / 1e6
print(f"Exported to {out_path} ({size_mb:.1f} MB)")
