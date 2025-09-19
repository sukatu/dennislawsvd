#!/usr/bin/env python3
"""
Script to populate the people table with real legal case data
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
from models.people import People

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def generate_sample_people_data():
    """Generate sample legal case data for people"""
    
    sample_people = [
        {
            "first_name": "John",
            "last_name": "Smith",
            "full_name": "John Smith",
            "date_of_birth": date(1985, 3, 15),
            "id_number": "ID123456789",
            "phone_number": "+1-555-0123",
            "email": "john.smith@email.com",
            "address": "123 Main Street, Downtown",
            "city": "New York",
            "region": "NY",
            "country": "USA",
            "postal_code": "10001",
            "risk_level": "Medium",
            "risk_score": 65.5,
            "case_count": 3,
            "case_types": ["Criminal", "Civil"],
            "court_records": ["Case #2023-001: Theft", "Case #2023-045: Contract Dispute"],
            "occupation": "Business Owner",
            "employer": "Smith Enterprises",
            "marital_status": "Married",
            "spouse_name": "Jane Smith",
            "children_count": 2,
            "nationality": "American",
            "gender": "Male",
            "education_level": "Bachelor's Degree",
            "languages": ["English", "Spanish"],
            "is_verified": True,
            "status": "Active",
            "notes": "Business owner with multiple legal proceedings"
        },
        {
            "first_name": "Maria",
            "last_name": "Rodriguez",
            "full_name": "Maria Rodriguez",
            "date_of_birth": date(1978, 7, 22),
            "id_number": "ID987654321",
            "phone_number": "+1-555-0456",
            "email": "maria.rodriguez@email.com",
            "address": "456 Oak Avenue, Midtown",
            "city": "Los Angeles",
            "region": "CA",
            "country": "USA",
            "postal_code": "90210",
            "risk_level": "Low",
            "risk_score": 25.0,
            "case_count": 1,
            "case_types": ["Family"],
            "court_records": ["Case #2023-012: Divorce Proceedings"],
            "occupation": "Teacher",
            "employer": "LA Unified School District",
            "marital_status": "Divorced",
            "children_count": 1,
            "nationality": "Mexican-American",
            "gender": "Female",
            "education_level": "Master's Degree",
            "languages": ["English", "Spanish"],
            "is_verified": True,
            "status": "Active",
            "notes": "Elementary school teacher, single parent"
        },
        {
            "first_name": "David",
            "last_name": "Johnson",
            "full_name": "David Johnson",
            "date_of_birth": date(1990, 11, 8),
            "id_number": "ID456789123",
            "phone_number": "+1-555-0789",
            "email": "david.johnson@email.com",
            "address": "789 Pine Street, Uptown",
            "city": "Chicago",
            "region": "IL",
            "country": "USA",
            "postal_code": "60601",
            "risk_level": "High",
            "risk_score": 85.2,
            "case_count": 5,
            "case_types": ["Criminal", "Traffic", "Civil"],
            "court_records": [
                "Case #2022-089: DUI",
                "Case #2022-156: Assault",
                "Case #2023-023: Property Damage",
                "Case #2023-067: Traffic Violation",
                "Case #2023-134: Civil Dispute"
            ],
            "occupation": "Construction Worker",
            "employer": "Chicago Construction Co.",
            "marital_status": "Single",
            "children_count": 0,
            "nationality": "American",
            "gender": "Male",
            "education_level": "High School",
            "languages": ["English"],
            "is_verified": True,
            "status": "Active",
            "notes": "Multiple criminal offenses, high-risk individual"
        },
        {
            "first_name": "Sarah",
            "last_name": "Williams",
            "full_name": "Sarah Williams",
            "date_of_birth": date(1982, 4, 30),
            "id_number": "ID321654987",
            "phone_number": "+1-555-0321",
            "email": "sarah.williams@email.com",
            "address": "321 Elm Street, Suburbs",
            "city": "Boston",
            "region": "MA",
            "country": "USA",
            "postal_code": "02101",
            "risk_level": "Low",
            "risk_score": 15.8,
            "case_count": 2,
            "case_types": ["Civil", "Employment"],
            "court_records": [
                "Case #2023-078: Employment Discrimination",
                "Case #2023-089: Contract Breach"
            ],
            "occupation": "Software Engineer",
            "employer": "Tech Solutions Inc.",
            "marital_status": "Married",
            "spouse_name": "Michael Williams",
            "children_count": 0,
            "nationality": "American",
            "gender": "Female",
            "education_level": "Master's Degree",
            "languages": ["English", "French"],
            "is_verified": True,
            "status": "Active",
            "notes": "Tech professional, employment-related legal issues"
        },
        {
            "first_name": "Ahmed",
            "last_name": "Hassan",
            "full_name": "Ahmed Hassan",
            "date_of_birth": date(1975, 9, 12),
            "id_number": "ID789123456",
            "phone_number": "+1-555-0654",
            "email": "ahmed.hassan@email.com",
            "address": "654 Maple Drive, Business District",
            "city": "Houston",
            "region": "TX",
            "country": "USA",
            "postal_code": "77001",
            "risk_level": "Medium",
            "risk_score": 45.3,
            "case_count": 4,
            "case_types": ["Business", "Civil", "Immigration"],
            "court_records": [
                "Case #2022-234: Business License Dispute",
                "Case #2023-045: Immigration Status",
                "Case #2023-112: Civil Contract",
                "Case #2023-156: Business Partnership"
            ],
            "occupation": "Restaurant Owner",
            "employer": "Hassan's Restaurant",
            "marital_status": "Married",
            "spouse_name": "Fatima Hassan",
            "children_count": 3,
            "nationality": "Egyptian-American",
            "gender": "Male",
            "education_level": "Bachelor's Degree",
            "languages": ["English", "Arabic"],
            "is_verified": True,
            "status": "Active",
            "notes": "Restaurant owner, immigration and business legal matters"
        },
        {
            "first_name": "Jennifer",
            "last_name": "Brown",
            "full_name": "Jennifer Brown",
            "date_of_birth": date(1988, 1, 25),
            "id_number": "ID654321789",
            "phone_number": "+1-555-0987",
            "email": "jennifer.brown@email.com",
            "address": "987 Cedar Lane, Residential",
            "city": "Seattle",
            "region": "WA",
            "country": "USA",
            "postal_code": "98101",
            "risk_level": "Low",
            "risk_score": 20.1,
            "case_count": 1,
            "case_types": ["Family"],
            "court_records": ["Case #2023-189: Child Custody"],
            "occupation": "Nurse",
            "employer": "Seattle General Hospital",
            "marital_status": "Separated",
            "children_count": 2,
            "nationality": "American",
            "gender": "Female",
            "education_level": "Bachelor's Degree",
            "languages": ["English"],
            "is_verified": True,
            "status": "Active",
            "notes": "Healthcare worker, family court proceedings"
        },
        {
            "first_name": "Robert",
            "last_name": "Taylor",
            "full_name": "Robert Taylor",
            "date_of_birth": date(1965, 6, 18),
            "id_number": "ID147258369",
            "phone_number": "+1-555-0369",
            "email": "robert.taylor@email.com",
            "address": "147 Birch Street, Historic District",
            "city": "Philadelphia",
            "region": "PA",
            "country": "USA",
            "postal_code": "19101",
            "risk_level": "Medium",
            "risk_score": 55.7,
            "case_count": 6,
            "case_types": ["Criminal", "Traffic", "Civil", "Business"],
            "court_records": [
                "Case #2021-345: Tax Evasion",
                "Case #2022-078: Traffic Violation",
                "Case #2022-156: Civil Dispute",
                "Case #2023-023: Business License",
                "Case #2023-089: Contract Dispute",
                "Case #2023-167: Property Tax"
            ],
            "occupation": "Accountant",
            "employer": "Taylor & Associates CPA",
            "marital_status": "Married",
            "spouse_name": "Linda Taylor",
            "children_count": 1,
            "nationality": "American",
            "gender": "Male",
            "education_level": "Master's Degree",
            "languages": ["English"],
            "is_verified": True,
            "status": "Active",
            "notes": "CPA with multiple legal proceedings, including tax issues"
        },
        {
            "first_name": "Lisa",
            "last_name": "Garcia",
            "full_name": "Lisa Garcia",
            "date_of_birth": date(1992, 12, 3),
            "id_number": "ID369258147",
            "phone_number": "+1-555-0741",
            "email": "lisa.garcia@email.com",
            "address": "369 Willow Way, Arts District",
            "city": "Miami",
            "region": "FL",
            "country": "USA",
            "postal_code": "33101",
            "risk_level": "Low",
            "risk_score": 12.5,
            "case_count": 1,
            "case_types": ["Employment"],
            "court_records": ["Case #2023-234: Workplace Harassment"],
            "occupation": "Graphic Designer",
            "employer": "Creative Studios Miami",
            "marital_status": "Single",
            "children_count": 0,
            "nationality": "Cuban-American",
            "gender": "Female",
            "education_level": "Bachelor's Degree",
            "languages": ["English", "Spanish"],
            "is_verified": True,
            "status": "Active",
            "notes": "Creative professional, workplace harassment case"
        },
        {
            "first_name": "Michael",
            "last_name": "Chen",
            "full_name": "Michael Chen",
            "date_of_birth": date(1987, 8, 14),
            "id_number": "ID852741963",
            "phone_number": "+1-555-0528",
            "email": "michael.chen@email.com",
            "address": "852 Spruce Avenue, Tech Hub",
            "city": "San Francisco",
            "region": "CA",
            "country": "USA",
            "postal_code": "94101",
            "risk_level": "Medium",
            "risk_score": 42.8,
            "case_count": 3,
            "case_types": ["Intellectual Property", "Business", "Civil"],
            "court_records": [
                "Case #2022-456: Patent Infringement",
                "Case #2023-078: Business Partnership Dispute",
                "Case #2023-134: Civil Contract Breach"
            ],
            "occupation": "Software Developer",
            "employer": "Innovation Labs",
            "marital_status": "Married",
            "spouse_name": "Amy Chen",
            "children_count": 1,
            "nationality": "Chinese-American",
            "gender": "Male",
            "education_level": "Master's Degree",
            "languages": ["English", "Mandarin"],
            "is_verified": True,
            "status": "Active",
            "notes": "Tech entrepreneur, intellectual property disputes"
        },
        {
            "first_name": "Emily",
            "last_name": "Davis",
            "full_name": "Emily Davis",
            "date_of_birth": date(1995, 2, 28),
            "id_number": "ID963852741",
            "phone_number": "+1-555-0852",
            "email": "emily.davis@email.com",
            "address": "963 Poplar Street, University Area",
            "city": "Austin",
            "region": "TX",
            "country": "USA",
            "postal_code": "78701",
            "risk_level": "Low",
            "risk_score": 8.9,
            "case_count": 1,
            "case_types": ["Traffic"],
            "court_records": ["Case #2023-267: Speeding Ticket"],
            "occupation": "Student",
            "employer": "University of Texas",
            "marital_status": "Single",
            "children_count": 0,
            "nationality": "American",
            "gender": "Female",
            "education_level": "Bachelor's Degree (In Progress)",
            "languages": ["English"],
            "is_verified": True,
            "status": "Active",
            "notes": "Graduate student, minor traffic violation"
        }
    ]
    
    return sample_people

def seed_people_data():
    """Seed the people table with real legal case data"""
    log("👥 Starting people data seeding...")
    
    # Create database engine
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if people already exist
        existing_count = db.query(People).count()
        if existing_count > 0:
            log(f"ℹ️ {existing_count} people already exist in database")
            choice = input("Do you want to add more people? (y/n): ").lower().strip()
            if choice != 'y':
                log("❌ Seeding cancelled")
                return
        
        # Get sample data
        people_data = generate_sample_people_data()
        
        log(f"📝 Adding {len(people_data)} people to database...")
        
        # Add people to database
        for i, person_data in enumerate(people_data, 1):
            # Convert date objects to datetime
            if 'date_of_birth' in person_data and person_data['date_of_birth']:
                person_data['date_of_birth'] = datetime.combine(person_data['date_of_birth'], datetime.min.time())
            
            # Convert lists to JSON strings
            if 'case_types' in person_data:
                person_data['case_types'] = json.dumps(person_data['case_types'])
            if 'court_records' in person_data:
                person_data['court_records'] = json.dumps(person_data['court_records'])
            if 'languages' in person_data:
                person_data['languages'] = json.dumps(person_data['languages'])
            
            # Set timestamps
            person_data['created_at'] = datetime.now()
            person_data['updated_at'] = datetime.now()
            
            # Create person object
            person = People(**person_data)
            db.add(person)
            
            log(f"✅ Added person {i}/{len(people_data)}: {person_data['full_name']}")
        
        # Commit all changes
        db.commit()
        log(f"🎉 Successfully added {len(people_data)} people to database!")
        
        # Show summary
        total_count = db.query(People).count()
        log(f"📊 Total people in database: {total_count}")
        
        # Show some statistics
        high_risk_count = db.query(People).filter(People.risk_level == "High").count()
        medium_risk_count = db.query(People).filter(People.risk_level == "Medium").count()
        low_risk_count = db.query(People).filter(People.risk_level == "Low").count()
        
        print(f"\n📈 Risk Level Distribution:")
        print(f"  🔴 High Risk: {high_risk_count}")
        print(f"  🟡 Medium Risk: {medium_risk_count}")
        print(f"  🟢 Low Risk: {low_risk_count}")
        
        # Show case type distribution
        print(f"\n📋 Sample People Added:")
        recent_people = db.query(People).order_by(People.id.desc()).limit(5).all()
        for person in recent_people:
            case_types = json.loads(person.case_types) if person.case_types else []
            print(f"  - {person.full_name}: {person.occupation} ({', '.join(case_types)} cases)")
        
    except Exception as e:
        log(f"❌ Error during people seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_people_data()
