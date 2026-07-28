import json
from services.ai_service import get_recommendation, get_db_connection

def run_tests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, raw_json FROM users LIMIT 5")
    users = cursor.fetchall()
    conn.close()

    print("--- Running Recommendation Engine Tests ---")
    for row in users:
        user_id = row["user_id"]
        profile = json.loads(row["raw_json"])
        print(f"\nUser: {profile['name']} (Persona: {profile['occupation']})")
        
        try:
            rec = get_recommendation(user_id)
            print(f"Recommended: {rec['recommended_product']['name']} ({rec['recommended_category']})")
            print(f"Confidence: {rec['confidence_score']}%")
            print(f"Reasons: {rec['matched_reasons']}")
            print(f"Explanation: {rec['explanation']}")
            print(f"Is New Category: {rec['is_new_category']}")
            
            # Validation
            assert rec['recommended_category'] == rec['recommended_product']['category'], "Category mismatch!"
            assert 70 <= rec['confidence_score'] <= 95, f"Score out of bounds: {rec['confidence_score']}"
            assert len(rec['matched_reasons']) >= 2, "Not enough reasons"
            assert rec['explanation'] != "", "Explanation empty"
            
            print("=> Validation PASSED")
        except Exception as e:
            print(f"=> Validation FAILED: {e}")

if __name__ == "__main__":
    run_tests()
