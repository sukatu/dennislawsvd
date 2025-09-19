#!/usr/bin/env python3
"""
Script to populate companies, banks, and insurance tables with real data
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, timedelta
import json
import random

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from models.companies import Companies
from models.banks import Banks
from models.insurance import Insurance

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def generate_companies_data():
    """Generate sample company data"""
    return [
        {
            "name": "TechCorp Solutions Inc.",
            "short_name": "TechCorp",
            "website": "https://www.techcorp.com",
            "phone": "+1-555-0100",
            "email": "contact@techcorp.com",
            "address": "100 Technology Drive, Silicon Valley",
            "city": "San Francisco",
            "region": "CA",
            "country": "USA",
            "postal_code": "94105",
            "type_of_company": "Technology",
            "district": "Silicon Valley",
            "date_of_incorporation": date(2015, 3, 15),
            "date_of_commencement": date(2015, 4, 1),
            "nature_of_business": "Software development and IT consulting",
            "registration_number": "TC-2015-001",
            "tax_identification_number": "TIN-TC-2015",
            "directors": json.dumps([
                {"name": "John Smith", "position": "CEO"},
                {"name": "Sarah Johnson", "position": "CTO"},
                {"name": "Michael Brown", "position": "CFO"}
            ]),
            "authorized_shares": 1000000,
            "stated_capital": 5000000.00,
            "tin_number": "TIN-TC-2015",
            "established_date": datetime(2015, 3, 15),
            "company_type": "Corporation",
            "industry": "Technology",
            "ownership_type": "Private",
            "annual_revenue": 25000000.00,
            "net_worth": 15000000.00,
            "employee_count": 150,
            "rating": "A+",
            "is_active": True,
            "is_verified": True,
            "status": "Active"
        },
        {
            "name": "Green Energy Systems Ltd.",
            "short_name": "GreenEnergy",
            "website": "https://www.greenenergy.com",
            "phone": "+1-555-0200",
            "email": "info@greenenergy.com",
            "address": "500 Renewable Way, Eco District",
            "city": "Austin",
            "region": "TX",
            "country": "USA",
            "postal_code": "78701",
            "type_of_company": "Energy",
            "district": "Downtown",
            "date_of_incorporation": date(2018, 6, 20),
            "date_of_commencement": date(2018, 7, 1),
            "nature_of_business": "Renewable energy solutions and solar panel installation",
            "registration_number": "GE-2018-002",
            "tax_identification_number": "TIN-GE-2018",
            "directors": json.dumps([
                {"name": "Maria Rodriguez", "position": "CEO"},
                {"name": "David Wilson", "position": "COO"},
                {"name": "Lisa Chen", "position": "CFO"}
            ]),
            "authorized_shares": 500000,
            "stated_capital": 2000000.00,
            "tin_number": "TIN-GE-2018",
            "established_date": datetime(2018, 6, 20),
            "company_type": "Limited Company",
            "industry": "Renewable Energy",
            "ownership_type": "Private",
            "annual_revenue": 8000000.00,
            "net_worth": 5000000.00,
            "employee_count": 45,
            "rating": "A",
            "is_active": True,
            "is_verified": True,
            "status": "Active"
        },
        {
            "name": "Metro Construction Group",
            "short_name": "MetroCon",
            "website": "https://www.metroconstruction.com",
            "phone": "+1-555-0300",
            "email": "contact@metroconstruction.com",
            "address": "750 Builder Boulevard, Industrial Zone",
            "city": "Chicago",
            "region": "IL",
            "country": "USA",
            "postal_code": "60601",
            "type_of_company": "Construction",
            "district": "Industrial",
            "date_of_incorporation": date(2010, 1, 10),
            "date_of_commencement": date(2010, 2, 1),
            "nature_of_business": "Commercial and residential construction",
            "registration_number": "MC-2010-003",
            "tax_identification_number": "TIN-MC-2010",
            "directors": json.dumps([
                {"name": "Robert Taylor", "position": "President"},
                {"name": "Jennifer Davis", "position": "VP Operations"},
                {"name": "James Wilson", "position": "VP Finance"}
            ]),
            "authorized_shares": 2000000,
            "stated_capital": 10000000.00,
            "tin_number": "TIN-MC-2010",
            "established_date": datetime(2010, 1, 10),
            "company_type": "Corporation",
            "industry": "Construction",
            "ownership_type": "Private",
            "annual_revenue": 45000000.00,
            "net_worth": 25000000.00,
            "employee_count": 300,
            "rating": "A-",
            "is_active": True,
            "is_verified": True,
            "status": "Active"
        }
    ]

def generate_banks_data():
    """Generate sample bank data"""
    return [
        {
            "name": "First National Bank",
            "short_name": "FNB",
            "website": "https://www.fnb.com",
            "phone": "+1-555-1000",
            "email": "contact@fnb.com",
            "address": "100 Financial Plaza, Downtown",
            "city": "New York",
            "region": "NY",
            "country": "USA",
            "postal_code": "10001",
            "license_number": "BNK-001-NY",
            "registration_number": "REG-FNB-001",
            "established_date": datetime(1920, 5, 15),
            "bank_type": "Commercial",
            "ownership_type": "Public",
            "total_assets": 50000000000.00,
            "net_worth": 5000000000.00,
            "rating": "AA",
            "head_office_address": "100 Financial Plaza, New York, NY 10001",
            "customer_service_phone": "+1-800-FNB-HELP",
            "customer_service_email": "support@fnb.com",
            "has_website": True,
            "has_mobile_app": True,
            "is_active": True,
            "is_verified": True,
            "status": "Active"
        },
        {
            "name": "Community Savings Bank",
            "short_name": "CSB",
            "website": "https://www.communitysavings.com",
            "phone": "+1-555-2000",
            "email": "info@communitysavings.com",
            "address": "250 Main Street, Town Center",
            "city": "Austin",
            "region": "TX",
            "country": "USA",
            "postal_code": "78701",
            "license_number": "BNK-002-TX",
            "registration_number": "REG-CSB-002",
            "established_date": datetime(1985, 8, 22),
            "bank_type": "Community",
            "ownership_type": "Private",
            "total_assets": 2500000000.00,
            "net_worth": 250000000.00,
            "rating": "A",
            "head_office_address": "250 Main Street, Austin, TX 78701",
            "customer_service_phone": "+1-800-CSB-HELP",
            "customer_service_email": "support@communitysavings.com",
            "has_website": True,
            "has_mobile_app": True,
            "is_active": True,
            "is_verified": True,
            "status": "Active"
        }
    ]

def generate_insurance_data():
    """Generate sample insurance data"""
    return [
        {
            "name": "SecureLife Insurance Company",
            "short_name": "SecureLife",
            "website": "https://www.securelife.com",
            "phone": "+1-555-3000",
            "email": "contact@securelife.com",
            "address": "300 Insurance Tower, Financial District",
            "city": "Chicago",
            "region": "IL",
            "country": "USA",
            "postal_code": "60601",
            "license_number": "INS-001-IL",
            "registration_number": "REG-SLI-001",
            "established_date": datetime(1950, 4, 10),
            "insurance_type": "Life & Health",
            "ownership_type": "Public",
            "total_assets": 15000000000.00,
            "net_worth": 3000000000.00,
            "premium_income": 5000000000.00,
            "claims_paid": 4000000000.00,
            "rating": "AA-",
            "head_office_address": "300 Insurance Tower, Chicago, IL 60601",
            "customer_service_phone": "+1-800-SLI-HELP",
            "customer_service_email": "support@securelife.com",
            "claims_phone": "+1-800-SLI-CLAIM",
            "claims_email": "claims@securelife.com",
            "has_mobile_app": True,
            "has_online_portal": True,
            "has_online_claims": True,
            "has_24_7_support": True,
            "is_active": True,
            "is_verified": True,
            "status": "Active"
        },
        {
            "name": "AutoShield Insurance Corp.",
            "short_name": "AutoShield",
            "website": "https://www.autoshield.com",
            "phone": "+1-555-4000",
            "email": "info@autoshield.com",
            "address": "400 Auto Plaza, Business Park",
            "city": "Los Angeles",
            "region": "CA",
            "country": "USA",
            "postal_code": "90210",
            "license_number": "INS-002-CA",
            "registration_number": "REG-ASI-002",
            "established_date": datetime(1975, 9, 15),
            "insurance_type": "Auto & Property",
            "ownership_type": "Private",
            "total_assets": 8000000000.00,
            "net_worth": 1600000000.00,
            "premium_income": 2500000000.00,
            "claims_paid": 2000000000.00,
            "rating": "A+",
            "head_office_address": "400 Auto Plaza, Los Angeles, CA 90210",
            "customer_service_phone": "+1-800-ASI-HELP",
            "customer_service_email": "support@autoshield.com",
            "claims_phone": "+1-800-ASI-CLAIM",
            "claims_email": "claims@autoshield.com",
            "has_mobile_app": True,
            "has_online_portal": True,
            "has_online_claims": True,
            "has_24_7_support": True,
            "is_active": True,
            "is_verified": True,
            "status": "Active"
        }
    ]

def seed_entities_data():
    """Seed companies, banks, and insurance tables with real data"""
    log("🏢 Starting entities data seeding...")
    
    # Create database engine
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Seed Companies
        log("🏭 Adding companies...")
        companies_data = generate_companies_data()
        for company_data in companies_data:
            company = Companies(**company_data)
            db.add(company)
            log(f"✅ Added company: {company_data['name']}")
        
        # Seed Banks
        log("🏦 Adding banks...")
        banks_data = generate_banks_data()
        for bank_data in banks_data:
            bank = Banks(**bank_data)
            db.add(bank)
            log(f"✅ Added bank: {bank_data['name']}")
        
        # Seed Insurance
        log("🛡️ Adding insurance companies...")
        insurance_data = generate_insurance_data()
        for insurance_data_item in insurance_data:
            insurance = Insurance(**insurance_data_item)
            db.add(insurance)
            log(f"✅ Added insurance: {insurance_data_item['name']}")
        
        # Commit all changes
        db.commit()
        log("🎉 Successfully added all entities to database!")
        
        # Show summary
        companies_count = db.query(Companies).count()
        banks_count = db.query(Banks).count()
        insurance_count = db.query(Insurance).count()
        
        print(f"\n📊 Entities Summary:")
        print(f"  🏭 Companies: {companies_count}")
        print(f"  🏦 Banks: {banks_count}")
        print(f"  🛡️ Insurance Companies: {insurance_count}")
        
    except Exception as e:
        log(f"❌ Error during entities seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_entities_data()
