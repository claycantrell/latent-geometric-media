#!/usr/bin/env python3
"""
Export a semantic-keyed anamorph + word embeddings for the web viewer.

Pre-computes embeddings for a vocabulary of ~200 words so the browser
can compute concept directions without running a transformer model.
"""

import json
import numpy as np
from construct import text_to_points, shape_to_points
from semantic import (
    construct_semantic_anamorph,
    embed_texts,
    get_model,
)

# --- Build the anamorph ---
privileged_concepts = [
    (["cold", "frozen", "ice", "winter", "arctic"], ["warm", "hot", "fire", "summer", "tropical"]),
    (["mechanical", "industrial", "machine", "metal", "robotic"], ["organic", "natural", "living", "plant", "biological"]),
]

intended = ("COLD", text_to_points("COLD", 2000, font_size=90))
decoys = [
    ("spiral", shape_to_points("spiral", 2000)),
    ("triangle", shape_to_points("triangle", 2000)),
]

result = construct_semantic_anamorph(
    intended_image=intended,
    decoy_images=decoys,
    privileged_concepts=privileged_concepts,
    noise_scale=0.05,
    signal_scale=3.0,
    seed=42,
)

anamorph = result["anamorph"]

# --- Build vocabulary with pre-computed embeddings ---
# Include the concept words, plus a broad set for free exploration
vocab_words = sorted(set([
    # Privileged concept words
    "cold", "frozen", "ice", "winter", "arctic", "freezing", "icy", "frost", "snow", "glacier",
    "warm", "hot", "fire", "summer", "tropical", "boiling", "scorching", "heat", "burning", "lava",
    "mechanical", "industrial", "machine", "metal", "robotic", "engine", "gear", "steel", "automated", "factory",
    "organic", "natural", "living", "plant", "biological", "alive", "growing", "forest", "tree", "flower",
    # Temperature / weather
    "cool", "chilly", "frigid", "mild", "temperate", "humid", "dry", "rain", "storm", "wind",
    # Materials / textures
    "wood", "stone", "glass", "plastic", "ceramic", "concrete", "rubber", "fabric", "leather", "paper",
    # Emotions / abstract
    "happy", "sad", "angry", "calm", "peaceful", "chaotic", "beautiful", "ugly", "fast", "slow",
    "loud", "quiet", "bright", "dark", "heavy", "light", "hard", "soft", "rough", "smooth",
    # Science / tech
    "digital", "analog", "electric", "magnetic", "quantum", "atomic", "chemical", "nuclear", "solar", "cosmic",
    "computer", "robot", "algorithm", "data", "network", "signal", "circuit", "laser", "crystal", "pixel",
    # Nature
    "ocean", "mountain", "river", "desert", "jungle", "meadow", "volcano", "island", "cave", "sky",
    "animal", "bird", "fish", "insect", "wolf", "bear", "eagle", "whale", "snake", "spider",
    # Human / social
    "city", "village", "home", "school", "hospital", "church", "market", "prison", "castle", "bridge",
    "king", "queen", "soldier", "artist", "scientist", "teacher", "doctor", "farmer", "musician", "writer",
    # Food / sensory
    "sweet", "bitter", "sour", "salty", "spicy", "fresh", "rotten", "crisp", "juicy", "bland",
    # Colors
    "red", "blue", "green", "yellow", "black", "white", "purple", "orange", "silver", "gold",
    # Actions
    "build", "destroy", "create", "break", "grow", "shrink", "push", "pull", "open", "close",
    # Misc useful
    "ancient", "modern", "future", "past", "present", "new", "old", "big", "small", "tiny",
    "democracy", "monarchy", "freedom", "control", "order", "chaos", "war", "peace", "love", "hate",
    "guitar", "piano", "drum", "violin", "trumpet",
]))

print(f"Embedding {len(vocab_words)} vocabulary words...")
embeddings = embed_texts(vocab_words)  # (n_words, 384)
print(f"Embeddings shape: {embeddings.shape}")

# --- Export ---
data = {
    "ambient_dim": anamorph.ambient_dim,
    "n_points": len(anamorph.points),
    "n_images": len(anamorph.bases),
    "labels": anamorph.labels,
    "privileged_index": anamorph.privileged_index,
    "points": np.round(anamorph.points, 4).tolist(),
    "bases": [np.round(b, 6).tolist() for b in anamorph.bases],
    "privileged_concepts": [
        {"positive": pos, "negative": neg}
        for pos, neg in privileged_concepts
    ],
    "vocab": vocab_words,
    "word_embeddings": np.round(embeddings, 5).tolist(),
}

out_path = "web/semantic_data.json"
with open(out_path, "w") as f:
    json.dump(data, f, separators=(",", ":"))

size_mb = len(json.dumps(data, separators=(",", ":"))) / 1e6
print(f"Exported to {out_path} ({size_mb:.1f} MB)")
