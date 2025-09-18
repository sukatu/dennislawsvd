#!/usr/bin/env python3
"""
Migration script to make requested_by column nullable in subscription_requests table
"""

import sys
import os
from sqlalchemy import text

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal

def fix_requested_by_column():
    """Make requested_by column nullable in subscription_requests table"""
    
    db = SessionLocal()
    try:
        print("Making requested_by column nullable in subscription_requests table...")
        
        # Check current column definition
        result = db.execute(text("""
            SELECT COLUMN_NAME, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'subscription_requests' 
            AND COLUMN_NAME = 'requested_by'
        """))
        
        column_info = result.fetchone()
        if column_info:
            print(f"Current column definition: {column_info}")
            if column_info[1] == 'YES':
                print("✓ requested_by column is already nullable")
                return
        
        # Make the column nullable
        print("Updating requested_by column to be nullable...")
        db.execute(text("""
            ALTER TABLE subscription_requests 
            MODIFY COLUMN requested_by INT NULL
        """))
        
        db.commit()
        print("✅ Successfully made requested_by column nullable!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating column: {e}")
        raise
    finally:
        db.close()

def verify_column():
    """Verify that the column was updated successfully"""
    
    db = SessionLocal()
    try:
        print("\nVerifying column update...")
        
        result = db.execute(text("""
            SELECT COLUMN_NAME, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'subscription_requests' 
            AND COLUMN_NAME = 'requested_by'
        """))
        
        column_info = result.fetchone()
        if column_info:
            print(f"Updated column definition: {column_info}")
            if column_info[1] == 'YES':
                print("✅ Column is now nullable")
            else:
                print("❌ Column is still not nullable")
        else:
            print("❌ Column not found")
        
    except Exception as e:
        print(f"❌ Error verifying column: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting requested_by column migration...")
    fix_requested_by_column()
    verify_column()
    print("\n🎉 Migration completed!")
