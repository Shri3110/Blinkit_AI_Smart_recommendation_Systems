import sqlite3
import json
import random

def get_realistic_age(occupation):
    if occupation == 'Student':
        return random.randint(18, 24)
    elif occupation == 'Working Professional':
        return random.randint(25, 45)
    elif occupation == 'Parent':
        return random.randint(28, 55)
    elif occupation == 'Fitness Enthusiast':
        return random.randint(20, 35)
    elif occupation == 'Family Shopper':
        return random.randint(30, 55)
    elif occupation == 'Pet Owner':
        return random.randint(22, 50)
    elif occupation == 'Premium Shopper':
        return random.randint(28, 55)
    elif occupation == 'Budget Shopper':
        return random.randint(22, 60)
    else:
        return random.randint(25, 50)

def main():
    names = [
        "Arun Kumar", "Priya Raman", "Karthik Sundaram", "Divya Iyer",
        "Ramesh Pillai", "Lakshmi Nair", "Suresh Chandran", "Anitha Murugan",
        "Vignesh Krishnan", "Meena Balakrishnan", "Gokul Ganesan", "Swetha Shankar",
        "Naveen Ravi", "Deepa Selvam", "Bala Venkatesan", "Revathi Rajagopal",
        "Sathish Natarajan", "Kavya Subramaniam", "Manoj Elango", "Preethi Vasudevan"
    ]
    
    conn = sqlite3.connect('discovery_engine.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, raw_json FROM users ORDER BY user_id ASC")
    users = cursor.fetchall()
    
    for i, (user_id, raw_json_str) in enumerate(users):
        if i >= len(names):
            break
            
        user_data = json.loads(raw_json_str)
        
        # Update name
        user_data['name'] = names[i]
        
        # Update age based on occupation
        occupation = user_data.get('occupation', 'Student')
        user_data['age'] = get_realistic_age(occupation)
        
        # Save back to DB
        new_raw_json = json.dumps(user_data)
        cursor.execute("UPDATE users SET raw_json = ? WHERE user_id = ?", (new_raw_json, user_id))
        
    conn.commit()
    conn.close()
    print("Users updated successfully!")

if __name__ == "__main__":
    main()
