import json
import os

CATALOG_PATH = "data/real_product_catalog.json"

def clean_catalog():
    with open(CATALOG_PATH, "r") as f:
        products = json.load(f)

    # Categories where Amul makes sense
    amul_categories = [
        "Dairy, Bread & Eggs",
        "Ice Cream & Frozen Foods",
        "Chocolates & Desserts",
        "Health & Wellness", # Protein powder
        "Breakfast & Instant Food"
    ]
    
    # We will replace Amul with generic realistic brands for other categories
    replacements = {
        "Fruits & Vegetables": "Fresho",
        "Oil & Ghee": {
            "Ghee": "Amul", # Amul makes Ghee
            "Coconut Oil": "Parachute",
            "Olive Oil": "Figaro",
            "Vegetable Oil": "Fortune"
        },
        "Biscuits & Bakery": "Britannia",
        "Home & Kitchen": "Local"
    }

    count = 0
    for p in products:
        if p.get("brand") == "Amul":
            cat = p.get("category")
            if cat not in amul_categories:
                # Need to replace brand and name
                subcat = p.get("subcategory", "")
                
                new_brand = "Fresho"
                if cat in replacements:
                    if isinstance(replacements[cat], dict):
                        new_brand = replacements[cat].get(subcat, "Fortune")
                    else:
                        new_brand = replacements[cat]
                
                # Special cases
                if new_brand == "Amul": 
                    continue # Valid

                # Also replace 'Amul ' in the product name
                if p["name"].startswith("Amul "):
                    p["name"] = p["name"].replace("Amul ", f"{new_brand} ", 1)
                
                p["brand"] = new_brand
                count += 1
                print(f"Fixed: {p['name']} (Brand: {new_brand})")

    with open(CATALOG_PATH, "w") as f:
        json.dump(products, f, indent=4)
        
    print(f"Total fixes applied: {count}")

if __name__ == "__main__":
    clean_catalog()
