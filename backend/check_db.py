import sqlite3, json
c=sqlite3.connect('discovery_engine.db')
for row in c.execute('SELECT raw_json FROM products WHERE category = "Health & Wellness" LIMIT 5'):
 print(json.loads(row[0]).get('image_url'))
