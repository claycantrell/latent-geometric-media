#!/usr/bin/env python3
"""
Latent Anamorph — Phase 1 Demo

Constructs a latent anamorph with one intended image and several decoys,
then launches an interactive viewer to explore the projection space.

Usage:
    python demo.py                    # interactive viewer
    python demo.py --grid             # show privileged vs random projections
    python demo.py --all              # show all embedded views side by side
    python demo.py --text "SECRET"    # use custom text as the intended image
"""

import argparse
import sys

from construct import (
    construct_anamorph,
    text_to_points,
    shape_to_points,
)
from viewer import AnamorphViewer, view_all_embedded, view_random_grid


def build_default_anamorph(intended_text="HELLO", n_points=500, ambient_dim=256, noise=0.3):
    """Build the default demo anamorph: one text + three shape decoys."""
    images = [
        (intended_text, text_to_points(intended_text, n_points)),
        ("spiral", shape_to_points("spiral", n_points)),
        ("triangle", shape_to_points("triangle", n_points)),
        ("circle", shape_to_points("circle", n_points)),
    ]

    anamorph = construct_anamorph(
        images=images,
        privileged_index=0,
        ambient_dim=ambient_dim,
        noise_scale=noise,
        seed=42,
    )

    print(f"Constructed latent anamorph:")
    print(f"  {anamorph.points.shape[0]} points in R^{anamorph.ambient_dim}")
    print(f"  {len(anamorph.bases)} embedded views: {anamorph.labels}")
    print(f'  Intended view: "{anamorph.labels[anamorph.privileged_index]}"')
    print()

    return anamorph


def main():
    parser = argparse.ArgumentParser(description="Latent Anamorph — Phase 1 Demo")
    parser.add_argument("--grid", action="store_true", help="Show privileged vs random projections grid")
    parser.add_argument("--all", action="store_true", help="Show all embedded views side by side")
    parser.add_argument("--text", default="HELLO", help="Text for the intended image (default: HELLO)")
    parser.add_argument("--points", type=int, default=500, help="Points per image (default: 500)")
    parser.add_argument("--dim", type=int, default=256, help="Ambient dimension (default: 256)")
    parser.add_argument("--noise", type=float, default=0.3, help="Noise scale (default: 0.3)")
    args = parser.parse_args()

    anamorph = build_default_anamorph(
        intended_text=args.text,
        n_points=args.points,
        ambient_dim=args.dim,
        noise=args.noise,
    )

    if args.grid:
        view_random_grid(anamorph, n_random=8)
    elif args.all:
        view_all_embedded(anamorph)
    else:
        print("Controls:")
        print("  [Random View]  — jump to a random projection")
        print("  [Hint]         — move 20% closer to the intended view")
        print("  [Reveal]       — jump directly to the intended view")
        print("  [Slider]       — interpolate from random to intended")
        print()
        viewer = AnamorphViewer(anamorph)
        viewer.show()


if __name__ == "__main__":
    main()
