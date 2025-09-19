#!/usr/bin/env python3
"""
Script to populate PostgreSQL tables with real data from MySQL
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
    from urllib.parse import quote_plus
    password = quote_plus(MYSQL_PASSWORD)
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

def populate_people_data():
    """Populate people table with real MySQL data"""
    log("👥 Populating people table...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get people data from MySQL
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
                LIMIT 100
            """)
            
            people_data = cursor.fetchall()
            log(f"📊 Found {len(people_data)} people in MySQL")
            
            if people_data:
                # Insert into PostgreSQL
                with postgres_engine.connect() as pg_conn:
                    for person in people_data:
                        # Convert boolean values
                        is_verified = bool(person[33]) if person[33] is not None else False
                        
                        # Convert JSON strings
                        previous_names = json.loads(person[4]) if person[4] else None
                        case_types = json.loads(person[18]) if person[18] else None
                        court_records = json.loads(person[19]) if person[19] else None
                        languages = json.loads(person[32]) if person[32] else None
                        
                        # Convert dates
                        date_of_birth = person[5] if person[5] else None
                        date_of_death = person[6] if person[6] else None
                        verification_date = person[34] if person[34] else None
                        last_searched = person[36] if person[36] else None
                        created_at = person[38] if person[38] else datetime.now()
                        updated_at = person[39] if person[39] else datetime.now()
                        
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
                            ) ON CONFLICT (id) DO NOTHING
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
                    
                    pg_conn.commit()
                    log(f"✅ Successfully inserted {len(people_data)} people into PostgreSQL")
            
    except Exception as e:
        log(f"❌ Error populating people data: {e}")
    finally:
        mysql_conn.close()

def populate_companies_data():
    """Populate companies table with real MySQL data"""
    log("🏭 Populating companies table...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get companies data from MySQL
        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, short_name, website, phone, email, address, city, region,
                       country, postal_code, type_of_company, district, date_of_incorporation,
                       date_of_commencement, nature_of_business, registration_number,
                       tax_identification_number, directors, authorized_shares, stated_capital,
                       tin_number, established_date, company_type, industry, ownership_type,
                       annual_revenue, net_worth, employee_count, rating, is_active, is_verified,
                       status, created_at, updated_at, created_by, updated_by
                FROM companies 
                LIMIT 50
            """)
            
            companies_data = cursor.fetchall()
            log(f"📊 Found {len(companies_data)} companies in MySQL")
            
            if companies_data:
                # Insert into PostgreSQL
                with postgres_engine.connect() as pg_conn:
                    for company in companies_data:
                        # Convert boolean values
                        is_active = bool(company[29]) if company[29] is not None else True
                        is_verified = bool(company[30]) if company[30] is not None else False
                        
                        # Convert JSON strings
                        directors = json.loads(company[18]) if company[18] else None
                        
                        # Convert dates
                        date_of_incorporation = company[13] if company[13] else None
                        date_of_commencement = company[14] if company[14] else None
                        established_date = company[22] if company[22] else None
                        created_at = company[32] if company[32] else datetime.now()
                        updated_at = company[33] if company[33] else datetime.now()
                        
                        # Insert into PostgreSQL
                        pg_conn.execute(text("""
                            INSERT INTO companies (
                                id, name, short_name, website, phone, email, address, city, region,
                                country, postal_code, type_of_company, district, date_of_incorporation,
                                date_of_commencement, nature_of_business, registration_number,
                                tax_identification_number, directors, authorized_shares, stated_capital,
                                tin_number, established_date, company_type, industry, ownership_type,
                                annual_revenue, net_worth, employee_count, rating, is_active, is_verified,
                                status, created_at, updated_at, created_by, updated_by
                            ) VALUES (
                                :id, :name, :short_name, :website, :phone, :email, :address, :city, :region,
                                :country, :postal_code, :type_of_company, :district, :date_of_incorporation,
                                :date_of_commencement, :nature_of_business, :registration_number,
                                :tax_identification_number, :directors, :authorized_shares, :stated_capital,
                                :tin_number, :established_date, :company_type, :industry, :ownership_type,
                                :annual_revenue, :net_worth, :employee_count, :rating, :is_active, :is_verified,
                                :status, :created_at, :updated_at, :created_by, :updated_by
                            ) ON CONFLICT (id) DO NOTHING
                        """), {
                            'id': company[0],
                            'name': company[1],
                            'short_name': company[2],
                            'website': company[3],
                            'phone': company[4],
                            'email': company[5],
                            'address': company[6],
                            'city': company[7],
                            'region': company[8],
                            'country': company[9],
                            'postal_code': company[10],
                            'type_of_company': company[11],
                            'district': company[12],
                            'date_of_incorporation': date_of_incorporation,
                            'date_of_commencement': date_of_commencement,
                            'nature_of_business': company[15],
                            'registration_number': company[16],
                            'tax_identification_number': company[17],
                            'directors': json.dumps(directors) if directors else None,
                            'authorized_shares': company[19],
                            'stated_capital': company[20],
                            'tin_number': company[21],
                            'established_date': established_date,
                            'company_type': company[23],
                            'industry': company[24],
                            'ownership_type': company[25],
                            'annual_revenue': company[26],
                            'net_worth': company[27],
                            'employee_count': company[28],
                            'rating': company[29],
                            'is_active': is_active,
                            'is_verified': is_verified,
                            'status': company[31],
                            'created_at': created_at,
                            'updated_at': updated_at,
                            'created_by': company[34],
                            'updated_by': company[35]
                        })
                    
                    pg_conn.commit()
                    log(f"✅ Successfully inserted {len(companies_data)} companies into PostgreSQL")
            
    except Exception as e:
        log(f"❌ Error populating companies data: {e}")
    finally:
        mysql_conn.close()

def populate_banks_data():
    """Populate banks table with real MySQL data"""
    log("🏦 Populating banks table...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get banks data from MySQL
        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, short_name, website, phone, email, address, city, region,
                       country, postal_code, license_number, registration_number, established_date,
                       bank_type, ownership_type, total_assets, net_worth, rating,
                       head_office_address, customer_service_phone, customer_service_email,
                       has_website, has_mobile_app, is_active, is_verified, status,
                       created_at, updated_at, created_by, updated_by
                FROM banks 
                LIMIT 50
            """)
            
            banks_data = cursor.fetchall()
            log(f"📊 Found {len(banks_data)} banks in MySQL")
            
            if banks_data:
                # Insert into PostgreSQL
                with postgres_engine.connect() as pg_conn:
                    for bank in banks_data:
                        # Convert boolean values
                        has_website = bool(bank[22]) if bank[22] is not None else False
                        has_mobile_app = bool(bank[23]) if bank[23] is not None else False
                        is_active = bool(bank[24]) if bank[24] is not None else True
                        is_verified = bool(bank[25]) if bank[25] is not None else False
                        
                        # Convert dates
                        established_date = bank[14] if bank[14] else None
                        created_at = bank[27] if bank[27] else datetime.now()
                        updated_at = bank[28] if bank[28] else datetime.now()
                        
                        # Insert into PostgreSQL
                        pg_conn.execute(text("""
                            INSERT INTO banks (
                                id, name, short_name, website, phone, email, address, city, region,
                                country, postal_code, license_number, registration_number, established_date,
                                bank_type, ownership_type, total_assets, net_worth, rating,
                                head_office_address, customer_service_phone, customer_service_email,
                                has_website, has_mobile_app, is_active, is_verified, status,
                                created_at, updated_at, created_by, updated_by
                            ) VALUES (
                                :id, :name, :short_name, :website, :phone, :email, :address, :city, :region,
                                :country, :postal_code, :license_number, :registration_number, :established_date,
                                :bank_type, :ownership_type, :total_assets, :net_worth, :rating,
                                :head_office_address, :customer_service_phone, :customer_service_email,
                                :has_website, :has_mobile_app, :is_active, :is_verified, :status,
                                :created_at, :updated_at, :created_by, :updated_by
                            ) ON CONFLICT (id) DO NOTHING
                        """), {
                            'id': bank[0],
                            'name': bank[1],
                            'short_name': bank[2],
                            'website': bank[3],
                            'phone': bank[4],
                            'email': bank[5],
                            'address': bank[6],
                            'city': bank[7],
                            'region': bank[8],
                            'country': bank[9],
                            'postal_code': bank[10],
                            'license_number': bank[11],
                            'registration_number': bank[12],
                            'established_date': established_date,
                            'bank_type': bank[15],
                            'ownership_type': bank[16],
                            'total_assets': bank[17],
                            'net_worth': bank[18],
                            'rating': bank[19],
                            'head_office_address': bank[20],
                            'customer_service_phone': bank[21],
                            'customer_service_email': bank[22],
                            'has_website': has_website,
                            'has_mobile_app': has_mobile_app,
                            'is_active': is_active,
                            'is_verified': is_verified,
                            'status': bank[26],
                            'created_at': created_at,
                            'updated_at': updated_at,
                            'created_by': bank[29],
                            'updated_by': bank[30]
                        })
                    
                    pg_conn.commit()
                    log(f"✅ Successfully inserted {len(banks_data)} banks into PostgreSQL")
            
    except Exception as e:
        log(f"❌ Error populating banks data: {e}")
    finally:
        mysql_conn.close()

def populate_insurance_data():
    """Populate insurance table with real MySQL data"""
    log("🛡️ Populating insurance table...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        # Get insurance data from MySQL
        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, short_name, website, phone, email, address, city, region,
                       country, postal_code, license_number, registration_number, established_date,
                       insurance_type, ownership_type, total_assets, net_worth, premium_income,
                       claims_paid, rating, head_office_address, customer_service_phone,
                       customer_service_email, claims_phone, claims_email, has_mobile_app,
                       has_online_portal, has_online_claims, has_24_7_support, is_active,
                       is_verified, status, created_at, updated_at, created_by, updated_by
                FROM insurance 
                LIMIT 50
            """)
            
            insurance_data = cursor.fetchall()
            log(f"📊 Found {len(insurance_data)} insurance companies in MySQL")
            
            if insurance_data:
                # Insert into PostgreSQL
                with postgres_engine.connect() as pg_conn:
                    for insurance in insurance_data:
                        # Convert boolean values
                        has_mobile_app = bool(insurance[27]) if insurance[27] is not None else False
                        has_online_portal = bool(insurance[28]) if insurance[28] is not None else False
                        has_online_claims = bool(insurance[29]) if insurance[29] is not None else False
                        has_24_7_support = bool(insurance[30]) if insurance[30] is not None else False
                        is_active = bool(insurance[31]) if insurance[31] is not None else True
                        is_verified = bool(insurance[32]) if insurance[32] is not None else False
                        
                        # Convert dates
                        established_date = insurance[14] if insurance[14] else None
                        created_at = insurance[33] if insurance[33] else datetime.now()
                        updated_at = insurance[34] if insurance[34] else datetime.now()
                        
                        # Insert into PostgreSQL
                        pg_conn.execute(text("""
                            INSERT INTO insurance (
                                id, name, short_name, website, phone, email, address, city, region,
                                country, postal_code, license_number, registration_number, established_date,
                                insurance_type, ownership_type, total_assets, net_worth, premium_income,
                                claims_paid, rating, head_office_address, customer_service_phone,
                                customer_service_email, claims_phone, claims_email, has_mobile_app,
                                has_online_portal, has_online_claims, has_24_7_support, is_active,
                                is_verified, status, created_at, updated_at, created_by, updated_by
                            ) VALUES (
                                :id, :name, :short_name, :website, :phone, :email, :address, :city, :region,
                                :country, :postal_code, :license_number, :registration_number, :established_date,
                                :insurance_type, :ownership_type, :total_assets, :net_worth, :premium_income,
                                :claims_paid, :rating, :head_office_address, :customer_service_phone,
                                :customer_service_email, :claims_phone, :claims_email, :has_mobile_app,
                                :has_online_portal, :has_online_claims, :has_24_7_support, :is_active,
                                :is_verified, :status, :created_at, :updated_at, :created_by, :updated_by
                            ) ON CONFLICT (id) DO NOTHING
                        """), {
                            'id': insurance[0],
                            'name': insurance[1],
                            'short_name': insurance[2],
                            'website': insurance[3],
                            'phone': insurance[4],
                            'email': insurance[5],
                            'address': insurance[6],
                            'city': insurance[7],
                            'region': insurance[8],
                            'country': insurance[9],
                            'postal_code': insurance[10],
                            'license_number': insurance[11],
                            'registration_number': insurance[12],
                            'established_date': established_date,
                            'insurance_type': insurance[15],
                            'ownership_type': insurance[16],
                            'total_assets': insurance[17],
                            'net_worth': insurance[18],
                            'premium_income': insurance[19],
                            'claims_paid': insurance[20],
                            'rating': insurance[21],
                            'head_office_address': insurance[22],
                            'customer_service_phone': insurance[23],
                            'customer_service_email': insurance[24],
                            'claims_phone': insurance[25],
                            'claims_email': insurance[26],
                            'has_mobile_app': has_mobile_app,
                            'has_online_portal': has_online_portal,
                            'has_online_claims': has_online_claims,
                            'has_24_7_support': has_24_7_support,
                            'is_active': is_active,
                            'is_verified': is_verified,
                            'status': insurance[33],
                            'created_at': created_at,
                            'updated_at': updated_at,
                            'created_by': insurance[35],
                            'updated_by': insurance[36]
                        })
                    
                    pg_conn.commit()
                    log(f"✅ Successfully inserted {len(insurance_data)} insurance companies into PostgreSQL")
            
    except Exception as e:
        log(f"❌ Error populating insurance data: {e}")
    finally:
        mysql_conn.close()

def main():
    log("🚀 Starting real data population from MySQL to PostgreSQL...")
    
    try:
        # Test MySQL connection
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        # Test PostgreSQL connection
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Populate tables
        populate_people_data()
        populate_companies_data()
        populate_banks_data()
        populate_insurance_data()
        
        log("🎉 Real data population completed successfully!")
        
        # Show summary
        with postgres_engine.connect() as conn:
            people_count = conn.execute(text("SELECT COUNT(*) FROM people")).fetchone()[0]
            companies_count = conn.execute(text("SELECT COUNT(*) FROM companies")).fetchone()[0]
            banks_count = conn.execute(text("SELECT COUNT(*) FROM banks")).fetchone()[0]
            insurance_count = conn.execute(text("SELECT COUNT(*) FROM insurance")).fetchone()[0]
            
            print(f"\n📊 Database Summary:")
            print(f"  👥 People: {people_count:,}")
            print(f"  🏭 Companies: {companies_count:,}")
            print(f"  🏦 Banks: {banks_count:,}")
            print(f"  🛡️ Insurance Companies: {insurance_count:,}")
            
    except Exception as e:
        log(f"❌ Error during data population: {e}")

if __name__ == "__main__":
    main()
