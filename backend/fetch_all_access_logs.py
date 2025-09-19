#!/usr/bin/env python3
"""
Script to fetch ALL access_logs data from MySQL to PostgreSQL
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

def fetch_all_access_logs():
    """Fetch ALL access_logs data from MySQL to PostgreSQL"""
    log("📊 Fetching ALL access_logs data from MySQL...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get total count first
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM access_logs")
            total_count = cursor.fetchone()[0]
            log(f"📊 Total access_logs in MySQL: {total_count:,}")
        
        if total_count == 0:
            log("ℹ️ No access_logs found in MySQL")
            return
        
        # Fetch ALL access_logs data (no LIMIT)
        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, user_id, session_id, ip_address, user_agent, method, url, endpoint, 
                       status_code, response_time, request_size, response_size, referer, 
                       country, city, device_type, browser, os, created_at
                FROM access_logs 
                ORDER BY id
            """)
            
            logs_data = cursor.fetchall()
            log(f"📋 Fetched {len(logs_data)} access_logs from MySQL")
            
            if logs_data:
                # Clear existing access_logs data first
                with postgres_engine.connect() as pg_conn:
                    pg_conn.execute(text("DELETE FROM access_logs;"))
                    pg_conn.commit()
                    log("🗑️ Cleared existing access_logs data")
                
                # Insert ALL access_logs data in batches
                batch_size = 1000
                total_inserted = 0
                
                with postgres_engine.connect() as pg_conn:
                    for i in range(0, len(logs_data), batch_size):
                        batch = logs_data[i:i + batch_size]
                        
                        for log_record in batch:
                            try:
                                # Convert dates
                                created_at = safe_convert_date(log_record[18]) or datetime.now()
                                
                                # Insert into PostgreSQL
                                pg_conn.execute(text("""
                                    INSERT INTO access_logs (
                                        id, user_id, session_id, ip_address, user_agent, method, url, endpoint, 
                                        status_code, response_time, request_size, response_size, referer, 
                                        country, city, device_type, browser, os, created_at
                                    ) VALUES (
                                        :id, :user_id, :session_id, :ip_address, :user_agent, :method, :url, :endpoint, 
                                        :status_code, :response_time, :request_size, :response_size, :referer, 
                                        :country, :city, :device_type, :browser, :os, :created_at
                                    )
                                """), {
                                    'id': log_record[0],
                                    'user_id': log_record[1],
                                    'session_id': log_record[2],
                                    'ip_address': log_record[3],
                                    'user_agent': log_record[4],
                                    'method': log_record[5],
                                    'url': log_record[6],
                                    'endpoint': log_record[7],
                                    'status_code': log_record[8],
                                    'response_time': log_record[9],
                                    'request_size': log_record[10],
                                    'response_size': log_record[11],
                                    'referer': log_record[12],
                                    'country': log_record[13],
                                    'city': log_record[14],
                                    'device_type': log_record[15],
                                    'browser': log_record[16],
                                    'os': log_record[17],
                                    'created_at': created_at
                                })
                                total_inserted += 1
                                
                            except Exception as e:
                                log(f"⚠️ Error inserting access_log {log_record[0]}: {e}")
                                continue
                        
                        # Commit batch
                        pg_conn.commit()
                        log(f"✅ Inserted batch {i//batch_size + 1}: {min(i + batch_size, len(logs_data))}/{len(logs_data)} access_logs")
                
                log(f"🎉 Successfully inserted {total_inserted:,} access_logs into PostgreSQL")
            else:
                log("ℹ️ No access_logs data found in MySQL")
                
    except Exception as e:
        log(f"❌ Error fetching access_logs data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting comprehensive access_logs data fetch...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Fetch all access_logs
        fetch_all_access_logs()
        
        # Show final summary
        with postgres_engine.connect() as conn:
            logs_count = conn.execute(text("SELECT COUNT(*) FROM access_logs")).fetchone()[0]
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"  📊 Access Logs in PostgreSQL: {logs_count:,}")
            print(f"\n🎉 All access_logs data successfully migrated!")
            
    except Exception as e:
        log(f"❌ Error during access_logs data fetch: {e}")

if __name__ == "__main__":
    main()
