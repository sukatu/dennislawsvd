#!/usr/bin/env python3
"""
Script to fetch ALL activity_logs data from MySQL to PostgreSQL
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

def fetch_all_activity_logs():
    """Fetch ALL activity_logs data from MySQL to PostgreSQL"""
    log("📊 Fetching ALL activity_logs data from MySQL...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get total count first
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM activity_logs")
            total_count = cursor.fetchone()[0]
            log(f"📊 Total activity_logs in MySQL: {total_count:,}")
        
        if total_count == 0:
            log("ℹ️ No activity_logs found in MySQL")
            return
        
        # Fetch ALL activity_logs data (no LIMIT)
        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, user_id, session_id, activity_type, action, description, resource_type, 
                       resource_id, old_values, new_values, ip_address, user_agent, log_metadata, 
                       severity, created_at
                FROM activity_logs 
                ORDER BY id
            """)
            
            logs_data = cursor.fetchall()
            log(f"📋 Fetched {len(logs_data)} activity_logs from MySQL")
            
            if logs_data:
                # Clear existing activity_logs data first
                with postgres_engine.connect() as pg_conn:
                    pg_conn.execute(text("DELETE FROM activity_logs;"))
                    pg_conn.commit()
                    log("🗑️ Cleared existing activity_logs data")
                
                # Insert ALL activity_logs data in batches
                batch_size = 1000
                total_inserted = 0
                
                with postgres_engine.connect() as pg_conn:
                    for i in range(0, len(logs_data), batch_size):
                        batch = logs_data[i:i + batch_size]
                        
                        for log_record in batch:
                            try:
                                # Convert dates
                                created_at = safe_convert_date(log_record[14]) or datetime.now()
                                
                                # Convert JSON strings
                                old_values = safe_convert_json(log_record[8])
                                new_values = safe_convert_json(log_record[9])
                                log_metadata = safe_convert_json(log_record[12])
                                
                                # Insert into PostgreSQL
                                pg_conn.execute(text("""
                                    INSERT INTO activity_logs (
                                        id, user_id, session_id, activity_type, action, description, resource_type, 
                                        resource_id, old_values, new_values, ip_address, user_agent, log_metadata, 
                                        severity, created_at
                                    ) VALUES (
                                        :id, :user_id, :session_id, :activity_type, :action, :description, :resource_type, 
                                        :resource_id, :old_values, :new_values, :ip_address, :user_agent, :log_metadata, 
                                        :severity, :created_at
                                    )
                                """), {
                                    'id': log_record[0],
                                    'user_id': log_record[1],
                                    'session_id': log_record[2],
                                    'activity_type': log_record[3],
                                    'action': log_record[4],
                                    'description': log_record[5],
                                    'resource_type': log_record[6],
                                    'resource_id': log_record[7],
                                    'old_values': json.dumps(old_values) if old_values else None,
                                    'new_values': json.dumps(new_values) if new_values else None,
                                    'ip_address': log_record[10],
                                    'user_agent': log_record[11],
                                    'log_metadata': json.dumps(log_metadata) if log_metadata else None,
                                    'severity': log_record[13],
                                    'created_at': created_at
                                })
                                total_inserted += 1
                                
                            except Exception as e:
                                log(f"⚠️ Error inserting activity_log {log_record[0]}: {e}")
                                continue
                        
                        # Commit batch
                        pg_conn.commit()
                        log(f"✅ Inserted batch {i//batch_size + 1}: {min(i + batch_size, len(logs_data))}/{len(logs_data)} activity_logs")
                
                log(f"🎉 Successfully inserted {total_inserted:,} activity_logs into PostgreSQL")
            else:
                log("ℹ️ No activity_logs data found in MySQL")
                
    except Exception as e:
        log(f"❌ Error fetching activity_logs data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting comprehensive activity_logs data fetch...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Fetch all activity_logs
        fetch_all_activity_logs()
        
        # Show final summary
        with postgres_engine.connect() as conn:
            logs_count = conn.execute(text("SELECT COUNT(*) FROM activity_logs")).fetchone()[0]
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"  📊 Activity Logs in PostgreSQL: {logs_count:,}")
            print(f"\n🎉 All activity_logs data successfully migrated!")
            
    except Exception as e:
        log(f"❌ Error during activity_logs data fetch: {e}")

if __name__ == "__main__":
    main()
