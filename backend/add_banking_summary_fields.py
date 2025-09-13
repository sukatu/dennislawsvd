#!/usr/bin/env python3
"""
Script to add AI-generated banking summary fields to the reported_cases table.
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

def add_banking_summary_fields():
    print("🚀 Adding AI-generated banking summary fields to reported_cases table...")
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        # Add new columns for AI-generated banking summary
        alter_queries = [
            "ALTER TABLE reported_cases ADD COLUMN ai_case_outcome VARCHAR(50) DEFAULT NULL COMMENT 'AI-generated case outcome (WON, LOST, PARTIALLY_WON, PARTIALLY_LOST, UNRESOLVED)'",
            "ALTER TABLE reported_cases ADD COLUMN ai_court_orders TEXT DEFAULT NULL COMMENT 'AI-generated court orders analysis'",
            "ALTER TABLE reported_cases ADD COLUMN ai_financial_impact VARCHAR(50) DEFAULT NULL COMMENT 'AI-generated financial impact level (HIGH, MODERATE, LOW, NONE)'",
            "ALTER TABLE reported_cases ADD COLUMN ai_detailed_outcome TEXT DEFAULT NULL COMMENT 'AI-generated detailed outcome analysis'",
            "ALTER TABLE reported_cases ADD COLUMN ai_summary_generated_at DATETIME DEFAULT NULL COMMENT 'Timestamp when AI summary was generated'",
            "ALTER TABLE reported_cases ADD COLUMN ai_summary_version VARCHAR(10) DEFAULT '1.0' COMMENT 'Version of AI summary generation algorithm'"
        ]

        for query in alter_queries:
            try:
                cursor.execute(query)
                print(f"✅ Executed: {query.split('ADD COLUMN')[1].split('COMMENT')[0].strip()}")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠️  Column already exists: {query.split('ADD COLUMN')[1].split('COMMENT')[0].strip()}")
                else:
                    print(f"❌ Error executing query: {e}")

        connection.commit()
        print("✅ All banking summary fields added successfully!")

        # Verify the new columns
        cursor.execute("DESCRIBE reported_cases;")
        columns = cursor.fetchall()
        
        print("\n📋 New columns in reported_cases table:")
        for column in columns:
            if column[0].startswith('ai_'):
                print(f"  {column[0]}: {column[1]} {column[2] or 'NO'} {column[3] or 'PRI'} {column[4] or 'None'} {column[5] or 'None'}")

    except Error as e:
        print(f"❌ Error adding banking summary fields: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    add_banking_summary_fields()
    print("🎉 Database update completed successfully!")
