#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
for row in cursor:
    print(row)
cursor.close()
db.close()
