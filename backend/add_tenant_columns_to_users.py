#!/usr/bin/env python3
"""
Migration script to add tenant-related columns to the users table
"""

import sys
import os
from sqlalchemy import text

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal

def add_tenant_columns():
    """Add tenant_id and is_tenant_admin columns to users table"""
    
    db = SessionLocal()
    try:
        print("Adding tenant columns to users table...")
        
        # Check if columns already exist
        result = db.execute(text("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'users' 
            AND COLUMN_NAME IN ('tenant_id', 'is_tenant_admin')
        """))
        
        existing_columns = [row[0] for row in result.fetchall()]
        
        # Add tenant_id column if it doesn't exist
        if 'tenant_id' not in existing_columns:
            print("Adding tenant_id column...")
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN tenant_id INT NULL,
                ADD INDEX idx_users_tenant_id (tenant_id)
            """))
            print("✓ Added tenant_id column")
        else:
            print("✓ tenant_id column already exists")
        
        # Add is_tenant_admin column if it doesn't exist
        if 'is_tenant_admin' not in existing_columns:
            print("Adding is_tenant_admin column...")
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN is_tenant_admin BOOLEAN NOT NULL DEFAULT FALSE
            """))
            print("✓ Added is_tenant_admin column")
        else:
            print("✓ is_tenant_admin column already exists")
        
        # Add foreign key constraint if it doesn't exist
        try:
            print("Adding foreign key constraint...")
            db.execute(text("""
                ALTER TABLE users 
                ADD CONSTRAINT fk_users_tenant_id 
                FOREIGN KEY (tenant_id) REFERENCES tenants(id) 
                ON DELETE SET NULL
            """))
            print("✓ Added foreign key constraint")
        except Exception as e:
            if "Duplicate key name" in str(e) or "already exists" in str(e):
                print("✓ Foreign key constraint already exists")
            else:
                print(f"Warning: Could not add foreign key constraint: {e}")
        
        db.commit()
        print("\n✅ Successfully added tenant columns to users table!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding tenant columns: {e}")
        raise
    finally:
        db.close()

def verify_columns():
    """Verify that the columns were added successfully"""
    
    db = SessionLocal()
    try:
        print("\nVerifying columns...")
        
        result = db.execute(text("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'users' 
            AND COLUMN_NAME IN ('tenant_id', 'is_tenant_admin')
            ORDER BY COLUMN_NAME
        """))
        
        columns = result.fetchall()
        
        if len(columns) == 2:
            print("✅ All tenant columns found:")
            for col_name, data_type, is_nullable, default in columns:
                print(f"  - {col_name}: {data_type}, nullable: {is_nullable}, default: {default}")
        else:
            print(f"⚠️  Expected 2 columns, found {len(columns)}")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        
    except Exception as e:
        print(f"❌ Error verifying columns: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting tenant columns migration...")
    add_tenant_columns()
    verify_columns()
    print("\n🎉 Migration completed!")
