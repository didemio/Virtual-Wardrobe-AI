import unittest
from tools.wardrobe_tools import load_wardrobe, get_clothes_by_category

class TestWardrobeTools(unittest.TestCase):
    def test_load_wardrobe(self):
        wardrobe = load_wardrobe()
        self.assertIn('clothes', wardrobe)
        self.assertGreater(len(wardrobe['clothes']), 0)

    def test_get_clothes_by_category(self):
        clothes = get_clothes_by_category('üst')
        self.assertGreater(len(clothes), 0)
        for item in clothes:
            self.assertEqual(item['category'], 'üst')

if __name__ == '__main__':
    unittest.main()