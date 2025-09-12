#!/usr/bin/env python3
"""
Script to add previous_names field to banks, people, and insurance tables
"""

import pymysql
from config import settings

def add_previous_names_field():
    """Add previous_names JSON field to banks, people, and insurance tables"""
    
    # Database configuration
    db_config = {
        'host': settings.mysql_host,
        'user': settings.mysql_user,
        'password': settings.mysql_password,
        'database': settings.mysql_database,
        'charset': 'utf8mb4'
    }
    
    try:
        # Connect to database
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        print("Adding previous_names field to banks table...")
        cursor.execute("""
            ALTER TABLE banks 
            ADD COLUMN previous_names JSON DEFAULT NULL 
            COMMENT 'JSON array of previous names held by the bank'
        """)
        
        print("Adding previous_names field to people table...")
        cursor.execute("""
            ALTER TABLE people 
            ADD COLUMN previous_names JSON DEFAULT NULL 
            COMMENT 'JSON array of previous names held by the person'
        """)
        
        print("Adding previous_names field to insurance table...")
        cursor.execute("""
            ALTER TABLE insurance 
            ADD COLUMN previous_names JSON DEFAULT NULL 
            COMMENT 'JSON array of previous names held by the insurance company'
        """)
        
        # Commit changes
        conn.commit()
        print("✅ Successfully added previous_names field to all tables")
        
        # Add some sample data
        print("\nAdding sample previous names data...")
        
        # Sample data for banks
        bank_previous_names = [
            {
                "bank_id": 1,
                "previous_names": [
                    "Access Bank Ghana Limited",
                    "Access Bank (Ghana) Limited", 
                    "Access Bank Ghana",
                    "Access Bank Ltd"
                ]
            },
            {
                "bank_id": 2,
                "previous_names": [
                    "Ghana Commercial Bank Limited",
                    "GCB Bank Limited",
                    "Ghana Commercial Bank",
                    "GCB"
                ]
            },
            {
                "bank_id": 3,
                "previous_names": [
                    "Ecobank Ghana Limited",
                    "Ecobank (Ghana) Limited",
                    "Ecobank Ghana",
                    "Ecobank Ltd"
                ]
            }
        ]
        
        for bank_data in bank_previous_names:
            cursor.execute("""
                UPDATE banks 
                SET previous_names = %s 
                WHERE id = %s
            """, (str(bank_data["previous_names"]), bank_data["bank_id"]))
        
        # Sample data for people
        people_previous_names = [
            {
                "person_id": 1,
                "previous_names": [
                    "John Kwame Asante",
                    "Kwame John Asante",
                    "J.K. Asante"
                ]
            },
            {
                "person_id": 2,
                "previous_names": [
                    "Mary Akosua Mensah",
                    "Akosua Mary Mensah",
                    "A.M. Mensah"
                ]
            }
        ]
        
        for person_data in people_previous_names:
            cursor.execute("""
                UPDATE people 
                SET previous_names = %s 
                WHERE id = %s
            """, (str(person_data["previous_names"]), person_data["person_id"]))
        
        # Sample data for insurance
        insurance_previous_names = [
            {
                "insurance_id": 1,
                "previous_names": [
                    "Ghana Life Insurance Company Limited",
                    "Ghana Life Insurance Co. Ltd",
                    "Ghana Life Insurance"
                ]
            },
            {
                "insurance_id": 2,
                "previous_names": [
                    "Enterprise Life Assurance Company Limited",
                    "Enterprise Life Assurance Co. Ltd",
                    "Enterprise Life"
                ]
            }
        ]
        
        for insurance_data in insurance_previous_names:
            cursor.execute("""
                UPDATE insurance 
                SET previous_names = %s 
                WHERE id = %s
            """, (str(insurance_data["previous_names"]), insurance_data["insurance_id"]))
        
        conn.commit()
        print("✅ Successfully added sample previous names data")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_previous_names_field()
