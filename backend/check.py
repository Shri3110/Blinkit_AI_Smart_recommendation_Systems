import sqlite3
c=sqlite3.connect('discovery_engine.db')
for r in c.execute('SELECT id, name, image_url FROM products WHERE image_url NOT LIKE ''%pro_placeholder%'''):
 print(r)
