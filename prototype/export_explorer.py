#!/usr/bin/env python3
"""
Phase 3: Export real word embeddings for the concept-lens explorer.

Embeds ~400 categorized words and exports them with the full vocabulary
embeddings for concept-direction computation in the browser.
"""

import json
import numpy as np
from semantic import embed_texts, get_model

# --- Categorized word dataset ---
# Each category has a name, color, and list of words
categories = {
    "animals_domestic": {
        "color": "#ff6b6b",
        "words": [
            "dog", "cat", "horse", "cow", "sheep", "chicken", "pig", "goat",
            "rabbit", "hamster", "parrot", "goldfish", "donkey", "duck", "turkey",
        ],
    },
    "animals_wild": {
        "color": "#ee4444",
        "words": [
            "wolf", "bear", "eagle", "shark", "lion", "tiger", "elephant", "whale",
            "snake", "spider", "hawk", "dolphin", "crocodile", "panther", "falcon",
        ],
    },
    "food_sweet": {
        "color": "#ffa94d",
        "words": [
            "cake", "chocolate", "candy", "cookie", "ice cream", "honey", "sugar",
            "pie", "donut", "caramel", "pudding", "brownie", "muffin", "syrup",
        ],
    },
    "food_savory": {
        "color": "#ff8800",
        "words": [
            "steak", "burger", "pizza", "sushi", "bacon", "cheese", "bread",
            "soup", "salad", "pasta", "rice", "curry", "taco", "sandwich",
        ],
    },
    "places_urban": {
        "color": "#74c0fc",
        "words": [
            "skyscraper", "subway", "highway", "mall", "apartment", "factory",
            "office", "stadium", "airport", "hospital", "prison", "parking lot",
            "nightclub", "warehouse", "bus stop",
        ],
    },
    "places_nature": {
        "color": "#4488ff",
        "words": [
            "forest", "mountain", "ocean", "river", "desert", "meadow", "glacier",
            "waterfall", "canyon", "island", "volcano", "cave", "swamp", "reef",
            "prairie",
        ],
    },
    "professions_physical": {
        "color": "#69db7c",
        "words": [
            "farmer", "carpenter", "mechanic", "plumber", "firefighter", "soldier",
            "miner", "sailor", "chef", "blacksmith", "lumberjack", "fisherman",
            "bricklayer", "welder",
        ],
    },
    "professions_mental": {
        "color": "#44bb66",
        "words": [
            "scientist", "professor", "lawyer", "doctor", "engineer", "programmer",
            "accountant", "philosopher", "mathematician", "psychologist", "architect",
            "analyst", "researcher", "economist",
        ],
    },
    "emotions_positive": {
        "color": "#da77f2",
        "words": [
            "joy", "love", "hope", "peace", "gratitude", "excitement", "pride",
            "contentment", "amusement", "delight", "bliss", "serenity", "euphoria",
            "compassion",
        ],
    },
    "emotions_negative": {
        "color": "#9944cc",
        "words": [
            "anger", "fear", "sadness", "anxiety", "grief", "hatred", "jealousy",
            "shame", "guilt", "disgust", "loneliness", "despair", "frustration",
            "resentment",
        ],
    },
    "weather_hot": {
        "color": "#ffd43b",
        "words": [
            "sunshine", "heatwave", "desert sun", "tropical", "scorching", "humid",
            "sweltering", "sunburn", "drought", "wildfire", "summer heat",
        ],
    },
    "weather_cold": {
        "color": "#66d9e8",
        "words": [
            "blizzard", "snowfall", "frost", "icicle", "avalanche", "frozen lake",
            "polar wind", "hailstorm", "winter storm", "freezing rain", "glacier ice",
        ],
    },
    "technology": {
        "color": "#aaaaaa",
        "words": [
            "computer", "robot", "satellite", "laser", "algorithm", "database",
            "smartphone", "internet", "processor", "software", "circuit", "antenna",
            "server", "drone",
        ],
    },
    "music": {
        "color": "#e599f7",
        "words": [
            "guitar", "piano", "violin", "drums", "trumpet", "flute", "symphony",
            "jazz", "rock", "opera", "choir", "rhythm", "melody", "harmony",
        ],
    },
}

# Flatten
all_words = []
all_categories = []
all_colors = []
cat_names = []

for cat_name, cat_data in categories.items():
    for word in cat_data["words"]:
        all_words.append(word)
        all_categories.append(cat_name)
        all_colors.append(cat_data["color"])
    if cat_name not in cat_names:
        cat_names.append(cat_name)

print(f"Embedding {len(all_words)} words across {len(categories)} categories...")
embeddings = embed_texts(all_words)
print(f"Embeddings shape: {embeddings.shape}")

# Also build the concept vocabulary (reuse from semantic export + add new words)
concept_vocab_words = sorted(set([
    # Temperature
    "cold", "hot", "warm", "cool", "frozen", "boiling", "freezing", "scorching",
    "icy", "burning", "chilly", "heated", "tepid", "frigid",
    # Nature vs artificial
    "natural", "artificial", "organic", "synthetic", "wild", "domestic", "tame",
    "manufactured", "handmade", "industrial", "mechanical", "biological",
    # Physical vs mental
    "physical", "mental", "body", "mind", "intellectual", "manual", "cerebral",
    "muscular", "cognitive", "athletic", "academic", "thoughtful",
    # Positive vs negative
    "good", "bad", "happy", "sad", "positive", "negative", "pleasant", "unpleasant",
    "beautiful", "ugly", "wonderful", "terrible", "joyful", "miserable",
    # Urban vs rural
    "urban", "rural", "city", "countryside", "metropolitan", "pastoral",
    "suburban", "wilderness", "downtown", "village", "remote", "crowded",
    # Sweet vs savory
    "sweet", "savory", "salty", "bitter", "sour", "sugary", "spicy", "bland",
    "rich", "plain", "tangy", "umami",
    # Loud vs quiet
    "loud", "quiet", "noisy", "silent", "booming", "hushed", "thunderous", "peaceful",
    # Fast vs slow
    "fast", "slow", "quick", "gradual", "rapid", "leisurely", "instant", "prolonged",
    # Old vs new
    "ancient", "modern", "old", "new", "traditional", "innovative", "classic", "contemporary",
    # Big vs small
    "big", "small", "enormous", "tiny", "massive", "miniature", "vast", "compact",
    # Dangerous vs safe
    "dangerous", "safe", "risky", "secure", "hazardous", "harmless", "deadly", "gentle",
    # Abstract vs concrete
    "abstract", "concrete", "theoretical", "practical", "conceptual", "tangible",
]))

print(f"Embedding {len(concept_vocab_words)} concept vocabulary words...")
concept_embeddings = embed_texts(concept_vocab_words)

# --- Export ---
data = {
    "ambient_dim": int(embeddings.shape[1]),
    "n_points": len(all_words),
    "words": all_words,
    "categories": all_categories,
    "colors": all_colors,
    "category_names": list(categories.keys()),
    "category_colors": {k: v["color"] for k, v in categories.items()},
    "points": np.round(embeddings, 4).tolist(),
    "concept_vocab": concept_vocab_words,
    "concept_embeddings": np.round(concept_embeddings, 5).tolist(),
    "suggested_lenses": [
        {
            "name": "Temperature",
            "pos": ["hot", "warm", "burning", "scorching"],
            "neg": ["cold", "frozen", "freezing", "icy"],
        },
        {
            "name": "Wild ↔ Domestic",
            "pos": ["wild", "dangerous", "natural"],
            "neg": ["domestic", "tame", "safe"],
        },
        {
            "name": "Physical ↔ Mental",
            "pos": ["physical", "body", "manual", "muscular"],
            "neg": ["mental", "mind", "intellectual", "cerebral"],
        },
        {
            "name": "Urban ↔ Rural",
            "pos": ["urban", "city", "metropolitan", "crowded"],
            "neg": ["rural", "countryside", "wilderness", "remote"],
        },
        {
            "name": "Sweet ↔ Savory",
            "pos": ["sweet", "sugary"],
            "neg": ["savory", "salty", "spicy"],
        },
        {
            "name": "Positive ↔ Negative",
            "pos": ["good", "happy", "beautiful", "joyful"],
            "neg": ["bad", "sad", "ugly", "miserable"],
        },
        {
            "name": "Ancient ↔ Modern",
            "pos": ["ancient", "old", "traditional", "classic"],
            "neg": ["modern", "new", "innovative", "contemporary"],
        },
    ],
}

out_path = "web/explorer_data.json"
with open(out_path, "w") as f:
    json.dump(data, f, separators=(",", ":"))

size_mb = len(json.dumps(data, separators=(",", ":"))) / 1e6
print(f"Exported {len(all_words)} words + {len(concept_vocab_words)} concept vocab to {out_path} ({size_mb:.1f} MB)")
