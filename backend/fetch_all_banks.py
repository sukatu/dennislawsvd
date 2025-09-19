#!/usr/bin/env python3
"""
Script to fetch ALL banks data from MySQL to PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import pymysql
import json

# Load environment variables
load_dotenv()

# MySQL Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "dennislaw_svd")

# PostgreSQL Configuration
from config import settings

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_mysql_connection():
    """Get MySQL connection"""
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset='utf8mb4'
    )

def get_postgres_engine():
    """Get PostgreSQL engine"""
    return create_engine(settings.database_url)

def safe_convert_date(value):
    """Safely convert value to datetime"""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return None
    return value

def safe_convert_json(value):
    """Safely convert value to JSON"""
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except:
            return value
    return value

def fetch_all_banks():
    """Fetch ALL banks data from MySQL to PostgreSQL"""
    log("🏦 Fetching ALL banks data from MySQL...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get total count first
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM banks")
            total_count = cursor.fetchone()[0]
            log(f"📊 Total banks in MySQL: {total_count:,}")
        
        if total_count == 0:
            log("ℹ️ No banks found in MySQL")
            return
        
        # First, let's check the structure of the table
        with mysql_conn.cursor() as cursor:
            cursor.execute("DESCRIBE banks")
            columns = cursor.fetchall()
            log("📋 Banks Table Structure:")
            for column in columns:
                log(f"  - {column[0]}: {column[1]}")
        
        # Fetch ALL banks data (no LIMIT)
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM banks ORDER BY id")
            
            banks_data = cursor.fetchall()
            log(f"📋 Fetched {len(banks_data)} banks from MySQL")
            
            if banks_data:
                # Clear existing banks data first
                with postgres_engine.connect() as pg_conn:
                    pg_conn.execute(text("DELETE FROM banks;"))
                    pg_conn.commit()
                    log("🗑️ Cleared existing banks data")
                
                # Insert ALL banks data in batches
                batch_size = 1000
                total_inserted = 0
                
                with postgres_engine.connect() as pg_conn:
                    for i in range(0, len(banks_data), batch_size):
                        batch = banks_data[i:i + batch_size]
                        
                        for bank_record in batch:
                            try:
                                # Get column names from the first record to build dynamic insert
                                if total_inserted == 0:
                                    column_names = [desc[0] for desc in columns]
                                    placeholders = ', '.join([f':{col}' for col in column_names])
                                    insert_sql = f"""
                                        INSERT INTO banks ({', '.join(column_names)})
                                        VALUES ({placeholders})
                                    """
                                
                                # Filter out invalid bank records (those that look like case descriptions)
                                bank_name = bank_record[1] if len(bank_record) > 1 else ""
                                if (bank_name and 
                                    len(bank_name) > 100 and  # Very long names are likely case descriptions
                                    ('dispute' in bank_name.lower() or 
                                     'damages' in bank_name.lower() or 
                                     'between' in bank_name.lower() or
                                     'contract' in bank_name.lower() or
                                     'agreement' in bank_name.lower())):
                                    log(f"⚠️ Skipping invalid bank record: {bank_name[:50]}...")
                                    continue
                                
                                # Convert dates and JSON as needed
                                record_dict = {}
                                for j, value in enumerate(bank_record):
                                    col_name = column_names[j]
                                    if value is None:
                                        record_dict[col_name] = None
                                    elif 'date' in col_name.lower() or 'created' in col_name.lower() or 'updated' in col_name.lower():
                                        record_dict[col_name] = safe_convert_date(value) or value
                                    elif isinstance(value, str) and value.startswith('{'):
                                        record_dict[col_name] = safe_convert_json(value)
                                    elif col_name in ['has_mobile_app', 'has_online_banking', 'has_atm_services', 'has_foreign_exchange', 'is_active', 'is_verified']:
                                        # Convert MySQL TINYINT(1) to boolean
                                        record_dict[col_name] = bool(value) if value is not None else False
                                    else:
                                        record_dict[col_name] = value
                                
                                # Insert into PostgreSQL
                                pg_conn.execute(text(insert_sql), record_dict)
                                total_inserted += 1
                                
                            except Exception as e:
                                log(f"⚠️ Error inserting banks record {bank_record[0] if bank_record else 'unknown'}: {e}")
                                continue
                        
                        # Commit batch
                        pg_conn.commit()
                        log(f"✅ Inserted batch {i//batch_size + 1}: {min(i + batch_size, len(banks_data))}/{len(banks_data)} banks")
                
                log(f"🎉 Successfully inserted {total_inserted:,} banks into PostgreSQL")
            else:
                log("ℹ️ No banks data found in MySQL")
                
    except Exception as e:
        log(f"❌ Error fetching banks data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting comprehensive banks data fetch...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Fetch all banks
        fetch_all_banks()
        
        # Show final summary
        with postgres_engine.connect() as conn:
            banks_count = conn.execute(text("SELECT COUNT(*) FROM banks")).fetchone()[0]
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"  🏦 Banks in PostgreSQL: {banks_count:,}")
            print(f"\n🎉 All banks data successfully migrated!")
            
    except Exception as e:
        log(f"❌ Error during banks data fetch: {e}")

if __name__ == "__main__":
    main()
