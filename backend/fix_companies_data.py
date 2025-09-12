#!/usr/bin/env python3
"""
Script to fix all companies data with NULL values
"""

from sqlalchemy import create_engine, text
from config import settings

def fix_companies_data():
    """Fix all companies data with NULL values"""
    engine = create_engine(settings.database_url)
    
    with engine.connect() as conn:
        # Fix NULL timestamps and search_count for all companies
        print("Fixing NULL timestamps and search_count for all companies...")
        
        # Update all companies with NULL created_at, updated_at, or search_count
        conn.execute(text("""
            UPDATE companies 
            SET 
                created_at = COALESCE(created_at, NOW()),
                updated_at = COALESCE(updated_at, NOW()),
                search_count = COALESCE(search_count, 0)
            WHERE 
                created_at IS NULL 
                OR updated_at IS NULL 
                OR search_count IS NULL
        """))
        
        conn.commit()
        
        # Check how many companies were updated
        result = conn.execute(text("""
            SELECT COUNT(*) as total_companies,
                   SUM(CASE WHEN created_at IS NOT NULL THEN 1 ELSE 0 END) as with_created_at,
                   SUM(CASE WHEN updated_at IS NOT NULL THEN 1 ELSE 0 END) as with_updated_at,
                   SUM(CASE WHEN search_count IS NOT NULL THEN 1 ELSE 0 END) as with_search_count
            FROM companies
        """))
        
        stats = result.fetchone()
        print(f"Total companies: {stats[0]}")
        print(f"Companies with created_at: {stats[1]}")
        print(f"Companies with updated_at: {stats[2]}")
        print(f"Companies with search_count: {stats[3]}")
        
        print("Companies data fixed successfully!")

if __name__ == "__main__":
    fix_companies_data()
