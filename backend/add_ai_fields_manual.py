#!/usr/bin/env python3
"""
Manual script to add AI banking summary fields to reported_cases table.
"""

import mysql.connector
from mysql.connector import Error
from config import settings

DATABASE_CONFIG = {
    'host': settings.mysql_host,
    'port': settings.mysql_port,
    'user': settings.mysql_user,
    'password': settings.mysql_password,
    'database': settings.mysql_database
}

def add_ai_fields():
    print("🚀 Adding AI banking summary fields to reported_cases table...")
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        # Check if fields already exist
        cursor.execute("SHOW COLUMNS FROM reported_cases LIKE 'ai_%'")
        existing_fields = cursor.fetchall()
        
        if existing_fields:
            print(f"⚠️  Found {len(existing_fields)} existing AI fields. Skipping addition.")
            for field in existing_fields:
                print(f"  - {field[0]}")
            return

        # Add AI fields one by one
        fields_to_add = [
            ("ai_case_outcome", "VARCHAR(50) DEFAULT NULL COMMENT 'AI-generated case outcome'"),
            ("ai_court_orders", "TEXT DEFAULT NULL COMMENT 'AI-generated court orders analysis'"),
            ("ai_financial_impact", "VARCHAR(50) DEFAULT NULL COMMENT 'AI-generated financial impact level'"),
            ("ai_detailed_outcome", "TEXT DEFAULT NULL COMMENT 'AI-generated detailed outcome analysis'"),
            ("ai_summary_generated_at", "DATETIME DEFAULT NULL COMMENT 'Timestamp when AI summary was generated'"),
            ("ai_summary_version", "VARCHAR(10) DEFAULT '1.0' COMMENT 'Version of AI summary generation algorithm'")
        ]

        for field_name, field_definition in fields_to_add:
            try:
                query = f"ALTER TABLE reported_cases ADD COLUMN {field_name} {field_definition}"
                cursor.execute(query)
                print(f"✅ Added field: {field_name}")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠️  Field {field_name} already exists")
                else:
                    print(f"❌ Error adding {field_name}: {e}")

        connection.commit()
        print("✅ All AI fields added successfully!")

    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    add_ai_fields()
    print("🎉 Database update completed!")
