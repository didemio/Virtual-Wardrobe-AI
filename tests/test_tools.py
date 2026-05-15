import unittest
from tools.wardrobe_tools import (
    filter_by_category,
    list_categories,
    add_item,
    remove_item,
)
import copy

SAMPLE_WARDROBE = {
    "clothes": [
        {"id": 1, "name": "Winter Coat", "category": "outerwear"},
        {"id": 2, "name": "White T-shirt", "category": "tops"},
        {"id": 3, "name": "Sweater", "category": "tops"},
        {"id": 4, "name": "Blue Jeans", "category": "bottoms"},
    ]
}

def w():
    return copy.deepcopy(SAMPLE_WARDROBE)

class TestWardrobeTools(unittest.TestCase):

    def test_filter_returns_matching_items(self):
        result = filter_by_category(w(), "tops")
        self.assertEqual(len(result), 2)
        for item in result:
            self.assertEqual(item["category"], "tops")

    def test_filter_case_insensitive(self):
        result = filter_by_category(w(), "TOPS")
        self.assertEqual(len(result), 2)

    def test_filter_no_match_returns_empty(self):
        result = filter_by_category(w(), "shoes")
        self.assertEqual(result, [])

    def test_list_categories_unique(self):
        result = list_categories(w())
        self.assertEqual(sorted(result), sorted(["outerwear", "tops", "bottoms"]))

    def test_list_categories_empty_wardrobe(self):
        result = list_categories({"clothes": []})
        self.assertEqual(result, [])

    def test_add_item_increases_count(self):
        updated = add_item(w(), "Shirt", "tops")
        self.assertEqual(len(updated["clothes"]), 5)

    def test_add_item_unique_ids(self):
        updated = add_item(w(), "Sneakers", "shoes")
        ids = [item["id"] for item in updated["clothes"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_add_item_correct_data(self):
        updated = add_item(w(), "Baseball Cap", "accessories")
        last = updated["clothes"][-1]
        self.assertEqual(last["name"], "Baseball Cap")
        self.assertEqual(last["category"], "accessories")

    def test_remove_item_decreases_count(self):
        updated, success = remove_item(w(), 1)
        self.assertTrue(success)
        self.assertEqual(len(updated["clothes"]), 3)

    def test_remove_nonexistent_returns_false(self):
        updated, success = remove_item(w(), 999)
        self.assertFalse(success)
        self.assertEqual(len(updated["clothes"]), 4)

    def test_remove_correct_item(self):
        updated, _ = remove_item(w(), 2)
        ids = [item["id"] for item in updated["clothes"]]
        self.assertNotIn(2, ids)

if __name__ == "__main__":
    unittest.main()
