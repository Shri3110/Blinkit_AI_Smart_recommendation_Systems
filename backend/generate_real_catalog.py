import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"), timeout=15.0)

CATEGORIES = [
    "Fruits & Vegetables", "Dairy, Bread & Eggs", "Atta, Rice & Dal", "Oil & Ghee",
    "Masalas & Spices", "Breakfast & Instant Food", "Snacks & Munchies", "Biscuits & Bakery",
    "Chocolates & Desserts", "Tea & Coffee", "Cold Drinks & Juices", "Personal Care",
    "Hair Care", "Skin Care", "Baby Care", "Pet Care", "Cleaning Essentials",
    "Home & Kitchen", "Ice Cream & Frozen Foods", "Health & Wellness", "Stationery",
    "Electronics & Accessories"
]

def generate_real_products_for_category(category_name, product_id_start):
    prompt = f"""
You are an expert in Indian FMCG (Fast Moving Consumer Goods) and the Blinkit/Zepto/Instamart catalogs.
I need EXACTLY 15 REAL, well-known products that exist in India for the category "{category_name}".

CRITICAL RULES:
1. DO NOT invent products or brands. (No "Britannia Face Wash" or "Dove Measuring Cups").
2. Only use real brands (e.g. Amul, Britannia, Haldiram's, Surf Excel, Dove, Maggi, Aashirvaad).
3. Provide realistic weights/sizes (e.g., 1 L, 500 g, 100 g).
4. Provide realistic MRP and Selling Prices in INR (Selling price <= MRP).
5. Output MUST be a JSON list of objects.

JSON Format:
[
  {{
    "product_id": "P_...", (start from {product_id_start} and increment)
    "name": "Full real product name (e.g., Maggi 2-Minute Instant Noodles)",
    "brand": "Real brand name (e.g., Maggi)",
    "category": "{category_name}",
    "subcategory": "Logical subcategory",
    "variant": "Any variant or ''",
    "size": "Weight/Volume",
    "unit": "g, kg, L, ml, piece",
    "mrp": 100,
    "selling_price": 95,
    "discount_percentage": 5,
    "availability": "In Stock",
    "image_url": "https://cdn.grofers.com/app/images/products/full_screen/pro_placeholder.jpg",
    "product_url": "https://blinkit.com/"
  }}
]

Return ONLY the JSON. No markdown, no explanations.
"""
    while True:
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=8192
            )
            response_text = completion.choices[0].message.content.strip()
            
            # Clean up markdown if present
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                if lines[0].startswith("```"): lines = lines[1:]
                if lines[-1].startswith("```"): lines = lines[:-1]
                response_text = '\n'.join(lines)
                
            return json.loads(response_text)
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate limit" in err_str.lower():
                print(f"Rate limited. Sleeping 60s...", flush=True)
                time.sleep(60)
            else:
                print(f"Error generating {category_name}: {e}")
                return []

def main():
    all_products = []
    pid = 1000
    
    for category in CATEGORIES:
        print(f"Generating real products for {category}...", flush=True)
        products = generate_real_products_for_category(category, f"P_{pid}")
        if products:
            all_products.extend(products)
            pid += len(products)
            print(f" -> Added {len(products)} products. Total so far: {len(all_products)}", flush=True)
            
            # Save intermediate
            out_path = "data/real_product_catalog.json"
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(all_products, f, indent=4, ensure_ascii=False)
        time.sleep(2) # Rate limit
        
    out_path = "data/real_product_catalog.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully saved {len(all_products)} verified products to {out_path}.")

if __name__ == "__main__":
    main()
