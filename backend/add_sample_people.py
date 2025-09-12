#!/usr/bin/env python3
"""
Script to add sample people data to the database
"""

from sqlalchemy.orm import sessionmaker
from database import engine, create_tables
from models.people import People
from datetime import datetime, date
import random

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_sample_people():
    """Add sample people data to the database"""
    
    # Create tables first
    create_tables()
    
    # Sample people data
    sample_people = [
        {
            "first_name": "Albert",
            "last_name": "Kweku Obeng",
            "full_name": "Albert Kweku Obeng",
            "date_of_birth": datetime(1962, 3, 7),
            "date_of_death": datetime(2004, 3, 9),
            "id_number": "KL1K-DXP",
            "phone_number": "+233 24 123 4567",
            "email": "albert.obeng@email.com",
            "address": "123 Independence Avenue, Accra",
            "city": "Accra",
            "region": "Greater Accra",
            "country": "Ghana",
            "postal_code": "GA-123-4567",
            "risk_level": "Low",
            "risk_score": 25.0,
            "case_count": 2,
            "case_types": ["Property Dispute", "Family Law"],
            "occupation": "Business Owner",
            "employer": "Obeng Enterprises",
            "organization": "Ghana Chamber of Commerce",
            "job_title": "Managing Director",
            "marital_status": "Married",
            "spouse_name": "Grace Obeng",
            "children_count": 3,
            "emergency_contact": "Grace Obeng",
            "emergency_phone": "+233 24 123 4568",
            "nationality": "Ghanaian",
            "gender": "Male",
            "education_level": "University",
            "languages": ["English", "Twi", "Ga"],
            "is_verified": True,
            "verification_date": datetime(2023, 1, 15),
            "verification_notes": "Verified through court records and family verification",
            "status": "active",
            "notes": "Deceased - Historical record"
        },
        {
            "first_name": "Sarah",
            "last_name": "Mensah",
            "full_name": "Sarah Mensah",
            "date_of_birth": datetime(1975, 6, 15),
            "id_number": "GH-123456789",
            "phone_number": "+233 20 987 6543",
            "email": "sarah.mensah@email.com",
            "address": "456 Ring Road, Kumasi",
            "city": "Kumasi",
            "region": "Ashanti",
            "country": "Ghana",
            "postal_code": "KS-456-7890",
            "risk_level": "Medium",
            "risk_score": 65.0,
            "case_count": 5,
            "case_types": ["Business Dispute", "Contract Law", "Employment"],
            "occupation": "Lawyer",
            "employer": "Mensah & Associates",
            "organization": "Ghana Bar Association",
            "job_title": "Senior Partner",
            "marital_status": "Divorced",
            "spouse_name": None,
            "children_count": 2,
            "emergency_contact": "John Mensah",
            "emergency_phone": "+233 20 987 6544",
            "nationality": "Ghanaian",
            "gender": "Female",
            "education_level": "Postgraduate",
            "languages": ["English", "Twi", "French"],
            "is_verified": True,
            "verification_date": datetime(2023, 3, 20),
            "verification_notes": "Verified through professional licensing board",
            "status": "active",
            "notes": "Active legal practitioner"
        },
        {
            "first_name": "Kwame",
            "last_name": "Asante",
            "full_name": "Kwame Asante",
            "date_of_birth": datetime(1980, 9, 22),
            "id_number": "GH-987654321",
            "phone_number": "+233 26 555 1234",
            "email": "kwame.asante@email.com",
            "address": "789 High Street, Takoradi",
            "city": "Takoradi",
            "region": "Western",
            "country": "Ghana",
            "postal_code": "TK-789-0123",
            "risk_level": "High",
            "risk_score": 85.0,
            "case_count": 12,
            "case_types": ["Criminal", "Fraud", "Theft", "Assault"],
            "occupation": "Unemployed",
            "employer": None,
            "organization": None,
            "job_title": None,
            "marital_status": "Single",
            "spouse_name": None,
            "children_count": 0,
            "emergency_contact": "Mary Asante",
            "emergency_phone": "+233 26 555 1235",
            "nationality": "Ghanaian",
            "gender": "Male",
            "education_level": "Secondary",
            "languages": ["English", "Twi"],
            "is_verified": True,
            "verification_date": datetime(2023, 5, 10),
            "verification_notes": "Verified through criminal records and court proceedings",
            "status": "active",
            "notes": "Multiple criminal convictions"
        },
        {
            "first_name": "Ama",
            "last_name": "Serwaa",
            "full_name": "Ama Serwaa",
            "date_of_birth": datetime(1990, 1, 3),
            "id_number": "GH-456789123",
            "phone_number": "+233 27 333 7777",
            "email": "ama.serwaa@email.com",
            "address": "321 University Road, Cape Coast",
            "city": "Cape Coast",
            "region": "Central",
            "country": "Ghana",
            "postal_code": "CC-321-4567",
            "risk_level": "Low",
            "risk_score": 15.0,
            "case_count": 1,
            "case_types": ["Traffic Violation"],
            "occupation": "Teacher",
            "employer": "Cape Coast University",
            "organization": "Ghana Education Service",
            "job_title": "Lecturer",
            "marital_status": "Single",
            "spouse_name": None,
            "children_count": 0,
            "emergency_contact": "Kofi Serwaa",
            "emergency_phone": "+233 27 333 7778",
            "nationality": "Ghanaian",
            "gender": "Female",
            "education_level": "Postgraduate",
            "languages": ["English", "Twi", "Fante"],
            "is_verified": True,
            "verification_date": datetime(2023, 2, 28),
            "verification_notes": "Verified through employment records and educational institution",
            "status": "active",
            "notes": "Clean record, minor traffic violation"
        },
        {
            "first_name": "Kofi",
            "last_name": "Nkrumah",
            "full_name": "Kofi Nkrumah",
            "date_of_birth": datetime(1985, 4, 12),
            "id_number": "GH-111222333",
            "phone_number": "+233 24 444 8888",
            "email": "kofi.nkrumah@email.com",
            "address": "555 Liberation Road, Tamale",
            "city": "Tamale",
            "region": "Northern",
            "country": "Ghana",
            "postal_code": "TM-555-9999",
            "risk_level": "Medium",
            "risk_score": 45.0,
            "case_count": 3,
            "case_types": ["Land Dispute", "Family Law"],
            "occupation": "Farmer",
            "employer": "Self-employed",
            "organization": "Northern Farmers Association",
            "job_title": "Farm Owner",
            "marital_status": "Married",
            "spouse_name": "Akosua Nkrumah",
            "children_count": 4,
            "emergency_contact": "Akosua Nkrumah",
            "emergency_phone": "+233 24 444 8889",
            "nationality": "Ghanaian",
            "gender": "Male",
            "education_level": "Primary",
            "languages": ["English", "Dagbani", "Twi"],
            "is_verified": True,
            "verification_date": datetime(2023, 4, 5),
            "verification_notes": "Verified through traditional authority and community records",
            "status": "active",
            "notes": "Community leader, involved in land disputes"
        },
        {
            "first_name": "Efua",
            "last_name": "Agyeman",
            "full_name": "Efua Agyeman",
            "date_of_birth": datetime(1992, 8, 18),
            "id_number": "GH-777888999",
            "phone_number": "+233 23 666 1111",
            "email": "efua.agyeman@email.com",
            "address": "888 Airport Road, Ho",
            "city": "Ho",
            "region": "Volta",
            "country": "Ghana",
            "postal_code": "HO-888-1111",
            "risk_level": "Low",
            "risk_score": 20.0,
            "case_count": 0,
            "case_types": [],
            "occupation": "Nurse",
            "employer": "Ho Teaching Hospital",
            "organization": "Ghana Health Service",
            "job_title": "Senior Nurse",
            "marital_status": "Married",
            "spouse_name": "Samuel Agyeman",
            "children_count": 2,
            "emergency_contact": "Samuel Agyeman",
            "emergency_phone": "+233 23 666 1112",
            "nationality": "Ghanaian",
            "gender": "Female",
            "education_level": "Tertiary",
            "languages": ["English", "Ewe", "Twi"],
            "is_verified": True,
            "verification_date": datetime(2023, 6, 15),
            "verification_notes": "Verified through professional licensing and employment records",
            "status": "active",
            "notes": "Clean record, healthcare professional"
        }
    ]
    
    # Add more sample people with random data
    first_names = ["John", "Mary", "David", "Grace", "Michael", "Patricia", "James", "Elizabeth", "Robert", "Jennifer", "William", "Linda", "Richard", "Barbara", "Charles", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen", "Daniel", "Nancy", "Matthew", "Lisa", "Anthony", "Betty", "Mark", "Helen", "Donald", "Sandra", "Steven", "Donna", "Paul", "Carol", "Andrew", "Ruth", "Joshua", "Sharon", "Kenneth", "Michelle", "Kevin", "Laura", "Brian", "Sarah", "George", "Kimberly", "Edward", "Deborah"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts"]
    
    cities = ["Accra", "Kumasi", "Tamale", "Takoradi", "Cape Coast", "Ho", "Koforidua", "Sunyani", "Techiman", "Wa", "Bolgatanga", "Bawku", "Navrongo", "Yendi", "Savelugu", "Nalerigu", "Damongo", "Salaga", "Kintampo", "Ejura"]
    
    regions = ["Greater Accra", "Ashanti", "Northern", "Western", "Central", "Volta", "Eastern", "Brong-Ahafo", "Upper East", "Upper West"]
    
    occupations = ["Teacher", "Doctor", "Engineer", "Lawyer", "Accountant", "Nurse", "Farmer", "Business Owner", "Driver", "Mechanic", "Electrician", "Plumber", "Carpenter", "Tailor", "Hairdresser", "Chef", "Security Guard", "Cleaner", "Salesperson", "Manager"]
    
    case_types = ["Criminal", "Civil", "Family Law", "Property Dispute", "Contract Law", "Employment", "Traffic Violation", "Fraud", "Theft", "Assault", "Land Dispute", "Business Dispute"]
    
    for i in range(50):  # Add 50 more random people
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        city = random.choice(cities)
        region = random.choice(regions)
        occupation = random.choice(occupations)
        
        # Generate random case types
        num_cases = random.randint(0, 5)
        person_case_types = random.sample(case_types, min(num_cases, len(case_types))) if num_cases > 0 else []
        
        # Generate risk level based on case count
        if num_cases == 0:
            risk_level = "Low"
            risk_score = random.uniform(10, 30)
        elif num_cases <= 2:
            risk_level = "Low"
            risk_score = random.uniform(20, 40)
        elif num_cases <= 5:
            risk_level = "Medium"
            risk_score = random.uniform(40, 70)
        else:
            risk_level = "High"
            risk_score = random.uniform(70, 95)
        
        person_data = {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "date_of_birth": datetime(1950 + random.randint(0, 50), random.randint(1, 12), random.randint(1, 28)),
            "id_number": f"GH-{random.randint(100000000, 999999999)}",
            "phone_number": f"+233 {random.randint(20, 29)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            "email": f"{first_name.lower()}.{last_name.lower()}@email.com",
            "address": f"{random.randint(1, 999)} {random.choice(['Main Street', 'High Street', 'Ring Road', 'Independence Avenue', 'Liberation Road'])}",
            "city": city,
            "region": region,
            "country": "Ghana",
            "postal_code": f"{city[:2].upper()}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "risk_level": risk_level,
            "risk_score": round(risk_score, 1),
            "case_count": num_cases,
            "case_types": person_case_types,
            "occupation": occupation,
            "employer": f"{last_name} {random.choice(['Enterprises', 'Limited', 'Company', 'Associates'])}" if random.choice([True, False]) else None,
            "organization": f"{region} {random.choice(['Chamber of Commerce', 'Professional Association', 'Union'])}" if random.choice([True, False]) else None,
            "job_title": random.choice(["Manager", "Director", "Senior", "Junior", "Assistant", "Head"]) + " " + occupation if random.choice([True, False]) else None,
            "marital_status": random.choice(["Single", "Married", "Divorced", "Widowed"]),
            "spouse_name": f"{random.choice(first_names)} {last_name}" if random.choice([True, False]) else None,
            "children_count": random.randint(0, 6),
            "emergency_contact": f"{random.choice(first_names)} {last_name}",
            "emergency_phone": f"+233 {random.randint(20, 29)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            "nationality": "Ghanaian",
            "gender": random.choice(["Male", "Female"]),
            "education_level": random.choice(["Primary", "Secondary", "Tertiary", "University", "Postgraduate"]),
            "languages": random.sample(["English", "Twi", "Ga", "Ewe", "Dagbani", "Fante", "French"], random.randint(1, 3)),
            "is_verified": random.choice([True, False]),
            "verification_date": datetime(2023, random.randint(1, 12), random.randint(1, 28)) if random.choice([True, False]) else None,
            "verification_notes": f"Verified through {random.choice(['court records', 'employment records', 'community verification', 'professional licensing'])}" if random.choice([True, False]) else None,
            "status": "active",
            "notes": f"Sample person {i+1} - {random.choice(['Clean record', 'Minor issues', 'Active in community', 'Professional', 'Student'])}"
        }
        
        sample_people.append(person_data)
    
    # Insert data into database
    db = SessionLocal()
    try:
        for person_data in sample_people:
            person = People(**person_data)
            db.add(person)
        
        db.commit()
        print(f"Successfully added {len(sample_people)} people to the database")
        
    except Exception as e:
        print(f"Error adding people: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_people()
