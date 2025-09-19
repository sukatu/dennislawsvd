#!/usr/bin/env python3
"""
Script to fetch ALL bank_analytics data from MySQL to PostgreSQL
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

def fetch_all_bank_analytics():
    """Fetch ALL bank_analytics data from MySQL to PostgreSQL"""
    log("🏦 Fetching ALL bank_analytics data from MySQL...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get total count first
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM bank_analytics")
            total_count = cursor.fetchone()[0]
            log(f"📊 Total bank_analytics in MySQL: {total_count:,}")
        
        if total_count == 0:
            log("ℹ️ No bank_analytics found in MySQL")
            return
        
        # Fetch ALL bank_analytics data (no LIMIT)
        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, bank_id, risk_score, risk_level, risk_factors, total_monetary_amount, 
                       average_case_value, financial_risk_level, primary_subject_matter, 
                       subject_matter_categories, legal_issues, financial_terms, 
                       regulatory_compliance_score, customer_dispute_rate, operational_risk_score, 
                       credit_risk_exposure, case_complexity_score, success_rate, last_updated, created_at
                FROM bank_analytics 
                ORDER BY id
            """)
            
            analytics_data = cursor.fetchall()
            log(f"📋 Fetched {len(analytics_data)} bank_analytics from MySQL")
            
            if analytics_data:
                # Clear existing bank_analytics data first
                with postgres_engine.connect() as pg_conn:
                    pg_conn.execute(text("DELETE FROM bank_analytics;"))
                    pg_conn.commit()
                    log("🗑️ Cleared existing bank_analytics data")
                
                # Insert ALL bank_analytics data in batches
                batch_size = 1000
                total_inserted = 0
                
                with postgres_engine.connect() as pg_conn:
                    for i in range(0, len(analytics_data), batch_size):
                        batch = analytics_data[i:i + batch_size]
                        
                        for analytics_record in batch:
                            try:
                                # Convert dates
                                last_updated = safe_convert_date(analytics_record[18])
                                created_at = safe_convert_date(analytics_record[19]) or datetime.now()
                                
                                # Convert JSON strings
                                risk_factors = safe_convert_json(analytics_record[4])
                                subject_matter_categories = safe_convert_json(analytics_record[9])
                                legal_issues = safe_convert_json(analytics_record[10])
                                financial_terms = safe_convert_json(analytics_record[11])
                                
                                # Insert into PostgreSQL
                                pg_conn.execute(text("""
                                    INSERT INTO bank_analytics (
                                        id, bank_id, risk_score, risk_level, risk_factors, total_monetary_amount, 
                                        average_case_value, financial_risk_level, primary_subject_matter, 
                                        subject_matter_categories, legal_issues, financial_terms, 
                                        regulatory_compliance_score, customer_dispute_rate, operational_risk_score, 
                                        credit_risk_exposure, case_complexity_score, success_rate, last_updated, created_at
                                    ) VALUES (
                                        :id, :bank_id, :risk_score, :risk_level, :risk_factors, :total_monetary_amount, 
                                        :average_case_value, :financial_risk_level, :primary_subject_matter, 
                                        :subject_matter_categories, :legal_issues, :financial_terms, 
                                        :regulatory_compliance_score, :customer_dispute_rate, :operational_risk_score, 
                                        :credit_risk_exposure, :case_complexity_score, :success_rate, :last_updated, :created_at
                                    )
                                """), {
                                    'id': analytics_record[0],
                                    'bank_id': analytics_record[1],
                                    'risk_score': analytics_record[2],
                                    'risk_level': analytics_record[3],
                                    'risk_factors': json.dumps(risk_factors) if risk_factors else None,
                                    'total_monetary_amount': float(analytics_record[5]) if analytics_record[5] else None,
                                    'average_case_value': float(analytics_record[6]) if analytics_record[6] else None,
                                    'financial_risk_level': analytics_record[7],
                                    'primary_subject_matter': analytics_record[8],
                                    'subject_matter_categories': json.dumps(subject_matter_categories) if subject_matter_categories else None,
                                    'legal_issues': json.dumps(legal_issues) if legal_issues else None,
                                    'financial_terms': json.dumps(financial_terms) if financial_terms else None,
                                    'regulatory_compliance_score': analytics_record[12],
                                    'customer_dispute_rate': float(analytics_record[13]) if analytics_record[13] else None,
                                    'operational_risk_score': analytics_record[14],
                                    'credit_risk_exposure': float(analytics_record[15]) if analytics_record[15] else None,
                                    'case_complexity_score': analytics_record[16],
                                    'success_rate': float(analytics_record[17]) if analytics_record[17] else None,
                                    'last_updated': last_updated,
                                    'created_at': created_at
                                })
                                total_inserted += 1
                                
                            except Exception as e:
                                log(f"⚠️ Error inserting bank_analytics {analytics_record[0]}: {e}")
                                continue
                        
                        # Commit batch
                        pg_conn.commit()
                        log(f"✅ Inserted batch {i//batch_size + 1}: {min(i + batch_size, len(analytics_data))}/{len(analytics_data)} bank_analytics")
                
                log(f"🎉 Successfully inserted {total_inserted:,} bank_analytics into PostgreSQL")
            else:
                log("ℹ️ No bank_analytics data found in MySQL")
                
    except Exception as e:
        log(f"❌ Error fetching bank_analytics data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting comprehensive bank_analytics data fetch...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Fetch all bank_analytics
        fetch_all_bank_analytics()
        
        # Show final summary
        with postgres_engine.connect() as conn:
            analytics_count = conn.execute(text("SELECT COUNT(*) FROM bank_analytics")).fetchone()[0]
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"  🏦 Bank Analytics in PostgreSQL: {analytics_count:,}")
            print(f"\n🎉 All bank_analytics data successfully migrated!")
            
    except Exception as e:
        log(f"❌ Error during bank_analytics data fetch: {e}")

if __name__ == "__main__":
    main()
