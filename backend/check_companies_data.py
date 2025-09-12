#!/usr/bin/env python3
"""
Script to check and fix companies data
"""

from sqlalchemy import create_engine, text
from config import settings
from datetime import datetime

def check_companies_data():
    """Check companies data and fix any issues"""
    engine = create_engine(settings.database_url)
    
    with engine.connect() as conn:
        # Check the first company
        result = conn.execute(text("SELECT id, name, created_at, updated_at, search_count FROM companies WHERE id = 1"))
        company = result.fetchone()
        
        if company:
            print(f"Company ID: {company[0]}")
            print(f"Name: {company[1]}")
            print(f"Created At: {company[2]}")
            print(f"Updated At: {company[3]}")
            print(f"Search Count: {company[4]}")
            
            # Fix NULL created_at and updated_at
            if company[2] is None or company[3] is None:
                print("\nFixing NULL timestamps...")
                conn.execute(text("""
                    UPDATE companies 
                    SET created_at = NOW(), updated_at = NOW() 
                    WHERE id = 1
                """))
                conn.commit()
                print("Timestamps fixed!")
        else:
            print("No company found with ID 1")

if __name__ == "__main__":
    check_companies_data()
