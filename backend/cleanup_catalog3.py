import json
import os

CATALOG_PATH = "data/real_product_catalog.json"

def clean_catalog():
    with open(CATALOG_PATH, "r") as f:
        products = json.load(f)

    count = 0
    for p in products:
        name = p.get("name", "")
        # Haldiram's Fresh Green Chilli -> Fresho Fresh Green Chilli in Fruits & Vegetables
        if "Haldiram" in name and ("Chilli" in name or "Beetroot" in name or "Carrot" in name or "Onion" in name or "Tomato" in name or "Potato" in name):
            p["brand"] = "Fresho"
            p["name"] = name.replace("Haldiram's", "Fresho").replace("Haldiram", "Fresho")
            p["category"] = "Fruits & Vegetables"
            p["subcategory"] = "Fresh Vegetables"
            count += 1
            print(f"Fixed: {p['name']}")
            
    with open(CATALOG_PATH, "w") as f:
        json.dump(products, f, indent=4)
        
    print(f"Total additional fixes applied: {count}")

if __name__ == "__main__":
    clean_catalog()
