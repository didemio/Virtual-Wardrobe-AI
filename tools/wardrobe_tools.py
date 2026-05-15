import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "wardrobe.json"

TOOL_DEFINITIONS = [
    {
        "name": "get_all_items",
        "description": "Returns all clothing items currently in the wardrobe.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "filter_by_category",
        "description": "Returns clothing items that belong to a specific category (e.g. 'tops', 'outerwear', 'bottoms').",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "The category name to filter by."}
            },
            "required": ["category"],
        },
    },
    {
        "name": "list_categories",
        "description": "Returns a list of all unique clothing categories in the wardrobe.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "add_item",
        "description": "Adds a new clothing item to the wardrobe.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the clothing item."},
                "category": {"type": "string", "description": "Category of the clothing item."},
            },
            "required": ["name", "category"],
        },
    },
    {
        "name": "remove_item",
        "description": "Removes a clothing item from the wardrobe by its id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "The id of the item to remove."}
            },
            "required": ["id"],
        },
    },
]


def load_wardrobe(filepath=None) -> dict:
    path = Path(filepath) if filepath else DATA_PATH
    if not path.exists():
        return {"clothes": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_by_category(wardrobe: dict, category: str) -> list:
    return [
        item for item in wardrobe.get("clothes", [])
        if item.get("category", "").lower() == category.lower()
    ]


def list_categories(wardrobe: dict) -> list:
    return list({item.get("category", "") for item in wardrobe.get("clothes", [])})


def add_item(wardrobe: dict, name: str, category: str) -> dict:
    clothes = wardrobe.get("clothes", [])
    new_id = max((item["id"] for item in clothes), default=0) + 1
    clothes.append({"id": new_id, "name": name, "category": category})
    wardrobe["clothes"] = clothes
    return wardrobe


def remove_item(wardrobe: dict, item_id: int) -> tuple:
    clothes = wardrobe.get("clothes", [])
    new_clothes = [item for item in clothes if item["id"] != item_id]
    found = len(new_clothes) < len(clothes)
    wardrobe["clothes"] = new_clothes
    return wardrobe, found
