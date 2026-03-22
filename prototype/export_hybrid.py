#!/usr/bin/env python3
"""
Phase 3 (revised): Hybrid explorer — designed anamorphic forms hidden
inside a real word embedding dataset.

The real word embeddings retain their natural structure. We inject additional
"ghost" points whose 2D structure is designed to be visible ONLY under a
specific concept lens. Under any other projection, they blend in as noise.
"""

import json
import numpy as np
from construct import text_to_points, shape_to_points
from semantic import embed_texts, concept_direction, concept_basis, get_model

# -----------------------------------------------------------------------
# 1. Real word embeddings (same as before)
# -----------------------------------------------------------------------
categories = {
    "animals_domestic": {
        "color": "#ff6b6b",
        "words": ["dog", "cat", "horse", "cow", "sheep", "chicken", "pig", "goat",
                  "rabbit", "hamster", "parrot", "goldfish", "donkey", "duck", "turkey"],
    },
    "animals_wild": {
        "color": "#ee4444",
        "words": ["wolf", "bear", "eagle", "shark", "lion", "tiger", "elephant", "whale",
                  "snake", "spider", "hawk", "dolphin", "crocodile", "panther", "falcon"],
    },
    "food_sweet": {
        "color": "#ffa94d",
        "words": ["cake", "chocolate", "candy", "cookie", "honey", "sugar",
                  "pie", "donut", "caramel", "pudding", "brownie", "muffin", "syrup"],
    },
    "food_savory": {
        "color": "#ff8800",
        "words": ["steak", "burger", "pizza", "sushi", "bacon", "cheese", "bread",
                  "soup", "salad", "pasta", "rice", "curry", "taco", "sandwich"],
    },
    "places_urban": {
        "color": "#74c0fc",
        "words": ["skyscraper", "subway", "highway", "mall", "apartment", "factory",
                  "office", "stadium", "airport", "hospital", "prison",
                  "nightclub", "warehouse"],
    },
    "places_nature": {
        "color": "#4488ff",
        "words": ["forest", "mountain", "ocean", "river", "desert", "meadow", "glacier",
                  "waterfall", "canyon", "island", "volcano", "cave", "swamp", "reef"],
    },
    "professions_physical": {
        "color": "#69db7c",
        "words": ["farmer", "carpenter", "mechanic", "plumber", "firefighter", "soldier",
                  "miner", "sailor", "chef", "blacksmith", "lumberjack", "fisherman"],
    },
    "professions_mental": {
        "color": "#44bb66",
        "words": ["scientist", "professor", "lawyer", "doctor", "engineer", "programmer",
                  "accountant", "philosopher", "mathematician", "psychologist", "architect"],
    },
    "emotions_positive": {
        "color": "#da77f2",
        "words": ["joy", "love", "hope", "peace", "gratitude", "excitement", "pride",
                  "contentment", "delight", "bliss", "serenity", "compassion"],
    },
    "emotions_negative": {
        "color": "#9944cc",
        "words": ["anger", "fear", "sadness", "anxiety", "grief", "hatred", "jealousy",
                  "shame", "guilt", "disgust", "loneliness", "despair"],
    },
    "weather_hot": {
        "color": "#ffd43b",
        "words": ["sunshine", "heatwave", "tropical", "scorching", "humid",
                  "sweltering", "sunburn", "drought", "wildfire"],
    },
    "weather_cold": {
        "color": "#66d9e8",
        "words": ["blizzard", "snowfall", "frost", "icicle", "avalanche",
                  "freezing rain", "glacier ice"],
    },
    "technology": {
        "color": "#aaaaaa",
        "words": ["computer", "robot", "satellite", "laser", "algorithm", "database",
                  "smartphone", "internet", "processor", "software", "circuit", "drone"],
    },
    "music": {
        "color": "#e599f7",
        "words": ["guitar", "piano", "violin", "drums", "trumpet", "flute", "symphony",
                  "jazz", "rock", "opera", "choir", "rhythm", "melody"],
    },
}

# Flatten real words
real_words = []
real_categories = []
real_colors = []
for cat_name, cat_data in categories.items():
    for word in cat_data["words"]:
        real_words.append(word)
        real_categories.append(cat_name)
        real_colors.append(cat_data["color"])

print(f"Embedding {len(real_words)} real words...")
real_embeddings = embed_texts(real_words)
d = real_embeddings.shape[1]
print(f"  Dimension: {d}")

# -----------------------------------------------------------------------
# 2. Define the hidden form's concept subspace
# -----------------------------------------------------------------------
hidden_concepts = [
    (["dangerous", "deadly", "hazardous", "lethal", "toxic"],
     ["safe", "harmless", "gentle", "benign", "secure"]),
    (["ancient", "old", "medieval", "prehistoric", "archaic"],
     ["modern", "new", "futuristic", "contemporary", "innovative"]),
]

print("Computing hidden subspace from concepts:")
print(f"  Axis 1: dangerous/deadly ↔ safe/harmless")
print(f"  Axis 2: ancient/old ↔ modern/new")

hidden_basis = concept_basis(hidden_concepts)  # (d, 2)

# -----------------------------------------------------------------------
# 3. Generate hidden form points in the concept subspace
# -----------------------------------------------------------------------
# The form: the word "DANGER" rendered as points
hidden_2d = text_to_points("DANGER", n_points=800, font_size=80) * 2.5

# Embed into the full space via the concept basis
rng = np.random.default_rng(42)
hidden_embedded = hidden_2d @ hidden_basis.T  # (800, d)

# Add noise in all dimensions (small, so form is visible under correct lens)
hidden_embedded += rng.standard_normal(hidden_embedded.shape) * 0.03

# Shift the hidden points to be near the centroid of the real data
# so they blend in spatially
real_centroid = real_embeddings.mean(axis=0)
hidden_embedded += real_centroid

print(f"  Hidden form: 'DANGER', {len(hidden_2d)} points")

# -----------------------------------------------------------------------
# 4. Combine real + hidden
# -----------------------------------------------------------------------
all_points = np.vstack([real_embeddings, hidden_embedded])
all_words = real_words + [""] * len(hidden_2d)  # ghost points have no label
all_categories = real_categories + ["hidden_form"] * len(hidden_2d)
all_colors = real_colors + ["#ff2222"] * len(hidden_2d)

# Add hidden_form to category colors
cat_colors = {k: v["color"] for k, v in categories.items()}
cat_colors["hidden_form"] = "#ff2222"

print(f"  Total points: {len(all_points)} ({len(real_words)} real + {len(hidden_2d)} hidden)")

# -----------------------------------------------------------------------
# 5. Concept vocabulary for browser
# -----------------------------------------------------------------------
concept_vocab_words = sorted(set([
    "cold", "hot", "warm", "cool", "frozen", "boiling", "freezing", "scorching",
    "icy", "burning", "chilly", "heated", "frigid",
    "natural", "artificial", "organic", "synthetic", "wild", "domestic", "tame",
    "manufactured", "industrial", "mechanical", "biological",
    "physical", "mental", "body", "mind", "intellectual", "manual", "cerebral",
    "muscular", "cognitive", "athletic", "academic",
    "good", "bad", "happy", "sad", "positive", "negative", "pleasant", "unpleasant",
    "beautiful", "ugly", "joyful", "miserable",
    "urban", "rural", "city", "countryside", "metropolitan",
    "wilderness", "downtown", "village", "remote", "crowded",
    "sweet", "savory", "salty", "bitter", "sour", "sugary", "spicy", "bland",
    "loud", "quiet", "noisy", "silent", "peaceful",
    "fast", "slow", "quick", "gradual", "rapid",
    "ancient", "modern", "old", "new", "traditional", "innovative", "classic",
    "contemporary", "medieval", "prehistoric", "archaic", "futuristic",
    "big", "small", "enormous", "tiny", "massive", "miniature",
    "dangerous", "safe", "risky", "secure", "hazardous", "harmless",
    "deadly", "gentle", "lethal", "toxic", "benign",
    "abstract", "concrete", "theoretical", "practical",
]))

print(f"Embedding {len(concept_vocab_words)} concept vocabulary words...")
concept_embeddings = embed_texts(concept_vocab_words)

# -----------------------------------------------------------------------
# 6. Export
# -----------------------------------------------------------------------
data = {
    "ambient_dim": d,
    "n_points": len(all_points),
    "n_real": len(real_words),
    "n_hidden": len(hidden_2d),
    "words": all_words,
    "categories": all_categories,
    "colors": all_colors,
    "category_colors": cat_colors,
    "points": np.round(all_points, 4).tolist(),
    "concept_vocab": concept_vocab_words,
    "concept_embeddings": np.round(concept_embeddings, 5).tolist(),
    "hidden_concepts": [
        {"positive": pos, "negative": neg}
        for pos, neg in hidden_concepts
    ],
    "hidden_basis": np.round(hidden_basis, 6).tolist(),
    "suggested_lenses": [
        {"name": "Temperature", "pos": ["hot", "warm", "burning", "scorching"], "neg": ["cold", "frozen", "freezing", "icy"]},
        {"name": "Wild ↔ Domestic", "pos": ["wild", "dangerous", "natural"], "neg": ["domestic", "tame", "safe"]},
        {"name": "Physical ↔ Mental", "pos": ["physical", "body", "manual"], "neg": ["mental", "mind", "intellectual"]},
        {"name": "Urban ↔ Rural", "pos": ["urban", "city", "crowded"], "neg": ["rural", "wilderness", "remote"]},
        {"name": "Sweet ↔ Savory", "pos": ["sweet", "sugary"], "neg": ["savory", "salty", "spicy"]},
        {"name": "Positive ↔ Negative", "pos": ["good", "happy", "joyful"], "neg": ["bad", "sad", "miserable"]},
        {"name": "Ancient ↔ Modern", "pos": ["ancient", "old", "medieval"], "neg": ["modern", "new", "futuristic"]},
        {"name": "Dangerous ↔ Safe", "pos": ["dangerous", "deadly", "hazardous"], "neg": ["safe", "harmless", "gentle"]},
    ],
}

out_path = "web/explorer_data.json"
with open(out_path, "w") as f:
    json.dump(data, f, separators=(",", ":"))

size_mb = len(json.dumps(data, separators=(",", ":"))) / 1e6
print(f"Exported to {out_path} ({size_mb:.1f} MB)")
print()
print("The hidden form 'DANGER' is visible under the concept lens:")
print("  X: dangerous/deadly ↔ safe/harmless")
print("  Y: ancient/old ↔ modern/new")
print("Other lenses show the real data's natural structure with ghost points as noise.")
