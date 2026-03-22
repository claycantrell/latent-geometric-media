#!/usr/bin/env python3
"""
Phase 2 Demo: Semantic-Keyed Latent Anamorph

The hidden form lives in a subspace defined by concept directions.
Different text queries produce different projections — only semantically
correct queries reveal the form.

Usage:
    python demo_semantic.py                  # run full demo with contrast queries
    python demo_semantic.py --query "ice"    # try a single-word query
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from construct import text_to_points, shape_to_points
from semantic import (
    construct_semantic_anamorph,
    query_to_basis,
    concept_query_to_basis,
    concept_direction,
    compute_alignment,
    embed_texts,
)


def build_demo_anamorph():
    """Build a semantic anamorph with concept-defined privileged view."""

    privileged_concepts = [
        (["cold", "frozen", "ice", "winter", "arctic"], ["warm", "hot", "fire", "summer", "tropical"]),
        (["mechanical", "industrial", "machine", "metal", "robotic"], ["organic", "natural", "living", "plant", "biological"]),
    ]

    intended = ("COLD", text_to_points("COLD", 2000, font_size=90))
    decoys = [
        ("spiral", shape_to_points("spiral", 2000)),
        ("triangle", shape_to_points("triangle", 2000)),
    ]

    print("Building semantic anamorph...")
    print(f"  Axis 1: cold/frozen ↔ warm/hot")
    print(f"  Axis 2: mechanical ↔ organic")
    print()

    result = construct_semantic_anamorph(
        intended_image=intended,
        decoy_images=decoys,
        privileged_concepts=privileged_concepts,
        noise_scale=0.05,
        signal_scale=3.0,
        seed=42,
    )

    print(f"  Ambient dimension: {result['embedding_dim']}d")
    print(f"  Points: {result['anamorph'].points.shape[0]}")
    print()

    return result


def test_contrast_queries(result):
    """
    Test contrast-based queries (positive vs negative word sets).
    This matches how the subspace was built — the user provides
    the semantic clue as a contrast, not a single phrase.
    """
    anamorph = result["anamorph"]
    priv_basis = anamorph.bases[anamorph.privileged_index]

    # Each query is a pair of concept contrasts → 2D basis
    contrast_queries = [
        # Exact match
        {
            "label": "EXACT: cold↔warm × mechanical↔organic",
            "concepts": result["privileged_concepts"],
        },
        # Close: right concepts, fewer words
        {
            "label": "cold↔warm × machine↔nature",
            "concepts": [
                (["cold"], ["warm"]),
                (["machine"], ["nature"]),
            ],
        },
        # Close: synonyms
        {
            "label": "freezing↔boiling × robotic↔alive",
            "concepts": [
                (["freezing", "icy"], ["boiling", "scorching"]),
                (["robotic", "automated"], ["alive", "growing"]),
            ],
        },
        # One axis right, one wrong
        {
            "label": "cold↔warm × happy↔sad",
            "concepts": [
                (["cold"], ["warm"]),
                (["happy"], ["sad"]),
            ],
        },
        # One axis right, one random
        {
            "label": "mechanical↔organic × big↔small",
            "concepts": [
                (["mechanical"], ["organic"]),
                (["big"], ["small"]),
            ],
        },
        # Both axes wrong but coherent
        {
            "label": "fast↔slow × loud↔quiet",
            "concepts": [
                (["fast", "quick"], ["slow", "sluggish"]),
                (["loud", "noisy"], ["quiet", "silent"]),
            ],
        },
        # Completely unrelated
        {
            "label": "democracy↔monarchy × guitar↔piano",
            "concepts": [
                (["democracy", "voting"], ["monarchy", "king"]),
                (["guitar", "strings"], ["piano", "keys"]),
            ],
        },
        # Swapped polarity (cold→warm instead of warm→cold)
        {
            "label": "SWAPPED: warm↔cold × organic↔mechanical",
            "concepts": [
                (["warm"], ["cold"]),
                (["organic"], ["mechanical"]),
            ],
        },
    ]

    print("Contrast-query alignment tests:")
    print(f"{'Query':<50} {'Align':>6}")
    print("-" * 58)

    results_list = []
    for q in contrast_queries:
        basis = concept_query_to_basis(q["concepts"])
        align = compute_alignment(basis, priv_basis)
        bar = "█" * int(align * 30)
        print(f"{q['label']:<50} {align:>5.3f}  {bar}")
        results_list.append((q["label"], align, basis))

    print()
    return results_list


def render_grid(result, queries):
    """Render a grid of contrast-query projections."""
    anamorph = result["anamorph"]
    X = anamorph.points

    # Add decoy views
    for i, (basis, label) in enumerate(zip(anamorph.bases, anamorph.labels)):
        if i != anamorph.privileged_index:
            priv_basis = anamorph.bases[anamorph.privileged_index]
            queries.append((f"[decoy: {label}]", compute_alignment(basis, priv_basis), basis))

    n = len(queries)
    cols = 3
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows), facecolor="black")
    fig.patch.set_facecolor("black")
    if rows == 1:
        axes = [axes]
    axes = np.array(axes).flatten()

    for i, (label, align, basis) in enumerate(queries):
        proj = X @ basis
        ax = axes[i]
        ax.set_facecolor("black")

        if "[decoy" in label:
            color = "#44ff88"
        elif align > 0.85:
            color = "#ff4444"
        elif align > 0.6:
            color = "#ffaa44"
        elif align > 0.35:
            color = "#ffff44"
        else:
            color = "#4488ff"

        ax.scatter(proj[:, 0], proj[:, 1], s=2.5, alpha=0.6, c=color, edgecolors="none")

        # Wrap long labels
        display_label = label if len(label) < 40 else label[:37] + "..."
        ax.set_title(f'{display_label}\nalign={align:.3f}', fontsize=9, color="white", fontweight="bold")
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])

    for i in range(len(queries), len(axes)):
        axes[i].set_visible(False)

    fig.suptitle(
        "Semantic-Keyed Anamorph: concept contrasts → projection → form",
        fontsize=14, color="white", fontweight="bold", y=0.98
    )
    plt.tight_layout()
    plt.savefig("semantic_output.png", dpi=150, facecolor="black")
    print("Saved semantic_output.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default=None)
    args = parser.parse_args()

    result = build_demo_anamorph()

    if args.query:
        from semantic import query_to_basis
        anamorph = result["anamorph"]
        priv_basis = anamorph.bases[anamorph.privileged_index]
        basis = query_to_basis(args.query)
        align = compute_alignment(basis, priv_basis)
        proj = anamorph.points @ basis
        fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor="black")
        ax.set_facecolor("black")
        color = "#ff4444" if align > 0.8 else "#ffaa44" if align > 0.4 else "#4488ff"
        ax.scatter(proj[:, 0], proj[:, 1], s=3, alpha=0.6, c=color, edgecolors="none")
        ax.set_title(f'Query: "{args.query}" | alignment: {align:.3f}', fontsize=12, color="white")
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        plt.tight_layout()
        plt.savefig("semantic_query.png", dpi=150, facecolor="black")
        print(f'Query: "{args.query}" → alignment: {align:.3f}')
        print("Saved semantic_query.png")
    else:
        queries = test_contrast_queries(result)
        render_grid(result, queries)


if __name__ == "__main__":
    main()
