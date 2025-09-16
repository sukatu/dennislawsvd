#!/usr/bin/env python3
"""
Script to update AI columns in reported_cases table to support longer text
"""

import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_ai_columns():
    """Update AI columns to TEXT type"""
    
    # Database connection parameters
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Hausawi@2025',
        'database': 'dennislaw_svd',
        'charset': 'utf8mb4'
    }
    
    try:
        # Connect to database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        print("Connected to database successfully")
        
        # Update AI columns to TEXT type
        alter_queries = [
            "ALTER TABLE reported_cases MODIFY COLUMN ai_case_outcome TEXT",
            "ALTER TABLE reported_cases MODIFY COLUMN ai_financial_impact TEXT"
        ]
        
        for query in alter_queries:
            try:
                print(f"Executing: {query}")
                cursor.execute(query)
                print("✓ Success")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        # Commit changes
        connection.commit()
        print("\nAll AI columns updated successfully!")
        
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    update_ai_columns()
