import sqlite3
import json
import random

def main():
    conn = sqlite3.connect('discovery_engine.db')
    cursor = conn.cursor()
    
    # 1. Fetch all products and group by category
    cursor.execute("SELECT id, category, selling_price, raw_json FROM products")
    products = cursor.fetchall()
    
    products_by_cat = {}
    for p in products:
        pid, cat, price, raw = p
        if cat not in products_by_cat:
            products_by_cat[cat] = []
        products_by_cat[cat].append((pid, price, json.loads(raw)))
        
    # 2. Define Persona to Category mapping
    persona_categories = {
        'Parent': ['Baby Care', 'Dairy, Bread & Eggs', 'Cleaning Essentials'],
        'Fitness Enthusiast': ['Fruits & Vegetables', 'Health & Wellness', 'Breakfast & Instant Food'],
        'Pet Owner': ['Pet Care', 'Cleaning Essentials', 'Home & Kitchen'],
        'Student': ['Snacks & Munchies', 'Cold Drinks & Juices', 'Chocolates & Desserts', 'Biscuits & Bakery'],
        'Family Shopper': ['Atta, Rice & Dal', 'Oil & Ghee', 'Masalas & Spices', 'Dairy, Bread & Eggs'],
        'Premium Shopper': ['Skin Care', 'Ice Cream & Frozen Foods', 'Tea & Coffee', 'Personal Care'],
        'Working Professional': ['Breakfast & Instant Food', 'Dairy, Bread & Eggs', 'Personal Care', 'Tea & Coffee'],
        'Budget Shopper': ['Atta, Rice & Dal', 'Snacks & Munchies', 'Cleaning Essentials']
    }
    
    # 3. Process each user
    cursor.execute("SELECT user_id, raw_json FROM users")
    users = cursor.fetchall()
    
    cursor.execute("DELETE FROM purchases")
    print(f"Cleared existing purchases.")
    
    total_purchases_inserted = 0
    
    for u in users:
        user_id = u[0]
        user_data = json.loads(u[1])
        occupation = user_data.get('occupation', 'Student')
        
        target_cats = persona_categories.get(occupation, persona_categories['Student'])
        
        # Decide how many items they bought recently based on monthly orders
        # 12 to 25 items total to populate history
        num_items = random.randint(12, 25)
        
        for i in range(num_items):
            # 85% chance to buy from their target categories, 15% random exploration
            if random.random() < 0.85:
                cat = random.choice(target_cats)
            else:
                cat = random.choice(list(products_by_cat.keys()))
                
            if cat not in products_by_cat or not products_by_cat[cat]:
                continue
                
            product = random.choice(products_by_cat[cat])
            pid, price, prod_json = product
            
            # Format order id
            order_id = f"PUR_{user_id}_{i}"
            
            cursor.execute(
                "INSERT INTO purchases (order_id, user_id, product_id, category, price_paid) VALUES (?, ?, ?, ?, ?)",
                (order_id, user_id, pid, cat, price)
            )
            total_purchases_inserted += 1
            
    conn.commit()
    conn.close()
    
    print(f"Successfully generated {total_purchases_inserted} new purchases aligned with personas.")

if __name__ == "__main__":
    main()
