#!/usr/bin/env python3
"""
Test Type III relational anamorph.

Shows:
- Top row: coordinate-based views (PCA, random proj, secret-dim PCA) → all blobs
- Bottom row: k-NN graphs (full Euclidean = mess, secret metric = FORM, ground truth)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from sklearn.decomposition import PCA

from relational import construct_relational_anamorph, text_to_skeleton


def draw_knn_graph(ax, points_for_dist, layout_2d, k=5, color="#ff4444", title=""):
    """Draw k-NN graph: compute neighbors from points_for_dist, render at layout_2d positions."""
    n = len(points_for_dist)
    tree = KDTree(points_for_dist)

    for i in range(n):
        _, idxs = tree.query(points_for_dist[i], k=k + 1)
        for j in idxs[1:]:
            ax.plot(
                [layout_2d[i, 0], layout_2d[j, 0]],
                [layout_2d[i, 1], layout_2d[j, 1]],
                c=color, alpha=0.12, linewidth=0.6
            )
    ax.scatter(layout_2d[:, 0], layout_2d[:, 1], s=6, c=color, alpha=0.8, zorder=5)
    ax.set_title(title, color="white", fontsize=10)
    ax.set_aspect("equal")


def main():
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

    points = result["points"]
    s_start, s_end = result["secret_dims"]
    target_layout = result["target_layout"]
    target_layout_norm = (target_layout - target_layout.mean(axis=0)) / (target_layout.std() + 1e-8)

    fig, axes = plt.subplots(2, 3, figsize=(18, 12), facecolor="black")
    for ax in axes.flatten():
        ax.set_facecolor("black")
        ax.set_xticks([])
        ax.set_yticks([])

    # --- Top row: coordinate projections (should all be blobs) ---

    # PCA all dims
    pca_all = PCA(n_components=2).fit_transform(points)
    axes[0, 0].scatter(pca_all[:, 0], pca_all[:, 1], s=5, c="#4488ff", alpha=0.6)
    axes[0, 0].set_title("PCA (all 100 dims) → blob", color="white", fontsize=10)
    axes[0, 0].set_aspect("equal")

    # Random projection
    rng = np.random.default_rng(77)
    rand_basis = np.linalg.qr(rng.standard_normal((100, 2)))[0]
    rand_proj = points @ rand_basis
    axes[0, 1].scatter(rand_proj[:, 0], rand_proj[:, 1], s=5, c="#4488ff", alpha=0.6)
    axes[0, 1].set_title("Random projection → blob", color="white", fontsize=10)
    axes[0, 1].set_aspect("equal")

    # PCA of secret dims only (coordinate hint — still needs the right 2D within 12D)
    pca_secret = PCA(n_components=2).fit_transform(points[:, s_start:s_end])
    axes[0, 2].scatter(pca_secret[:, 0], pca_secret[:, 1], s=5, c="#ffaa44", alpha=0.6)
    axes[0, 2].set_title(f"PCA of dims [{s_start}:{s_end}] → faint hint", color="#ffaa44", fontsize=10)
    axes[0, 2].set_aspect("equal")

    # --- Bottom row: graph-based views ---

    # k-NN graph with full Euclidean (should be mess)
    draw_knn_graph(
        axes[1, 0], points, pca_all, k=4,
        color="#4488ff",
        title="k-NN graph (all dims) → noise"
    )

    # k-NN graph with SECRET metric — rendered at TARGET LAYOUT positions
    draw_knn_graph(
        axes[1, 1], points[:, s_start:s_end], target_layout_norm, k=4,
        color="#ff4444",
        title=f"k-NN graph (dims [{s_start}:{s_end}]) → FORM"
    )

    # Ground truth
    axes[1, 2].set_title("Ground truth target graph", color="#44ff88", fontsize=10)
    for i, j in target_edges:
        axes[1, 2].plot(
            [target_layout_norm[i, 0], target_layout_norm[j, 0]],
            [target_layout_norm[i, 1], target_layout_norm[j, 1]],
            c="#44ff88", alpha=0.15, linewidth=0.6
        )
    axes[1, 2].scatter(target_layout_norm[:, 0], target_layout_norm[:, 1],
                       s=6, c="#44ff88", alpha=0.8)
    axes[1, 2].set_aspect("equal")

    fig.suptitle(
        "Type III Relational Anamorph\n"
        "No projection reveals the form — only the right distance metric does",
        color="white", fontsize=14, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig("relational_output.png", dpi=150, facecolor="black")
    print("Saved relational_output.png")


if __name__ == "__main__":
    main()
