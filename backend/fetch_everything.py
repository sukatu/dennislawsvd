#!/usr/bin/env python3
"""
Comprehensive script to fetch ALL data from MySQL and populate PostgreSQL
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

def populate_table(table_name, mysql_query, postgres_query, transform_func=None):
    """Generic function to populate any table"""
    log(f"📊 Populating {table_name} table...")
    
    mysql_conn = get_mysql_connection()
    postgres_engine = get_postgres_engine()
    
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(mysql_query)
            data = cursor.fetchall()
            
            if data:
                log(f"📋 Found {len(data)} records in MySQL {table_name}")
                
                with postgres_engine.connect() as pg_conn:
                    for row in data:
                        try:
                            # Transform data if function provided
                            if transform_func:
                                row_data = transform_func(row)
                            else:
                                row_data = dict(zip([col[0] for col in cursor.description], row))
                            
                            pg_conn.execute(text(postgres_query), row_data)
                        except Exception as e:
                            log(f"⚠️  Error inserting record in {table_name}: {e}")
                            continue
                    
                    pg_conn.commit()
                    log(f"✅ Successfully inserted {len(data)} records into {table_name}")
            else:
                log(f"ℹ️  No data found in MySQL {table_name}")
                
    except Exception as e:
        log(f"❌ Error populating {table_name}: {e}")
    finally:
        mysql_conn.close()

def transform_people(row):
    """Transform people data"""
    columns = ['id', 'first_name', 'last_name', 'full_name', 'previous_names', 'date_of_birth',
               'date_of_death', 'id_number', 'phone_number', 'email', 'address', 'city', 'region',
               'country', 'postal_code', 'risk_level', 'risk_score', 'case_count', 'case_types',
               'court_records', 'occupation', 'employer', 'organization', 'job_title',
               'marital_status', 'spouse_name', 'children_count', 'emergency_contact',
               'emergency_phone', 'nationality', 'gender', 'education_level', 'languages',
               'is_verified', 'verification_date', 'verification_notes', 'last_searched',
               'search_count', 'created_at', 'updated_at', 'created_by', 'updated_by',
               'status', 'notes']
    
    data = dict(zip(columns, row))
    
    # Convert specific fields
    data['is_verified'] = safe_convert_bool(data['is_verified'])
    data['previous_names'] = json.dumps(safe_convert_json(data['previous_names'])) if data['previous_names'] else None
    data['case_types'] = json.dumps(safe_convert_json(data['case_types'])) if data['case_types'] else None
    data['court_records'] = json.dumps(safe_convert_json(data['court_records'])) if data['court_records'] else None
    data['languages'] = json.dumps(safe_convert_json(data['languages'])) if data['languages'] else None
    data['created_at'] = safe_convert_date(data['created_at']) or datetime.now()
    data['updated_at'] = safe_convert_date(data['updated_at']) or datetime.now()
    
    return data

def transform_companies(row):
    """Transform companies data"""
    columns = ['id', 'name', 'short_name', 'website', 'phone', 'email', 'address', 'city', 'region',
               'country', 'postal_code', 'type_of_company', 'district', 'date_of_incorporation',
               'date_of_commencement', 'nature_of_business', 'registration_number',
               'tax_identification_number', 'directors', 'authorized_shares', 'stated_capital',
               'tin_number', 'established_date', 'company_type', 'industry', 'ownership_type',
               'annual_revenue', 'net_worth', 'employee_count', 'rating', 'is_active', 'is_verified',
               'status', 'created_at', 'updated_at', 'created_by', 'updated_by']
    
    data = dict(zip(columns, row))
    
    # Convert specific fields
    data['is_active'] = safe_convert_bool(data['is_active'])
    data['is_verified'] = safe_convert_bool(data['is_verified'])
    data['directors'] = json.dumps(safe_convert_json(data['directors'])) if data['directors'] else None
    data['created_at'] = safe_convert_date(data['created_at']) or datetime.now()
    data['updated_at'] = safe_convert_date(data['updated_at']) or datetime.now()
    
    return data

def transform_banks(row):
    """Transform banks data"""
    columns = ['id', 'name', 'short_name', 'website', 'phone', 'email', 'address', 'city', 'region',
               'country', 'postal_code', 'license_number', 'established_date',
               'bank_type', 'ownership_type', 'total_assets', 'net_worth', 'rating',
               'head_office_address', 'customer_service_phone', 'customer_service_email',
               'has_website', 'has_mobile_app', 'is_active', 'is_verified', 'status',
               'created_at', 'updated_at', 'created_by', 'updated_by']
    
    data = dict(zip(columns, row))
    
    # Convert specific fields
    data['has_website'] = safe_convert_bool(data['has_website'])
    data['has_mobile_app'] = safe_convert_bool(data['has_mobile_app'])
    data['is_active'] = safe_convert_bool(data['is_active'])
    data['is_verified'] = safe_convert_bool(data['is_verified'])
    data['created_at'] = safe_convert_date(data['created_at']) or datetime.now()
    data['updated_at'] = safe_convert_date(data['updated_at']) or datetime.now()
    
    return data

def transform_insurance(row):
    """Transform insurance data"""
    columns = ['id', 'name', 'short_name', 'website', 'phone', 'email', 'address', 'city', 'region',
               'country', 'postal_code', 'license_number', 'established_date',
               'insurance_type', 'ownership_type', 'total_assets', 'net_worth', 'premium_income',
               'claims_paid', 'rating', 'head_office_address', 'customer_service_phone',
               'customer_service_email', 'claims_phone', 'claims_email', 'has_mobile_app',
               'has_online_portal', 'has_online_claims', 'has_24_7_support', 'is_active',
               'is_verified', 'status', 'created_at', 'updated_at', 'created_by', 'updated_by']
    
    data = dict(zip(columns, row))
    
    # Convert specific fields
    data['has_mobile_app'] = safe_convert_bool(data['has_mobile_app'])
    data['has_online_portal'] = safe_convert_bool(data['has_online_portal'])
    data['has_online_claims'] = safe_convert_bool(data['has_online_claims'])
    data['has_24_7_support'] = safe_convert_bool(data['has_24_7_support'])
    data['is_active'] = safe_convert_bool(data['is_active'])
    data['is_verified'] = safe_convert_bool(data['is_verified'])
    data['created_at'] = safe_convert_date(data['created_at']) or datetime.now()
    data['updated_at'] = safe_convert_date(data['updated_at']) or datetime.now()
    
    return data

def transform_reported_cases(row):
    """Transform reported cases data"""
    columns = ['id', 'case_number', 'title', 'description', 'case_type', 'status', 'priority',
               'court_name', 'judge_name', 'plaintiff', 'defendant', 'case_date', 'hearing_date',
               'outcome', 'verdict', 'damages_awarded', 'legal_fees', 'case_value',
               'document_path', 'created_at', 'updated_at', 'created_by', 'updated_by']
    
    data = dict(zip(columns, row))
    
    # Convert specific fields
    data['created_at'] = safe_convert_date(data['created_at']) or datetime.now()
    data['updated_at'] = safe_convert_date(data['updated_at']) or datetime.now()
    
    return data

def main():
    log("🚀 Starting comprehensive data fetch from MySQL to PostgreSQL...")
    
    try:
        # Test connections
        mysql_conn = get_mysql_connection()
        mysql_conn.close()
        log("✅ MySQL connection successful")
        
        postgres_engine = get_postgres_engine()
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("✅ PostgreSQL connection successful")
        
        # Define all tables to populate
        tables_to_populate = [
            {
                'name': 'people',
                'mysql_query': 'SELECT * FROM people',
                'postgres_query': '''
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
                ''',
                'transform': transform_people
            },
            {
                'name': 'companies',
                'mysql_query': 'SELECT * FROM companies',
                'postgres_query': '''
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
                ''',
                'transform': transform_companies
            },
            {
                'name': 'banks',
                'mysql_query': 'SELECT * FROM banks',
                'postgres_query': '''
                    INSERT INTO banks (
                        id, name, short_name, website, phone, email, address, city, region,
                        country, postal_code, license_number, established_date,
                        bank_type, ownership_type, total_assets, net_worth, rating,
                        head_office_address, customer_service_phone, customer_service_email,
                        has_website, has_mobile_app, is_active, is_verified, status,
                        created_at, updated_at, created_by, updated_by
                    ) VALUES (
                        :id, :name, :short_name, :website, :phone, :email, :address, :city, :region,
                        :country, :postal_code, :license_number, :established_date,
                        :bank_type, :ownership_type, :total_assets, :net_worth, :rating,
                        :head_office_address, :customer_service_phone, :customer_service_email,
                        :has_website, :has_mobile_app, :is_active, :is_verified, :status,
                        :created_at, :updated_at, :created_by, :updated_by
                    ) ON CONFLICT (id) DO NOTHING
                ''',
                'transform': transform_banks
            },
            {
                'name': 'insurance',
                'mysql_query': 'SELECT * FROM insurance',
                'postgres_query': '''
                    INSERT INTO insurance (
                        id, name, short_name, website, phone, email, address, city, region,
                        country, postal_code, license_number, established_date,
                        insurance_type, ownership_type, total_assets, net_worth, premium_income,
                        claims_paid, rating, head_office_address, customer_service_phone,
                        customer_service_email, claims_phone, claims_email, has_mobile_app,
                        has_online_portal, has_online_claims, has_24_7_support, is_active,
                        is_verified, status, created_at, updated_at, created_by, updated_by
                    ) VALUES (
                        :id, :name, :short_name, :website, :phone, :email, :address, :city, :region,
                        :country, :postal_code, :license_number, :established_date,
                        :insurance_type, :ownership_type, :total_assets, :net_worth, :premium_income,
                        :claims_paid, :rating, :head_office_address, :customer_service_phone,
                        :customer_service_email, :claims_phone, :claims_email, :has_mobile_app,
                        :has_online_portal, :has_online_claims, :has_24_7_support, :is_active,
                        :is_verified, :status, :created_at, :updated_at, :created_by, :updated_by
                    ) ON CONFLICT (id) DO NOTHING
                ''',
                'transform': transform_insurance
            },
            {
                'name': 'reported_cases',
                'mysql_query': 'SELECT * FROM reported_cases',
                'postgres_query': '''
                    INSERT INTO reported_cases (
                        id, case_number, title, description, case_type, status, priority,
                        court_name, judge_name, plaintiff, defendant, case_date, hearing_date,
                        outcome, verdict, damages_awarded, legal_fees, case_value,
                        document_path, created_at, updated_at, created_by, updated_by
                    ) VALUES (
                        :id, :case_number, :title, :description, :case_type, :status, :priority,
                        :court_name, :judge_name, :plaintiff, :defendant, :case_date, :hearing_date,
                        :outcome, :verdict, :damages_awarded, :legal_fees, :case_value,
                        :document_path, :created_at, :updated_at, :created_by, :updated_by
                    ) ON CONFLICT (id) DO NOTHING
                ''',
                'transform': transform_reported_cases
            }
        ]
        
        # Populate all tables
        for table in tables_to_populate:
            populate_table(
                table['name'],
                table['mysql_query'],
                table['postgres_query'],
                table['transform']
            )
        
        log("🎉 Comprehensive data fetch completed!")
        
        # Show final summary
        with postgres_engine.connect() as conn:
            people_count = conn.execute(text("SELECT COUNT(*) FROM people")).fetchone()[0]
            companies_count = conn.execute(text("SELECT COUNT(*) FROM companies")).fetchone()[0]
            banks_count = conn.execute(text("SELECT COUNT(*) FROM banks")).fetchone()[0]
            insurance_count = conn.execute(text("SELECT COUNT(*) FROM insurance")).fetchone()[0]
            cases_count = conn.execute(text("SELECT COUNT(*) FROM reported_cases")).fetchone()[0]
            
            print(f"\n📊 Final Database Summary:")
            print(f"  👥 People: {people_count:,}")
            print(f"  🏭 Companies: {companies_count:,}")
            print(f"  🏦 Banks: {banks_count:,}")
            print(f"  🛡️ Insurance Companies: {insurance_count:,}")
            print(f"  📋 Reported Cases: {cases_count:,}")
            print(f"\n🎯 Total Records: {people_count + companies_count + banks_count + insurance_count + cases_count:,}")
            
    except Exception as e:
        log(f"❌ Error during comprehensive data fetch: {e}")

if __name__ == "__main__":
    main()
