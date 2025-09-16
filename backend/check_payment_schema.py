#!/usr/bin/env python3

import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'case_search.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if payments table exists and get its schema
try:
    cursor.execute("PRAGMA table_info(payments)")
    columns = cursor.fetchall()
    
    print("Payments table schema:")
    for column in columns:
        print(f"  {column[1]} ({column[2]}) - {'NOT NULL' if column[3] else 'NULL'}")
        
    # Check if there's a metadata column
    metadata_columns = [col for col in columns if 'metadata' in col[1].lower()]
    if metadata_columns:
        print(f"\nFound metadata columns: {[col[1] for col in metadata_columns]}")
    else:
        print("\nNo metadata columns found")
        
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
    print("Payments table might not exist")

conn.close()
