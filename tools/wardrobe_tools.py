import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'wardrobe.json')

def load_wardrobe():
    """Load wardrobe data from JSON file."""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_clothes_by_category(category):
    """Get clothes by category."""
    wardrobe = load_wardrobe()
    return [item for item in wardrobe['clothes'] if item['category'] == category]

def suggest_outfit():
    """Suggest a simple outfit."""
    wardrobe = load_wardrobe()
    clothes = wardrobe['clothes']
    if len(clothes) < 2:
        return "Not enough clothes for an outfit."
    # Simple suggestion: pick one from üst and one from dışgiyim if available
    upper = next((c for c in clothes if c['category'] == 'üst'), None)
    outer = next((c for c in clothes if c['category'] == 'dışgiyim'), None)
    if upper and outer:
        return f"Suggested outfit: {upper['name']} with {outer['name']}"
    return "No suitable outfit found."