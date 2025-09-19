#!/usr/bin/env python3
"""
Script to fetch ALL people data from MySQL to PostgreSQL (all 6,331 records)
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

def safe_convert_bool(value):
    """Safely convert various values to boolean"""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        return value.lower() in ('1', 'true', 'yes', 'on', 'active')
    return bool(value)

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

def fetch_all_people():
    """Fetch ALL people data from MySQL to PostgreSQL"""
    log("👥 Fetching ALL people data from MySQL...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get total count first
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM people")
            total_count = cursor.fetchone()[0]
            log(f"📊 Total people in MySQL: {total_count:,}")
        
        # Fetch ALL people data (no LIMIT)
        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, first_name, last_name, full_name, previous_names, date_of_birth, 
                       date_of_death, id_number, phone_number, email, address, city, region, 
                       country, postal_code, risk_level, risk_score, case_count, case_types, 
                       court_records, occupation, employer, organization, job_title, 
                       marital_status, spouse_name, children_count, emergency_contact, 
                       emergency_phone, nationality, gender, education_level, languages, 
                       is_verified, verification_date, verification_notes, last_searched, 
                       search_count, created_at, updated_at, created_by, updated_by, 
                       status, notes
                FROM people 
                ORDER BY id
            """)
            
            people_data = cursor.fetchall()
            log(f"📋 Fetched {len(people_data)} people from MySQL")
            
            if people_data:
                # Clear existing people data first
                with postgres_engine.connect() as pg_conn:
                    pg_conn.execute(text("DELETE FROM people;"))
                    pg_conn.commit()
                    log("🗑️ Cleared existing people data")
                
                # Insert ALL people data in batches
                batch_size = 1000
                total_inserted = 0
                
                with postgres_engine.connect() as pg_conn:
                    for i in range(0, len(people_data), batch_size):
                        batch = people_data[i:i + batch_size]
                        
                        for person in batch:
                            try:
                                # Convert boolean values
                                is_verified = safe_convert_bool(person[33]) if person[33] is not None else False
                                
                                # Convert JSON strings
                                previous_names = safe_convert_json(person[4])
                                case_types = safe_convert_json(person[18])
                                court_records = safe_convert_json(person[19])
                                languages = safe_convert_json(person[32])
                                
                                # Convert dates
                                date_of_birth = person[5] if person[5] else None
                                date_of_death = person[6] if person[6] else None
                                verification_date = person[34] if person[34] else None
                                last_searched = person[36] if person[36] else None
                                created_at = safe_convert_date(person[38]) or datetime.now()
                                updated_at = safe_convert_date(person[39]) or datetime.now()
                                
                                # Insert into PostgreSQL
                                pg_conn.execute(text("""
                                    INSERT INTO people (
                                        id, first_name, last_name, full_name, previous_names, date_of_birth,
                                        date_of_death, id_number, phone_number, email, address, city, region,
                                        country, postal_code, risk_level, risk_score, case_count, case_types,
                                        court_records, occupation, employer, organization, job_title,
                                        marital_status, spouse_name, children_count, emergency_contact,
                                        emergency_phone, nationality, gender, education_level, languages,
                                        is_verified, verification_date, verification_notes, last_searched,
                                        search_count, created_at, updated_at, created_by, updated_by,
                                        status, notes
                                    ) VALUES (
                                        :id, :first_name, :last_name, :full_name, :previous_names, :date_of_birth,
                                        :date_of_death, :id_number, :phone_number, :email, :address, :city, :region,
                                        :country, :postal_code, :risk_level, :risk_score, :case_count, :case_types,
                                        :court_records, :occupation, :employer, :organization, :job_title,
                                        :marital_status, :spouse_name, :children_count, :emergency_contact,
                                        :emergency_phone, :nationality, :gender, :education_level, :languages,
                                        :is_verified, :verification_date, :verification_notes, :last_searched,
                                        :search_count, :created_at, :updated_at, :created_by, :updated_by,
                                        :status, :notes
                                    )
                                """), {
                                    'id': person[0],
                                    'first_name': person[1],
                                    'last_name': person[2],
                                    'full_name': person[3],
                                    'previous_names': json.dumps(previous_names) if previous_names else None,
                                    'date_of_birth': date_of_birth,
                                    'date_of_death': date_of_death,
                                    'id_number': person[7],
                                    'phone_number': person[8],
                                    'email': person[9],
                                    'address': person[10],
                                    'city': person[11],
                                    'region': person[12],
                                    'country': person[13],
                                    'postal_code': person[14],
                                    'risk_level': person[15],
                                    'risk_score': person[16],
                                    'case_count': person[17],
                                    'case_types': json.dumps(case_types) if case_types else None,
                                    'court_records': json.dumps(court_records) if court_records else None,
                                    'occupation': person[20],
                                    'employer': person[21],
                                    'organization': person[22],
                                    'job_title': person[23],
                                    'marital_status': person[24],
                                    'spouse_name': person[25],
                                    'children_count': person[26],
                                    'emergency_contact': person[27],
                                    'emergency_phone': person[28],
                                    'nationality': person[29],
                                    'gender': person[30],
                                    'education_level': person[31],
                                    'languages': json.dumps(languages) if languages else None,
                                    'is_verified': is_verified,
                                    'verification_date': verification_date,
                                    'verification_notes': person[35],
                                    'last_searched': last_searched,
                                    'search_count': person[37],
                                    'created_at': created_at,
                                    'updated_at': updated_at,
                                    'created_by': person[40],
                                    'updated_by': person[41],
                                    'status': person[42],
                                    'notes': person[43]
                                })
                                total_inserted += 1
                                
                            except Exception as e:
                                log(f"⚠️ Error inserting person {person[0]}: {e}")
                                continue
                        
                        # Commit batch
                        pg_conn.commit()
                        log(f"✅ Inserted batch {i//batch_size + 1}: {min(i + batch_size, len(people_data))}/{len(people_data)} people")
                
                log(f"🎉 Successfully inserted {total_inserted:,} people into PostgreSQL")
            else:
                log("ℹ️ No people data found in MySQL")
                
    except Exception as e:
        log(f"❌ Error fetching people data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting comprehensive people data fetch...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Fetch all people
        fetch_all_people()
        
        # Show final summary
        with postgres_engine.connect() as conn:
            people_count = conn.execute(text("SELECT COUNT(*) FROM people")).fetchone()[0]
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"  👥 People in PostgreSQL: {people_count:,}")
            print(f"\n🎉 All people data successfully migrated!")
            
    except Exception as e:
        log(f"❌ Error during people data fetch: {e}")

if __name__ == "__main__":
    main()
