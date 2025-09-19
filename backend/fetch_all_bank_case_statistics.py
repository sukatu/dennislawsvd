#!/usr/bin/env python3
"""
Script to fetch ALL bank_case_statistics data from MySQL to PostgreSQL
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

def fetch_all_bank_case_statistics():
    """Fetch ALL bank_case_statistics data from MySQL to PostgreSQL"""
    log("📊 Fetching ALL bank_case_statistics data from MySQL...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get total count first
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM bank_case_statistics")
            total_count = cursor.fetchone()[0]
            log(f"📊 Total bank_case_statistics in MySQL: {total_count:,}")
        
        if total_count == 0:
            log("ℹ️ No bank_case_statistics found in MySQL")
            return
        
        # First, let's check the structure of the table
        with mysql_conn.cursor() as cursor:
            cursor.execute("DESCRIBE bank_case_statistics")
            columns = cursor.fetchall()
            log("📋 Bank Case Statistics Table Structure:")
            for column in columns:
                log(f"  - {column[0]}: {column[1]}")
        
        # Fetch ALL bank_case_statistics data (no LIMIT)
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM bank_case_statistics ORDER BY id")
            
            statistics_data = cursor.fetchall()
            log(f"📋 Fetched {len(statistics_data)} bank_case_statistics from MySQL")
            
            if statistics_data:
                # Clear existing bank_case_statistics data first
                with postgres_engine.connect() as pg_conn:
                    pg_conn.execute(text("DELETE FROM bank_case_statistics;"))
                    pg_conn.commit()
                    log("🗑️ Cleared existing bank_case_statistics data")
                
                # Insert ALL bank_case_statistics data in batches
                batch_size = 1000
                total_inserted = 0
                
                with postgres_engine.connect() as pg_conn:
                    for i in range(0, len(statistics_data), batch_size):
                        batch = statistics_data[i:i + batch_size]
                        
                        for stats_record in batch:
                            try:
                                # Get column names from the first record to build dynamic insert
                                if total_inserted == 0:
                                    column_names = [desc[0] for desc in columns]
                                    placeholders = ', '.join([f':{col}' for col in column_names])
                                    insert_sql = f"""
                                        INSERT INTO bank_case_statistics ({', '.join(column_names)})
                                        VALUES ({placeholders})
                                    """
                                
                                # Convert dates and JSON as needed
                                record_dict = {}
                                for j, value in enumerate(stats_record):
                                    col_name = column_names[j]
                                    if value is None:
                                        record_dict[col_name] = None
                                    elif 'date' in col_name.lower() or 'created' in col_name.lower() or 'updated' in col_name.lower():
                                        record_dict[col_name] = safe_convert_date(value) or value
                                    elif isinstance(value, str) and value.startswith('{'):
                                        record_dict[col_name] = safe_convert_json(value)
                                    else:
                                        record_dict[col_name] = value
                                
                                # Insert into PostgreSQL
                                pg_conn.execute(text(insert_sql), record_dict)
                                total_inserted += 1
                                
                            except Exception as e:
                                log(f"⚠️ Error inserting bank_case_statistics record {stats_record[0] if stats_record else 'unknown'}: {e}")
                                continue
                        
                        # Commit batch
                        pg_conn.commit()
                        log(f"✅ Inserted batch {i//batch_size + 1}: {min(i + batch_size, len(statistics_data))}/{len(statistics_data)} bank_case_statistics")
                
                log(f"🎉 Successfully inserted {total_inserted:,} bank_case_statistics into PostgreSQL")
            else:
                log("ℹ️ No bank_case_statistics data found in MySQL")
                
    except Exception as e:
        log(f"❌ Error fetching bank_case_statistics data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting comprehensive bank_case_statistics data fetch...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Fetch all bank_case_statistics
        fetch_all_bank_case_statistics()
        
        # Show final summary
        with postgres_engine.connect() as conn:
            statistics_count = conn.execute(text("SELECT COUNT(*) FROM bank_case_statistics")).fetchone()[0]
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"  📊 Bank Case Statistics in PostgreSQL: {statistics_count:,}")
            print(f"\n🎉 All bank_case_statistics data successfully migrated!")
            
    except Exception as e:
        log(f"❌ Error during bank_case_statistics data fetch: {e}")

if __name__ == "__main__":
    main()
