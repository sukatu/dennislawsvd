#!/usr/bin/env python3
"""
Script to fetch ALL case_hearings data from MySQL to PostgreSQL
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

def fetch_all_case_hearings():
    """Fetch ALL case_hearings data from MySQL to PostgreSQL"""
    log("⚖️ Fetching ALL case_hearings data from MySQL...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get total count first
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM case_hearings")
            total_count = cursor.fetchone()[0]
            log(f"📊 Total case_hearings in MySQL: {total_count:,}")
        
        if total_count == 0:
            log("ℹ️ No case_hearings found in MySQL")
            return
        
        # First, let's check the structure of the table
        with mysql_conn.cursor() as cursor:
            cursor.execute("DESCRIBE case_hearings")
            columns = cursor.fetchall()
            log("📋 Case Hearings Table Structure:")
            for column in columns:
                log(f"  - {column[0]}: {column[1]}")
        
        # Fetch ALL case_hearings data (no LIMIT)
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM case_hearings ORDER BY id")
            
            hearings_data = cursor.fetchall()
            log(f"📋 Fetched {len(hearings_data)} case_hearings from MySQL")
            
            if hearings_data:
                # Clear existing case_hearings data first
                with postgres_engine.connect() as pg_conn:
                    pg_conn.execute(text("DELETE FROM case_hearings;"))
                    pg_conn.commit()
                    log("🗑️ Cleared existing case_hearings data")
                
                # Insert ALL case_hearings data in batches
                batch_size = 1000
                total_inserted = 0
                
                with postgres_engine.connect() as pg_conn:
                    for i in range(0, len(hearings_data), batch_size):
                        batch = hearings_data[i:i + batch_size]
                        
                        for hearing_record in batch:
                            try:
                                # Get column names from the first record to build dynamic insert
                                if total_inserted == 0:
                                    column_names = [desc[0] for desc in columns]
                                    placeholders = ', '.join([f':{col}' for col in column_names])
                                    insert_sql = f"""
                                        INSERT INTO case_hearings ({', '.join(column_names)})
                                        VALUES ({placeholders})
                                    """
                                
                                # Convert dates and JSON as needed
                                record_dict = {}
                                for j, value in enumerate(hearing_record):
                                    col_name = column_names[j]
                                    if value is None:
                                        record_dict[col_name] = None
                                    elif 'date' in col_name.lower() or 'created' in col_name.lower() or 'updated' in col_name.lower():
                                        record_dict[col_name] = safe_convert_date(value) or value
                                    elif isinstance(value, str) and value.startswith('{'):
                                        record_dict[col_name] = safe_convert_json(value)
                                    else:
                                        record_dict[col_name] = value
                                
                                # Insert into PostgreSQL with individual transaction
                                with pg_conn.begin():
                                    pg_conn.execute(text(insert_sql), record_dict)
                                total_inserted += 1
                                
                            except Exception as e:
                                log(f"⚠️ Error inserting case_hearings record {hearing_record[0] if hearing_record else 'unknown'}: {e}")
                                continue
                        
                        log(f"✅ Inserted batch {i//batch_size + 1}: {min(i + batch_size, len(hearings_data))}/{len(hearings_data)} case_hearings")
                
                log(f"🎉 Successfully inserted {total_inserted:,} case_hearings into PostgreSQL")
            else:
                log("ℹ️ No case_hearings data found in MySQL")
                
    except Exception as e:
        log(f"❌ Error fetching case_hearings data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting comprehensive case_hearings data fetch...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Fetch all case_hearings
        fetch_all_case_hearings()
        
        # Show final summary
        with postgres_engine.connect() as conn:
            hearings_count = conn.execute(text("SELECT COUNT(*) FROM case_hearings")).fetchone()[0]
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"  ⚖️ Case Hearings in PostgreSQL: {hearings_count:,}")
            print(f"\n🎉 All case_hearings data successfully migrated!")
            
    except Exception as e:
        log(f"❌ Error during case_hearings data fetch: {e}")

if __name__ == "__main__":
    main()
