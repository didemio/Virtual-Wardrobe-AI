from tools.wardrobe_tools import load_wardrobe, suggest_outfit

def main():
    print("Welcome to Virtual Wardrobe AI!")
    wardrobe = load_wardrobe()
    print(f"Your wardrobe has {len(wardrobe['clothes'])} items.")
    print(suggest_outfit())

if __name__ == "__main__":
    main()