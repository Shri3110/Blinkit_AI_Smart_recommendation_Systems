import json
import random
import sqlite3
import os

personas = [
    {
        'user_id': 'U_PROFESSIONAL',
        'name': 'Priya Sharma',
        'age': 28,
        'occupation': 'Working Professional',
        'avatar': 'https://i.pravatar.cc/150?img=5',
        'shopping_behaviour': 'Routine Reorderer',
        'monthly_orders': 6,
        'exploration_score': 3,
        'average_order_value': 1200,
        'favourite_categories': ['Dairy, Bread & Eggs', 'Breakfast & Instant Food', 'Personal Care']
    },
    {
        'user_id': 'U_STUDENT',
        'name': 'Rahul Verma',
        'age': 21,
        'occupation': 'Student',
        'avatar': 'https://i.pravatar.cc/150?img=11',
        'shopping_behaviour': 'Explorer',
        'monthly_orders': 15,
        'exploration_score': 8,
        'average_order_value': 350,
        'favourite_categories': ['Snacks & Munchies', 'Cold Drinks & Juices', 'Chocolates & Desserts']
    },
    {
        'user_id': 'U_PET_OWNER',
        'name': 'Aditya Desai',
        'age': 32,
        'occupation': 'Pet Owner',
        'avatar': 'https://i.pravatar.cc/150?img=12',
        'shopping_behaviour': 'Routine Reorderer',
        'monthly_orders': 5,
        'exploration_score': 4,
        'average_order_value': 900,
        'favourite_categories': ['Pet Care', 'Cleaning Essentials']
    },
    {
        'user_id': 'U_FAMILY',
        'name': 'Neha Gupta',
        'age': 35,
        'occupation': 'Family Shopper',
        'avatar': 'https://i.pravatar.cc/150?img=1',
        'shopping_behaviour': 'Budget Conscious',
        'monthly_orders': 4,
        'exploration_score': 5,
        'average_order_value': 1800,
        'favourite_categories': ['Atta, Rice & Dal', 'Oil & Ghee', 'Masalas & Spices']
    },
    {
        'user_id': 'U_PARENT',
        'name': 'Kavita Reddy',
        'age': 30,
        'occupation': 'Parent',
        'avatar': 'https://i.pravatar.cc/150?img=9',
        'shopping_behaviour': 'Routine Reorderer',
        'monthly_orders': 12,
        'exploration_score': 2,
        'average_order_value': 1500,
        'favourite_categories': ['Baby Care', 'Dairy, Bread & Eggs', 'Cleaning Essentials']
    },
    {
        'user_id': 'U_FITNESS',
        'name': 'Rohan Mehta',
        'age': 26,
        'occupation': 'Fitness Enthusiast',
        'avatar': 'https://i.pravatar.cc/150?img=15',
        'shopping_behaviour': 'Explorer',
        'monthly_orders': 8,
        'exploration_score': 7,
        'average_order_value': 1100,
        'favourite_categories': ['Health & Wellness', 'Fruits & Vegetables']
    },
    {
        'user_id': 'U_BUDGET',
        'name': 'Aarav Singh',
        'age': 24,
        'occupation': 'Budget Shopper',
        'avatar': 'https://i.pravatar.cc/150?img=13',
        'shopping_behaviour': 'Budget Conscious',
        'monthly_orders': 3,
        'exploration_score': 6,
        'average_order_value': 400,
        'favourite_categories': ['Snacks & Munchies', 'Atta, Rice & Dal', 'Cleaning Essentials']
    },
    {
        'user_id': 'U_PREMIUM',
        'name': 'Rajesh Kumar',
        'age': 42,
        'occupation': 'Premium Shopper',
        'avatar': 'https://i.pravatar.cc/150?img=14',
        'shopping_behaviour': 'Explorer',
        'monthly_orders': 10,
        'exploration_score': 9,
        'average_order_value': 2500,
        'favourite_categories': ['Ice Cream & Frozen Foods', 'Skin Care', 'Personal Care']
    }
]

db_path = 'discovery_engine.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT raw_json FROM products')
products = [json.loads(row[0]) for row in cursor.fetchall()]

cursor.execute('DELETE FROM users')
cursor.execute('DELETE FROM purchases')
cursor.execute('DELETE FROM carts')

for p in personas:
    cursor.execute('INSERT INTO users (user_id, raw_json) VALUES (?, ?)', (p['user_id'], json.dumps(p)))
    
    for i in range(10):
        fav_prods = [prod for prod in products if prod.get('category') in p['favourite_categories']]
        if not fav_prods:
            fav_prods = products
        prod = random.choice(fav_prods)
        
        # In SQLite DB, purchases has columns: order_id, user_id, product_id, category, price_paid
        order_id = 'PUR_' + p['user_id'] + '_' + str(i)
        user_id = p['user_id']
        product_id = prod['product_id']
        category = prod.get('category', '')
        price_paid = prod.get('selling_price', 0)
        
        cursor.execute('INSERT INTO purchases (order_id, user_id, product_id, category, price_paid) VALUES (?, ?, ?, ?, ?)', 
                       (order_id, user_id, product_id, category, price_paid))

conn.commit()
conn.close()
print('Successfully seeded 8 specific personas with realistic purchases')
