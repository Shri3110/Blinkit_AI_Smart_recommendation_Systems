import os
from dotenv import load_dotenv
load_dotenv() # Load variables from .env file

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai_service import get_cart, get_recommendation, get_product_by_id, get_db_connection
import json

app = FastAPI(title="Blinkit Smart Discovery MVP")

CATEGORY_IMAGES = {
    'Fruits & Vegetables': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&q=80',
    'Dairy, Bread & Eggs': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80',
    'Atta, Rice & Dal': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&q=80',
    'Oil & Ghee': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&q=80',
    'Masalas & Spices': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80',
    'Breakfast & Instant Food': 'https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=400&q=80',
    'Snacks & Munchies': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=400&q=80',
    'Biscuits & Bakery': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400&q=80',
    'Chocolates & Desserts': 'https://images.unsplash.com/photo-1614088685112-0a760b71a3c8?w=400&q=80',
    'Tea & Coffee': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&q=80',
    'Cold Drinks & Juices': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&q=80',
    'Personal Care': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&q=80',
    'Hair Care': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&q=80',
    'Skin Care': 'https://images.unsplash.com/photo-1617897903246-719242758050?w=400&q=80',
    'Baby Care': 'https://images.unsplash.com/photo-1519689680058-324335c77eba?w=400&q=80',
    'Pet Care': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&q=80',
    'Cleaning Essentials': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400&q=80',
    'Home & Kitchen': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=400&q=80',
    'Ice Cream & Frozen Foods': 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=400&q=80',
    'Health & Wellness': '/health_wellness.png',
    'Stationery': 'https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=400&q=80',
    'Electronics & Accessories': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&q=80'
}

def fix_product_image(product):
    if product and 'category' in product:
        cat_img = CATEGORY_IMAGES.get(product['category'])
        if cat_img:
            product['image_url'] = cat_img
    return product

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/cart/{user_id}")
async def get_user_cart(user_id: str):
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Expand products with catalog details for frontend display
    expanded_items = []
    for item in cart.get("cart_items", []):
        prod = get_product_by_id(item["product_id"])
        if prod:
            prod = fix_product_image(prod)
            expanded_items.append({**prod, "quantity": item["quantity"]})
            
    return {
        "cart_id": cart["cart_id"],
        "user_id": cart["user_id"],
        "cart_value": cart["cart_value"],
        "items": expanded_items
    }

class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int = 1

@app.post("/api/cart/{user_id}/add")
async def add_to_cart(user_id: str, req: AddToCartRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    prod = get_product_by_id(req.product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
        
    cursor.execute("SELECT raw_json FROM carts WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if row:
        cart = json.loads(row["raw_json"])
        # Check if item exists
        existing = next((item for item in cart.get("cart_items", []) if item["product_id"] == req.product_id), None)
        if existing:
            existing["quantity"] += req.quantity
        else:
            cart.setdefault("cart_items", []).append({"product_id": req.product_id, "quantity": req.quantity})
            
        cart["cart_value"] = cart.get("cart_value", 0) + (prod["selling_price"] * req.quantity)
        
        cursor.execute("UPDATE carts SET cart_value = ?, raw_json = ? WHERE user_id = ?", 
                       (cart["cart_value"], json.dumps(cart), user_id))
    else:
        # Create new cart
        cart_id = f"C_NEW_{user_id}"
        cart_value = prod["selling_price"] * req.quantity
        cart = {
            "cart_id": cart_id,
            "user_id": user_id,
            "cart_items": [{"product_id": req.product_id, "quantity": req.quantity}],
            "cart_value": cart_value,
            "time_of_day": "Morning",
            "day_of_week": "Monday",
            "shopping_mission": "Dynamic Build",
            "checkout_status": "Active"
        }
        cursor.execute("INSERT INTO carts (cart_id, user_id, cart_value, raw_json) VALUES (?, ?, ?, ?)",
                       (cart_id, user_id, cart_value, json.dumps(cart)))
                       
    conn.commit()
    conn.close()
    return {"message": "Added to cart"}

@app.delete("/api/cart/{user_id}/clear")
async def clear_cart(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carts WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": "Cart cleared successfully"}

@app.delete("/api/cart/{user_id}/item/{product_id}")
async def remove_item_from_cart(user_id: str, product_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT raw_json FROM carts WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Cart not found")
        
    cart = json.loads(row["raw_json"])
    item_to_remove = next((item for item in cart.get("cart_items", []) if item["product_id"] == product_id), None)
    
    if not item_to_remove:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found in cart")
        
    prod = get_product_by_id(product_id)
    if prod:
        cart["cart_value"] = max(0, cart.get("cart_value", 0) - (prod["selling_price"] * item_to_remove["quantity"]))
        
    cart["cart_items"] = [item for item in cart.get("cart_items", []) if item["product_id"] != product_id]
    
    # If cart is empty, delete it
    if not cart["cart_items"]:
        cursor.execute("DELETE FROM carts WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("UPDATE carts SET cart_value = ?, raw_json = ? WHERE user_id = ?", 
                       (cart["cart_value"], json.dumps(cart), user_id))
    
    conn.commit()
    conn.close()
    return {"message": "Item removed from cart"}


@app.post("/api/recommend/{user_id}")
async def recommend(user_id: str):
    try:
        recommendation = get_recommendation(user_id)
        if recommendation and "recommended_product" in recommendation:
            recommendation["recommended_product"] = fix_product_image(recommendation["recommended_product"])
        return recommendation
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/api/categories")
async def get_categories(user_id: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    rows = cursor.fetchall()
    categories = [row["category"] for row in rows]
    
    if user_id:
        cursor.execute("SELECT raw_json FROM users WHERE user_id = ?", (user_id,))
        user_row = cursor.fetchone()
        if user_row:
            user_data = json.loads(user_row["raw_json"])
            fav_cats = user_data.get("favourite_categories", [])
            categories = [c for c in fav_cats if c in categories] + [c for c in categories if c not in fav_cats]
            
    conn.close()
    return categories

@app.get("/api/products/featured")
async def get_featured_products(user_id: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    fav_cats = []
    if user_id:
        cursor.execute("SELECT raw_json FROM users WHERE user_id = ?", (user_id,))
        user_row = cursor.fetchone()
        if user_row:
            user_data = json.loads(user_row["raw_json"])
            fav_cats = user_data.get("favourite_categories", [])
            
    if fav_cats:
        placeholders = ','.join(['?'] * len(fav_cats))
        query = f"SELECT raw_json FROM products WHERE category IN ({placeholders}) ORDER BY RANDOM() LIMIT 12"
        cursor.execute(query, fav_cats)
        rows = cursor.fetchall()
        
        if len(rows) < 12:
            limit = 12 - len(rows)
            query_backfill = f"SELECT raw_json FROM products WHERE category NOT IN ({placeholders}) ORDER BY RANDOM() LIMIT ?"
            params = tuple(fav_cats) + (limit,)
            cursor.execute(query_backfill, params)
            rows.extend(cursor.fetchall())
    else:
        cursor.execute("SELECT raw_json FROM products ORDER BY RANDOM() LIMIT 12")
        rows = cursor.fetchall()
        
    conn.close()
    return [fix_product_image(json.loads(row["raw_json"])) for row in rows]

@app.get("/api/products/category/{category}")
async def get_category_products(category: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT raw_json FROM products WHERE category = ? LIMIT 50", (category,))
    rows = cursor.fetchall()
    conn.close()
    return [fix_product_image(json.loads(row["raw_json"])) for row in rows]

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    prod = get_product_by_id(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return fix_product_image(prod)

@app.get("/api/users")
async def get_users():
    # Return full user details for the frontend
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT raw_json FROM users LIMIT 20")
    rows = cursor.fetchall()
    conn.close()
    return [json.loads(row["raw_json"]) for row in rows]

@app.get("/api/users/{user_id}/purchases")
async def get_user_purchases(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pr.raw_json, pu.price_paid 
        FROM purchases pu
        JOIN products pr ON pu.product_id = pr.id
        WHERE pu.user_id = ?
        ORDER BY pu.order_id DESC
        LIMIT 10
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    purchases = []
    for row in rows:
        prod = json.loads(row["raw_json"])
        prod = fix_product_image(prod)
        prod["price_paid"] = row["price_paid"]
        purchases.append(prod)
    return purchases

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
