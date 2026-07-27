import os
import json
import time
import uuid
import re
from duckduckgo_search import DDGS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

CATEGORIES = [
    "Fruits & Vegetables", "Dairy, Bread & Eggs", "Atta, Rice & Dal", "Oil & Ghee",
    "Masalas & Spices", "Breakfast & Instant Food", "Snacks & Munchies", "Biscuits & Bakery",
    "Chocolates & Desserts", "Tea & Coffee", "Cold Drinks & Juices", "Personal Care",
    "Hair Care", "Skin Care", "Baby Care", "Pet Care", "Cleaning Essentials",
    "Home & Kitchen", "Ice Cream & Frozen Foods", "Health & Wellness", "Stationery"
]

def search_blinkit_category(category_name):
    query = f'site:blinkit.com/prn "₹" "{category_name}"'
    print(f"Searching: {category_name}")
    snippets = []
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=40)
            for r in results:
                snippets.append({
                    "title": r.get("title", ""),
                    "body": r.get("body", ""),
                    "href": r.get("href", "")
                })
    except Exception as e:
        print(f"Search error for {category_name}: {e}")
    return snippets

def parse_snippets_with_groq(category_name, snippets):
    if not snippets:
        return []
        
    prompt = f"""
You are an expert FMCG data extractor. I will give you a JSON list of search results from blinkit.com for the category "{category_name}".
Your task is to extract real product details ONLY from these snippets. 
DO NOT invent or guess any products. If a snippet does not contain a clear product name, brand, weight/volume, and price, SKIP IT.

Extract into a JSON list of objects with EXACTLY these keys:
"product_id": (Generate a unique ID starting with P_, e.g. P_801)
"name": (Exact name from snippet)
"brand": (Extract brand from name)
"category": "{category_name}"
"subcategory": (Infer logical subcategory)
"variant": (e.g., "Toned", "Spicy", if applicable, else "")
"size": (Extract weight/volume from snippet, e.g. "10 kg", "500 ml")
"unit": (e.g. "kg", "ml", "g", "piece")
"mrp": (Extract price in INR as integer. If only one price is visible, use it for both mrp and selling_price)
"selling_price": (Extract selling price as integer)
"discount_percentage": (Calculate if MRP > Selling Price, else 0)
"availability": "In Stock"
"image_url": "https://cdn.grofers.com/app/images/products/full_screen/pro_placeholder.jpg"
"product_url": (The exact href from the snippet)

Return ONLY valid JSON wrapped in ```json ... ```. 
Snippets:
{json.dumps(snippets, indent=2)}
"""
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        response_text = completion.choices[0].message.content
        # Extract json between ```json ... ```
        match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        else:
            # Fallback direct parse
            return json.loads(response_text)
    except Exception as e:
        print(f"Groq parsing error for {category_name}: {e}")
        return []

def main():
    all_products = []
    
    for category in CATEGORIES:
        snippets = search_blinkit_category(category)
        if snippets:
            products = parse_snippets_with_groq(category, snippets)
            all_products.extend(products)
            print(f"Added {len(products)} products for {category}. Total: {len(all_products)}")
        time.sleep(2) # Prevent DDG rate limits
        
    # Generate completely unique IDs
    for i, p in enumerate(all_products):
        p["product_id"] = f"P_{1000 + i}"
        
    out_path = "data/real_product_catalog.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully saved {len(all_products)} verified products to {out_path}.")

if __name__ == "__main__":
    main()
