import json
import os

CATALOG_PATH = "data/real_product_catalog.json"

def clean_catalog():
    with open(CATALOG_PATH, "r") as f:
        products = json.load(f)

    count = 0
    for p in products:
        # Fix Britannia Good Day and other biscuits in wrong categories
        if "Biscuit" in p.get("name", "") or "Cookies" in p.get("name", "") or p.get("brand") == "Britannia":
            if p.get("category") != "Biscuits & Bakery":
                # Except if it's dairy/cheese by Britannia
                if "Cheese" not in p.get("name", "") and "Milk" not in p.get("name", "") and "Butter" not in p.get("name", "") or "Butter Biscuit" in p.get("name", ""):
                    p["category"] = "Biscuits & Bakery"
                    p["subcategory"] = "Biscuits"
                    count += 1
                    print(f"Fixed category for: {p['name']}")
                    
        # Fix Haldiram's in Fruits & Vegetables
        if p.get("brand") == "Haldiram's" and p.get("category") == "Fruits & Vegetables":
            p["category"] = "Snacks & Munchies"
            p["subcategory"] = "Namkeen"
            count += 1
            print(f"Fixed category for: {p['name']}")
            
        # Fix Dhani in Fruits & Vegetables
        if p.get("brand") == "Dhani" and p.get("category") == "Fruits & Vegetables":
            p["brand"] = "Fresho"
            count += 1
            print(f"Fixed brand for: {p['name']}")

    with open(CATALOG_PATH, "w") as f:
        json.dump(products, f, indent=4)
        
    print(f"Total additional fixes applied: {count}")

if __name__ == "__main__":
    clean_catalog()
