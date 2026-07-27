import sqlite3
import json
import os
import random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(os.path.dirname(__file__), "discovery_engine.db")

def migrate():
    print("Loading Old Catalog for category mapping...")
    with open(os.path.join(DATA_DIR, "product_catalog.json"), "r", encoding="utf-8") as f:
        old_products = json.load(f)
    old_id_to_cat = {p["id"]: p["category"] for p in old_products}

    print("Loading New Real Catalog...")
    with open(os.path.join(DATA_DIR, "real_product_catalog.json"), "r", encoding="utf-8") as f:
        products = json.load(f)
        
    category_map = {}
    for p in products:
        cat = p["category"]
        if cat not in category_map:
            category_map[cat] = []
        category_map[cat].append(p)
        
    print("Remapping Purchase History...")
    with open(os.path.join(DATA_DIR, "purchase_history.json"), "r", encoding="utf-8") as f:
        purchases = json.load(f)
        
    for p in purchases:
        # p["category"] might already be in the purchase record, but let's be safe
        cat = p.get("category")
        if not cat:
            cat = old_id_to_cat.get(p["product_id"])
            
        if cat in category_map and category_map[cat]:
            real_prod = random.choice(category_map[cat])
            p["product_id"] = real_prod["product_id"]
            p["category"] = real_prod["category"]
            p["price_paid"] = real_prod["selling_price"]
            
    with open(os.path.join(DATA_DIR, "purchase_history.json"), "w", encoding="utf-8") as f:
        json.dump(purchases, f, indent=4)
        
    print("Remapping Carts...")
    with open(os.path.join(DATA_DIR, "current_cart.json"), "r", encoding="utf-8") as f:
        carts = json.load(f)
        
    for c in carts:
        total_value = 0
        for item in c["cart_items"]:
            old_id = item["product_id"]
            cat = old_id_to_cat.get(old_id, "Dairy, Bread & Eggs") # fallback
            
            if cat in category_map and category_map[cat]:
                real_prod = random.choice(category_map[cat])
                item["product_id"] = real_prod["product_id"]
                price = real_prod["selling_price"]
            else:
                price = 100
                
            total_value += price * item["quantity"]
        c["cart_value"] = total_value
        
    with open(os.path.join(DATA_DIR, "current_cart.json"), "w", encoding="utf-8") as f:
        json.dump(carts, f, indent=4)

    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            brand TEXT,
            category TEXT,
            subcategory TEXT,
            selling_price REAL,
            image_url TEXT,
            raw_json TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            occupation TEXT,
            raw_json TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            order_id TEXT PRIMARY KEY,
            user_id TEXT,
            product_id TEXT,
            category TEXT,
            price_paid REAL,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            cart_id TEXT PRIMARY KEY,
            user_id TEXT,
            cart_value REAL,
            raw_json TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    # Clear existing data
    cursor.execute('DELETE FROM carts')
    cursor.execute('DELETE FROM purchases')
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM products')

    print("Inserting Products to DB...")
    for p in products:
        pid = p.get("product_id", p.get("id"))
        p["id"] = pid 
        cursor.execute('''
            INSERT INTO products (id, name, brand, category, subcategory, selling_price, image_url, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (pid, p["name"], p["brand"], p["category"], p["subcategory"], p["selling_price"], p.get("image_url", ""), json.dumps(p)))

    print("Inserting Users to DB...")
    with open(os.path.join(DATA_DIR, "customer_profiles.json"), "r", encoding="utf-8") as f:
        users = json.load(f)
        for u in users:
            cursor.execute('''
                INSERT INTO users (user_id, name, age, occupation, raw_json)
                VALUES (?, ?, ?, ?, ?)
            ''', (u["user_id"], u["name"], u["age"], u["occupation"], json.dumps(u)))

    print("Inserting Purchases to DB...")
    for p in purchases:
        cursor.execute('''
            INSERT INTO purchases (order_id, user_id, product_id, category, price_paid)
            VALUES (?, ?, ?, ?, ?)
        ''', (p["order_id"], p["user_id"], p["product_id"], p["category"], p["price_paid"]))

    print("Inserting Carts to DB...")
    for c in carts:
        cursor.execute('''
            INSERT INTO carts (cart_id, user_id, cart_value, raw_json)
            VALUES (?, ?, ?, ?)
        ''', (c["cart_id"], c["user_id"], c["cart_value"], json.dumps(c)))

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
