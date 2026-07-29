import os
import json
import sqlite3
import random
from groq import Groq

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "discovery_engine.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_cart(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT raw_json FROM carts WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row["raw_json"])
    return None

def get_product_by_id(product_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT raw_json FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row["raw_json"])
    return None

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [row["category"] for row in rows]

from collections import Counter

PERSONA_PREFERENCES = {
    "Fitness Enthusiasts": {
        "preferred": ["Health & Wellness", "Fruits & Vegetables", "Meat & Seafood", "Dairy, Bread & Eggs"],
        "avoid": ["Snacks & Munchies", "Cold Drinks & Juices", "Sweet Tooth"]
    },
    "Students": {
        "preferred": ["Snacks & Munchies", "Cold Drinks & Juices", "Instant Food", "Breakfast & Instant Food"],
        "avoid": ["Baby Care", "Meat & Seafood", "Pet Care"]
    },
    "Families": {
        "preferred": ["Dairy, Bread & Eggs", "Cleaning Essentials", "Home & Kitchen", "Atta, Rice & Dal", "Personal Care"],
        "avoid": []
    },
    "Parents": {
        "preferred": ["Baby Care", "Dairy, Bread & Eggs", "Cleaning Essentials", "Home & Kitchen"],
        "avoid": []
    },
    "Pet Owners": {
        "preferred": ["Pet Care", "Cleaning Essentials", "Home & Kitchen"],
        "avoid": []
    }
}

PRODUCT_AFFINITY_MAP = {
    "Milk": "Cornflakes",
    "Bread": "Butter",
    "Protein Powder": "Electral",
    "Oats": "Dry Fruits",
    "Rice": "Pickles",
    "Atta": "Cooking Oil",
    "Pet Food": "Pet Shampoo",
    "Dog Treats": "Pet Toys",
    "Cleaning Liquid": "Air Freshener"
}

SESSION_HISTORY = {} # user_id -> set of recently recommended product IDs

def rank_unexplored_categories(unexplored_categories, profile, category_frequencies, cart_items):
    scored_cats = []
    persona_type = profile.get('occupation', '')
    prefs = PERSONA_PREFERENCES.get(persona_type, {"preferred": [], "avoid": []})
    
    exploration_score = profile.get('exploration_score', 5)
    cart_cat_names = [item.get("category", "") for item in cart_items]
    
    for cat in unexplored_categories:
        score = 0
        
        # 1. Persona preference
        if cat in prefs["preferred"]:
            score += 40
        elif cat in prefs["avoid"]:
            score -= 40
            
        # 2. Cart compatibility (heuristic mapping)
        if "Dairy, Bread & Eggs" in cart_cat_names and cat in ["Breakfast & Instant Food", "Snacks & Munchies"]:
            score += 20
        if "Snacks & Munchies" in cart_cat_names and cat in ["Cold Drinks & Juices", "Sweet Tooth"]:
            score += 20
        if "Pet Care" in cart_cat_names and cat in ["Cleaning Essentials"]:
            score += 15
        if "Baby Care" in cart_cat_names and cat in ["Cleaning Essentials", "Dairy, Bread & Eggs"]:
            score += 15
            
        # 3. Purchase History Affinity
        # If they buy a lot of fruits/veg, maybe health/wellness is good
        if "Fruits & Vegetables" in category_frequencies and cat == "Health & Wellness":
            score += 15
            
        # 4. Shopping behaviour / Exploration score
        # Use exploration_score as a multiplier for some random variance to ensure 
        # that ties are broken differently and high explorers get more variety
        score += exploration_score * random.randint(1, 4)
        
        scored_cats.append((score, cat))
        
    scored_cats.sort(key=lambda x: x[0], reverse=True)
    return [c[1] for c in scored_cats]

def score_candidate(product, profile, category_frequencies, cart_items, unexplored_categories):
    score = 0
    reasons = set()
    
    cat = product.get("category", "")
    name = product.get("name", "")
    
    # 1. Persona Match (+30)
    persona_type = profile.get('occupation', '')
    if persona_type in PERSONA_PREFERENCES:
        prefs = PERSONA_PREFERENCES[persona_type]
        if cat in prefs["preferred"]:
            score += 30
            if persona_type == "Fitness Enthusiasts":
                reasons.add("Matches your healthy lifestyle")
            elif persona_type == "Students":
                reasons.add("Matches your shopping style")
            elif persona_type in ["Families", "Parents"]:
                reasons.add("Relevant to your family needs")
            elif persona_type == "Pet Owners":
                reasons.add("Ideal for your pets")
            else:
                reasons.add("Fits your shopping routine")
        elif cat in prefs["avoid"]:
            score -= 20
            
    # 2. Purchase History Relevance (+25)
    if cat in category_frequencies:
        freq = category_frequencies[cat]
        if freq >= 3:
            score += 25
            reasons.add("High affinity with your purchase history")
        elif freq == 2:
            score += 15
            reasons.add("Relevant to your lifestyle")
        else:
            score += 5
            reasons.add("Based on your recent purchases")
            
    # 3. Current Cart Compatibility (+20)
    cart_match = False
    for cart_item in cart_items:
        cart_name = cart_item.get("name", "")
        for trigger, target in PRODUCT_AFFINITY_MAP.items():
            if trigger.lower() in cart_name.lower() and target.lower() in name.lower():
                cart_match = True
            elif target.lower() in cart_name.lower() and trigger.lower() in name.lower():
                cart_match = True
                
    if cart_match:
        score += 20
        reasons.add("Frequently bought with your favourite products")
        reasons.add("Great complementary purchase")
                
    # 4. Cross-category Novelty (+10) -> Reduced from +15 so it doesn't overpower persona match
    if cat in unexplored_categories:
        score += 10
        reasons.add("Introduces a new category")
        
    # 5. Product Availability (+10) (simulated)
    score += 10
    
    # Map score to 70-95 range
    final_score = 70 + int((score / 100.0) * 25)
    final_score = max(70, min(95, final_score))
        
    return final_score, list(reasons)


def get_recommendation(user_id: str):
    api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key) if api_key else None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get Profile
    cursor.execute("SELECT raw_json FROM users WHERE user_id = ?", (user_id,))
    user_row = cursor.fetchone()
    if not user_row:
        profile = {"age": 30, "occupation": "Unknown", "shopping_behaviour": "Unknown"}
    else:
        profile = json.loads(user_row["raw_json"])
    
    # Get Frequent Categories & Frequencies
    cursor.execute("SELECT category FROM purchases WHERE user_id = ?", (user_id,))
    purchases = cursor.fetchall()
    purchase_categories = [row["category"] for row in purchases]
    category_frequencies = Counter(purchase_categories)
    frequent_categories = list(category_frequencies.keys())

    # Get Cart
    cart = get_cart(user_id)
    cart_items = []
    if cart:
        for item in cart.get("cart_items", []):
            prod = get_product_by_id(item["product_id"])
            if prod:
                cart_items.append(prod)
    
    cart_details = [{"name": item["name"], "category": item["category"]} for item in cart_items]
    
    all_cats = get_all_categories()
    unexplored_categories = [c for c in all_cats if c not in frequent_categories]
    if not unexplored_categories:
        unexplored_categories = all_cats # Fallback

    # Intelligent Candidate Generation
    ranked_unexplored = rank_unexplored_categories(unexplored_categories, profile, category_frequencies, cart_items)
    
    # Pick the top 2-3 highest-ranked unexplored categories
    top_unexplored = ranked_unexplored[:3]
    
    # Pool candidate categories based on Persona + Top Unexplored
    persona_type = profile.get('occupation', '')
    target_categories = set(top_unexplored)
    if persona_type in PERSONA_PREFERENCES:
        target_categories.update(PERSONA_PREFERENCES[persona_type]["preferred"])
        
    # Pool from targeted categories
    placeholders = ','.join('?' for _ in target_categories)
    cursor.execute(f"SELECT raw_json FROM products WHERE category IN ({placeholders})", list(target_categories))
    all_targeted_products = [json.loads(row["raw_json"]) for row in cursor.fetchall()]
    
    # If not enough, fallback to random
    if len(all_targeted_products) < 15:
        cursor.execute("SELECT raw_json FROM products")
        all_targeted_products = [json.loads(row["raw_json"]) for row in cursor.fetchall()]
        
    conn.close()

    # Shuffle before slicing to ensure variety even within the targeted categories
    random.shuffle(all_targeted_products)
    candidates = all_targeted_products[:50]
    
    scored_candidates = []
    
    for candidate in candidates:
        # Don't recommend something already in the cart
        if any(c.get("id") == candidate.get("id") for c in cart_items):
            continue
            
        score, reasons = score_candidate(candidate, profile, category_frequencies, cart_items, unexplored_categories)
        scored_candidates.append((score, candidate, reasons))
        
    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    
    if scored_candidates:
        top_3 = scored_candidates[:3]
        history = SESSION_HISTORY.get(user_id, set())
        
        # Filter top_3 by those NOT in history
        unseen_top_3 = [c for c in top_3 if c[1].get("id") not in history]
        
        # If all top 3 have been seen recently, reset history and use all top 3
        if not unseen_top_3:
            unseen_top_3 = top_3
            SESSION_HISTORY[user_id] = set()
            
        highest_score = unseen_top_3[0][0]
        # Find candidates within 5 points of the highest available score in the top 3
        close_candidates = [c for c in unseen_top_3 if (highest_score - c[0]) <= 5]
        
        selected = random.choice(close_candidates)
        best_score, best_candidate, best_reasons = selected
        
        if user_id not in SESSION_HISTORY:
            SESSION_HISTORY[user_id] = set()
        SESSION_HISTORY[user_id].add(best_candidate.get("id"))
    else:
        best_candidate = {"name": "Mystery Item", "selling_price": 99, "category": random.choice(unexplored_categories)}
        best_score = 35
        best_reasons = ["Helps you discover a new category"]

    rec_category = best_candidate.get("category")
    intent = "Cross-category Discovery"

    def get_fallback_explanation(persona_type, candidate_name, rec_category):
        if persona_type == "Fitness Enthusiasts":
            return f"Based on your healthy shopping habits, {candidate_name} is a great addition to your regular purchases while helping you explore a new category."
        elif persona_type in ["Families", "Parents"]:
            return f"Parents with similar shopping patterns often purchase {candidate_name} alongside their regular family essentials."
        elif persona_type == "Working Professionals":
            return f"This {candidate_name} complements your routine purchases and introduces something new without changing your usual shopping behaviour."
        elif persona_type == "Students":
            return f"This quick and affordable {candidate_name} matches your shopping style while encouraging category exploration."
        elif persona_type == "Premium Shoppers":
            return f"This premium recommendation aligns with your preferences while helping you discover another category."
        else:
            return f"Since you frequently shop with us, we think {candidate_name} from {rec_category} perfectly complements your order."

    if client:
        # LLM Logic - restricted ONLY to generating the explanation
        prompt = f"""
        You are an AI recommendation engine for an Indian quick-commerce app (Blinkit).
        
        User Profile: Age {profile.get('age', 'Unknown')}, Occupation: {profile.get('occupation', 'Unknown')}
        Shopping Behaviour: {profile.get('shopping_behaviour', 'Unknown')}
        
        Current Cart Items:
        {json.dumps(cart_details, indent=2)}
        
        Frequently Bought Categories:
        {frequent_categories}
        
        SELECTED PRODUCT TO RECOMMEND:
        Name: {best_candidate.get('name')}
        Category: {rec_category}
        
        Task:
        Write a short, conversational explanation addressing the user directly (MAXIMUM 2 to 3 sentences) explaining WHY this specific product was recommended to them.
        
        CRITICAL RULES:
        - Use a natural, conversational tone. Avoid generic, repetitive phrases like "We've found that..."
        - Combine their Persona, Shopping behaviour, Cart items, and whether it helps them discover a new category into the explanation.
        - Do NOT invent or hallucinate product features or use-cases.
        - Keep it strictly to 2 to 3 sentences.
        
        Output JSON format exactly:
        {{
          "explanation": "string"
        }}
        """
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            explanation = result.get("explanation")
            if not explanation:
                explanation = get_fallback_explanation(persona_type, best_candidate.get('name'), rec_category)
        except Exception as e:
            print(f"LLM Error: {e}")
            explanation = get_fallback_explanation(persona_type, best_candidate.get('name'), rec_category)
    else:
        explanation = get_fallback_explanation(persona_type, best_candidate.get('name'), rec_category)

    # Validate output consistency before returning
    if not explanation or not explanation.strip():
        explanation = get_fallback_explanation(persona_type, best_candidate.get('name'), rec_category)
        
    while len(best_reasons) < 2:
        if "Popular among similar shoppers" not in best_reasons:
            best_reasons.append("Popular among similar shoppers")
        else:
            best_reasons.append("Fits your shopping routine")

    best_score = max(70, min(95, best_score))

    return {
        "intent": intent,
        "recommended_category": rec_category,
        "recommended_product": best_candidate,
        "explanation": explanation,
        "confidence_score": best_score,
        "matched_reasons": best_reasons,
        "is_new_category": rec_category in unexplored_categories
    }
