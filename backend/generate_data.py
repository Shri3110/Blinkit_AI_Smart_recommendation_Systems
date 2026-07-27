import json
import random
import uuid
from datetime import datetime, timedelta

# Configuration
NUM_PRODUCTS = 2000
NUM_CUSTOMERS = 1000
NUM_PURCHASES = 20000
DATA_DIR = "data"

categories = {
    "Staples": ["Atta", "Rice", "Dal", "Oil", "Salt", "Sugar"],
    "Dairy & Breakfast": ["Milk", "Bread", "Butter", "Cheese", "Cereal", "Eggs"],
    "Snacks & Munchies": ["Chips", "Biscuits", "Namkeen", "Popcorn", "Chocolates"],
    "Cold Drinks & Juices": ["Cola", "Juice", "Energy Drink", "Water", "Soda"],
    "Fresh Vegetables": ["Onion", "Potato", "Tomato", "Carrot", "Spinach"],
    "Fresh Fruits": ["Apple", "Banana", "Mango", "Orange", "Grapes"],
    "Personal Care": ["Soap", "Shampoo", "Toothpaste", "Deodorant", "Face Wash"],
    "Home Care": ["Detergent", "Dishwash", "Floor Cleaner", "Tissue", "Repellent"],
    "Baby Care": ["Diapers", "Baby Wipes", "Baby Powder", "Baby Oil", "Baby Food"],
    "Pet Care": ["Dog Food", "Cat Food", "Pet Shampoo", "Treats", "Litter"],
    "Electronics": ["Batteries", "Earphones", "Charger", "Cable", "Power Bank"],
    "Stationery": ["Pen", "Notebook", "Pencil", "Tape", "Marker"],
    "Fitness & Sports": ["Yoga Mat", "Protein Bar", "Shaker", "Skipping Rope"],
    "Kitchenware": ["Baking Mat", "Spatula", "Measuring Cups", "Container"]
}

brands = ["Aashirvaad", "Fortune", "Amul", "Britannia", "Lays", "Coca-Cola", "Surf Excel", "Vim", "Colgate", "Dove", "Pampers", "Johnson's", "Pedigree", "Whiskas", "Duracell", "Boat", "Classmate", "Reynolds", "Kellogg's", "Maggi", "Tropicana", "Dabur", "Tata", "Haldiram's", "Parle"]

def generate_products():
    products = []
    cat_keys = list(categories.keys())
    for i in range(NUM_PRODUCTS):
        cat = random.choice(cat_keys)
        subcat = random.choice(categories[cat])
        brand = random.choice(brands)
        mrp = random.randint(20, 1000)
        discount = random.randint(0, 30)
        selling_price = int(mrp * (1 - discount / 100))
        
        product = {
            "id": f"P_{i+1:05d}",
            "sku": f"SKU_{brand[:3].upper()}_{i+1:05d}",
            "name": f"{brand} {subcat} Variant {random.randint(1,5)}",
            "brand": brand,
            "category": cat,
            "subcategory": subcat,
            "variant": f"Variant {random.randint(1,5)}",
            "size": random.choice(["100g", "500g", "1kg", "1L", "500ml", "1 Pack"]),
            "unit": random.choice(["g", "kg", "L", "ml", "pack"]),
            "mrp": mrp,
            "selling_price": selling_price,
            "discount_percentage": discount,
            "rating": round(random.uniform(3.0, 5.0), 1),
            "review_count": random.randint(10, 5000),
            "availability": random.random() > 0.05,
            "stock_status": random.choice(["In Stock", "In Stock", "Low Stock", "Out of Stock"]),
            "bestseller": random.random() > 0.8,
            "new_arrival": random.random() > 0.9,
            "trending": random.random() > 0.85,
            "seasonality": random.choice(["All Season", "Summer", "Winter", "Monsoon"]),
            "diet_type": random.choice(["Vegetarian", "Vegetarian", "Vegan", "Non-Vegetarian"]),
            "lifestyle_tags": [random.choice(["Healthy", "Organic", "Premium", "Budget", "Gluten-Free"])],
            "cross_sell_categories": random.sample(cat_keys, k=2),
            "frequently_bought_with": [], # populated later
            "image_url": f"https://example.com/img_{i+1}.jpg",
            "product_url": f"https://example.com/product_{i+1}"
        }
        products.append(product)
    
    # Populate frequently bought with
    for p in products:
        p["frequently_bought_with"] = random.sample([x["id"] for x in products], k=random.randint(1, 4))
        
    return products

def generate_customers():
    customers = []
    cat_keys = list(categories.keys())
    personas = ["Students", "Working Professionals", "Families", "Parents", "Pet Owners", "Fitness Enthusiasts", "Budget Shoppers", "Premium Shoppers", "Senior Citizens"]
    for i in range(NUM_CUSTOMERS):
        customers.append({
            "user_id": f"U_{i+1:04d}",
            "name": f"User {i+1}",
            "age": random.randint(18, 70),
            "gender": random.choice(["Male", "Female", "Other"]),
            "city": random.choice(["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune"]),
            "occupation": random.choice(personas),
            "household_type": random.choice(["Single", "Couple", "Nuclear Family", "Joint Family"]),
            "monthly_income": random.choice(["Low", "Medium", "High"]),
            "shopping_frequency": random.choice(["Daily", "Weekly", "Monthly", "Occasionally"]),
            "preferred_categories": random.sample(cat_keys, k=random.randint(2, 5)),
            "preferred_brands": random.sample(brands, k=random.randint(1, 4)),
            "budget_level": random.choice(["Budget", "Standard", "Premium"]),
            "shopping_motivation": random.choice(["Convenience", "Discounts", "Quality", "Variety"]),
            "discovery_behavior": random.choice(["High", "Medium", "Low"]),
            "discount_sensitivity": round(random.uniform(0.1, 1.0), 2),
            "trust_score": random.randint(50, 100),
            "exploration_score": random.randint(10, 90),
            "loyalty_score": random.randint(0, 100),
            "average_order_value": random.randint(200, 2000),
            "average_order_frequency": random.randint(1, 15),
            "preferred_delivery_slot": random.choice(["Morning", "Afternoon", "Evening", "Night"]),
            "created_at": (datetime.now() - timedelta(days=random.randint(10, 365))).isoformat()
        })
    return customers

def generate_purchases(customers, products):
    purchases = []
    for i in range(NUM_PURCHASES):
        customer = random.choice(customers)
        product = random.choice(products)
        qty = random.randint(1, 5)
        price_paid = product["selling_price"] * qty
        order_date = datetime.now() - timedelta(days=random.randint(1, 100))
        
        purchases.append({
            "order_id": f"O_{i+1:06d}",
            "user_id": customer["user_id"],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "order_time": f"{random.randint(8,22):02d}:{random.randint(0,59):02d}",
            "product_id": product["id"],
            "quantity": qty,
            "price_paid": price_paid,
            "discount_received": (product["mrp"] - product["selling_price"]) * qty,
            "payment_method": random.choice(["UPI", "Card", "Wallet", "COD"]),
            "delivery_time": f"{random.randint(10, 45)} mins",
            "category": product["category"],
            "subcategory": product["subcategory"],
            "shopping_mission": random.choice(["Weekly groceries", "Daily milk", "Household refills", "Snacks"]),
            "repeat_purchase": random.random() > 0.5,
            "order_value": price_paid + random.randint(0, 500) # Total order value would be higher
        })
    return purchases

def generate_carts(customers, products):
    carts = []
    for i, c in enumerate(customers):
        cart_items = random.sample(products, k=random.randint(2, 10))
        cat_pool = set(list(categories.keys()))
        pref_cats = set(c["preferred_categories"])
        unexplored = list(cat_pool - pref_cats)
        
        recommended_cat = random.choice(unexplored) if unexplored else random.choice(list(cat_pool))
        rec_products = [p for p in products if p["category"] == recommended_cat]
        recommended_prod = random.choice(rec_products) if rec_products else random.choice(products)
        
        carts.append({
            "cart_id": f"C_{i+1:04d}",
            "user_id": c["user_id"],
            "cart_items": [{"product_id": p["id"], "quantity": random.randint(1,3)} for p in cart_items],
            "cart_value": sum([p["selling_price"] for p in cart_items]),
            "time_of_day": random.choice(["Morning", "Afternoon", "Evening"]),
            "day_of_week": random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
            "shopping_mission": random.choice(["Weekly groceries", "Party prep", "Breakfast restock"]),
            "recommended_category": recommended_cat,
            "recommended_product": recommended_prod["id"],
            "recommendation_reason": f"You frequently purchase {c['preferred_categories'][0]}. Customers with similar shopping habits also enjoy {recommended_cat}.",
            "user_action": random.choice(["Added", "Skipped", "Pending"]),
            "checkout_status": "Active"
        })
    return carts

if __name__ == "__main__":
    import os
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print("Generating products...")
    products = generate_products()
    with open(f"{DATA_DIR}/product_catalog.json", "w") as f:
        json.dump(products, f, indent=2)
        
    print("Generating customers...")
    customers = generate_customers()
    with open(f"{DATA_DIR}/customer_profiles.json", "w") as f:
        json.dump(customers, f, indent=2)
        
    print("Generating purchases...")
    purchases = generate_purchases(customers, products)
    with open(f"{DATA_DIR}/purchase_history.json", "w") as f:
        json.dump(purchases, f, indent=2)
        
    print("Generating carts...")
    carts = generate_carts(customers, products)
    with open(f"{DATA_DIR}/current_cart.json", "w") as f:
        json.dump(carts, f, indent=2)
        
    print("Data generation complete!")
