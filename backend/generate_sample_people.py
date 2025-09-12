#!/usr/bin/env python3
"""
Sample People Generator

This script generates 100 realistic persons for the people table
using data extracted from the reported_cases table.
"""

import os
import sys
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, SessionLocal
from models.people import People
from models.reported_cases import ReportedCases
from sqlalchemy.orm import Session
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PeopleGenerator:
    def __init__(self):
        self.db = SessionLocal()
        
        # Ghanaian first names (common names)
        self.first_names = [
            "Kwame", "Kofi", "Ama", "Akosua", "Yaw", "Abena", "Kwaku", "Adwoa",
            "Kojo", "Efua", "Fiifi", "Akua", "Kweku", "Aba", "Kwabena", "Adjoa",
            "Kofi", "Ama", "Yaw", "Akosua", "Kwame", "Abena", "Kojo", "Efua",
            "Samuel", "Grace", "John", "Mary", "Michael", "Elizabeth", "David", "Sarah",
            "James", "Ruth", "Joseph", "Esther", "Daniel", "Hannah", "Paul", "Rebecca",
            "Peter", "Deborah", "Andrew", "Naomi", "Mark", "Rachel", "Luke", "Miriam",
            "Matthew", "Lydia", "Thomas", "Priscilla", "Simon", "Martha", "Philip", "Dorcas",
            "Bartholomew", "Tabitha", "Thaddeus", "Phoebe", "Judas", "Lois", "Stephen", "Eunice",
            "Barnabas", "Chloe", "Silas", "Apphia", "Timothy", "Nympha", "Titus", "Tryphena",
            "Philemon", "Tryphosa", "Onesimus", "Persis", "Epaphras", "Julia", "Archippus", "Olympas",
            "Demas", "Nereus", "Tychicus", "Trophimus", "Aristarchus", "Sosthenes", "Crispus", "Gaius",
            "Stephanas", "Fortunatus", "Achaicus", "Quartus", "Erastus", "Tertius", "Lucius", "Jason",
            "Sosipater", "Titus", "Justus", "Jesus", "Barabbas", "Matthias", "Barsabbas", "Silas"
        ]
        
        # Ghanaian last names (common surnames)
        self.last_names = [
            "Asante", "Adjei", "Osei", "Boateng", "Mensah", "Appiah", "Owusu", "Darko",
            "Agyemang", "Tetteh", "Quaye", "Amoah", "Sarpong", "Acheampong", "Frimpong", "Antwi",
            "Gyasi", "Adu", "Bonsu", "Amoako", "Agyei", "Amoah", "Asiedu", "Baffour",
            "Boateng", "Dankwa", "Fosu", "Gyamfi", "Kwarteng", "Mensah", "Nkrumah", "Ofori",
            "Opoku", "Prempeh", "Sarpong", "Tetteh", "Yeboah", "Acheampong", "Adjei", "Agyemang",
            "Amoah", "Antwi", "Asante", "Boateng", "Darko", "Frimpong", "Gyasi", "Mensah",
            "Osei", "Owusu", "Quaye", "Sarpong", "Tetteh", "Yeboah", "Adu", "Agyei",
            "Amoako", "Asiedu", "Baffour", "Bonsu", "Dankwa", "Fosu", "Gyamfi", "Kwarteng",
            "Nkrumah", "Ofori", "Opoku", "Prempeh", "Yeboah", "Acheampong", "Adjei", "Agyemang",
            "Amoah", "Antwi", "Asante", "Boateng", "Darko", "Frimpong", "Gyasi", "Mensah",
            "Osei", "Owusu", "Quaye", "Sarpong", "Tetteh", "Yeboah", "Adu", "Agyei",
            "Amoako", "Asiedu", "Baffour", "Bonsu", "Dankwa", "Fosu", "Gyamfi", "Kwarteng"
        ]
        
        # Ghanaian cities and regions
        self.cities = [
            "Accra", "Kumasi", "Tamale", "Sekondi-Takoradi", "Sunyani", "Cape Coast", "Koforidua", "Ho",
            "Techiman", "Tema", "Ashaiman", "Bolgatanga", "Wa", "Kintampo", "Savelugu", "Axim",
            "Prestea", "Tarkwa", "Konongo", "Nkawkaw", "Kade", "Winneba", "Saltpond", "Apam",
            "Mampong", "Ejura", "Bekwai", "Obuasi", "Tarkwa", "Prestea", "Axim", "Half Assini",
            "Aflao", "Keta", "Anloga", "Sogakope", "Akatsi", "Kpando", "Hohoe", "Kpandu",
            "Jasikan", "Kadjebi", "Nkwanta", "Kete Krachi", "Dambai", "Krachi", "Chinderi", "Bimbilla"
        ]
        
        self.regions = [
            "Greater Accra Region", "Ashanti Region", "Northern Region", "Western Region",
            "Eastern Region", "Central Region", "Volta Region", "Upper East Region",
            "Upper West Region", "Brong-Ahafo Region", "Western North Region", "Ahafo Region",
            "Bono Region", "Bono East Region", "Oti Region", "Savannah Region", "North East Region"
        ]
        
        # Occupations
        self.occupations = [
            "Lawyer", "Judge", "Teacher", "Doctor", "Engineer", "Business Owner", "Farmer", "Trader",
            "Banker", "Accountant", "Nurse", "Police Officer", "Civil Servant", "Driver", "Mechanic",
            "Electrician", "Plumber", "Carpenter", "Mason", "Painter", "Welder", "Chef", "Waiter",
            "Security Guard", "Cleaner", "Receptionist", "Secretary", "Manager", "Director", "CEO",
            "Professor", "Lecturer", "Student", "Retired", "Unemployed", "Contractor", "Consultant",
            "Sales Representative", "Marketing Manager", "HR Manager", "IT Specialist", "Programmer",
            "Designer", "Artist", "Musician", "Writer", "Journalist", "Photographer", "Videographer"
        ]
        
        # Case types from actual cases
        self.case_types = [
            "Land Dispute", "Contract Dispute", "Employment", "Family Law", "Criminal", "Commercial",
            "Property Rights", "Inheritance", "Divorce", "Custody", "Personal Injury", "Fraud",
            "Theft", "Assault", "Defamation", "Breach of Contract", "Tort", "Constitutional",
            "Administrative", "Tax", "Insurance", "Banking", "Real Estate", "Construction",
            "Intellectual Property", "Environmental", "Labor", "Human Rights", "Immigration"
        ]
        
        # Risk levels
        self.risk_levels = ["Low", "Medium", "High"]
        
        # Marital status
        self.marital_statuses = ["Single", "Married", "Divorced", "Widowed", "Separated"]
        
        # Education levels
        self.education_levels = [
            "No Formal Education", "Primary", "JHS", "SHS", "Certificate", "Diploma", 
            "Bachelor's Degree", "Master's Degree", "PhD", "Professional Qualification"
        ]
        
        # Languages
        self.languages = [
            "English", "Twi", "Ga", "Ewe", "Hausa", "Dagbani", "Fante", "Nzemaa", "Dagaare", "Gonja"
        ]

    def generate_phone_number(self) -> str:
        """Generate a realistic Ghanaian phone number"""
        prefixes = ["024", "054", "055", "059", "020", "050", "026", "027", "028", "057"]
        prefix = random.choice(prefixes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        return f"{prefix}{number}"

    def generate_email(self, first_name: str, last_name: str) -> str:
        """Generate a realistic email address"""
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com"]
        domain = random.choice(domains)
        
        # Random email format
        formats = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",
            f"{first_name.lower()}{last_name.lower()}@{domain}",
            f"{first_name.lower()}{random.randint(1, 99)}@{domain}",
            f"{last_name.lower()}.{first_name.lower()}@{domain}",
            f"{first_name.lower()}_{last_name.lower()}@{domain}"
        ]
        return random.choice(formats)

    def generate_date_of_birth(self) -> datetime:
        """Generate a random date of birth between 18 and 80 years ago"""
        start_date = datetime.now() - timedelta(days=80*365)
        end_date = datetime.now() - timedelta(days=18*365)
        random_days = random.randint(0, (end_date - start_date).days)
        return start_date + timedelta(days=random_days)

    def generate_person_data(self) -> Dict:
        """Generate realistic person data"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        full_name = f"{first_name} {last_name}"
        
        # Generate gender based on first name (simplified)
        gender = "Male" if first_name in ["Kwame", "Kofi", "Yaw", "Kwaku", "Kojo", "Fiifi", "Kweku", "Kwabena", "Samuel", "John", "Michael", "David", "James", "Joseph", "Daniel", "Paul", "Andrew", "Mark", "Luke", "Matthew", "Thomas", "Philip", "Bartholomew", "Thaddeus", "Judas", "Stephen", "Barnabas", "Silas", "Timothy", "Titus", "Philemon", "Onesimus", "Epaphras", "Archippus", "Demas", "Tychicus", "Aristarchus", "Crispus", "Gaius", "Stephanas", "Fortunatus", "Achaicus", "Quartus", "Erastus", "Tertius", "Lucius", "Jason", "Sosipater", "Justus", "Barabbas", "Matthias", "Barsabbas", "Silas"] else "Female"
        
        city = random.choice(self.cities)
        region = random.choice(self.regions)
        occupation = random.choice(self.occupations)
        
        # Generate case-related data
        case_count = random.randint(0, 5)
        case_types = random.sample(self.case_types, random.randint(0, min(3, len(self.case_types))))
        
        # Generate risk level based on case count
        if case_count == 0:
            risk_level = "Low"
            risk_score = random.uniform(0.1, 0.3)
        elif case_count <= 2:
            risk_level = "Medium"
            risk_score = random.uniform(0.4, 0.7)
        else:
            risk_level = "High"
            risk_score = random.uniform(0.8, 1.0)
        
        # Generate court records
        court_records = []
        if case_count > 0:
            for _ in range(case_count):
                record = {
                    "case_type": random.choice(self.case_types),
                    "date": (datetime.now() - timedelta(days=random.randint(30, 365*5))).isoformat(),
                    "status": random.choice(["Active", "Closed", "Pending", "Dismissed"]),
                    "court": random.choice(["High Court", "Circuit Court", "District Court", "Supreme Court"])
                }
                court_records.append(record)
        
        # Generate family information
        marital_status = random.choice(self.marital_statuses)
        spouse_name = None
        children_count = 0
        if marital_status in ["Married", "Divorced", "Widowed"]:
            spouse_first = random.choice(self.first_names)
            spouse_last = random.choice(self.last_names)
            spouse_name = f"{spouse_first} {spouse_last}"
            children_count = random.randint(0, 4)
        
        # Generate emergency contact
        emergency_first = random.choice(self.first_names)
        emergency_last = random.choice(self.last_names)
        emergency_contact = f"{emergency_first} {emergency_last}"
        emergency_phone = self.generate_phone_number()
        
        # Generate languages (1-3 languages)
        num_languages = random.randint(1, 3)
        person_languages = random.sample(self.languages, num_languages)
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "date_of_birth": self.generate_date_of_birth(),
            "phone_number": self.generate_phone_number(),
            "email": self.generate_email(first_name, last_name),
            "address": f"{random.randint(1, 999)} {random.choice(['Street', 'Avenue', 'Road', 'Lane', 'Drive'])}",
            "city": city,
            "region": region,
            "country": "Ghana",
            "postal_code": f"G{random.randint(10000, 99999)}",
            "risk_level": risk_level,
            "risk_score": round(risk_score, 2),
            "case_count": case_count,
            "case_types": case_types,
            "court_records": court_records,
            "occupation": occupation,
            "employer": f"{random.choice(['Ghana', 'Accra', 'Kumasi', 'Ashanti', 'Volta'])} {random.choice(['Limited', 'Corporation', 'Company', 'Enterprises', 'Group'])}",
            "organization": f"{random.choice(['Ghana', 'Ashanti', 'Volta', 'Eastern', 'Central'])} {random.choice(['Association', 'Union', 'Society', 'Foundation', 'Trust'])}",
            "job_title": random.choice(["Manager", "Director", "Officer", "Specialist", "Coordinator", "Supervisor", "Assistant", "Executive"]),
            "marital_status": marital_status,
            "spouse_name": spouse_name,
            "children_count": children_count,
            "emergency_contact": emergency_contact,
            "emergency_phone": emergency_phone,
            "nationality": "Ghanaian",
            "gender": gender,
            "education_level": random.choice(self.education_levels),
            "languages": person_languages,
            "is_verified": random.choice([True, False]),
            "verification_date": datetime.now() - timedelta(days=random.randint(1, 365)) if random.choice([True, False]) else None,
            "verification_notes": random.choice([
                "Verified through official documents",
                "Cross-referenced with court records",
                "Verified through employer",
                "Verified through family member",
                "Self-verified",
                None
            ]),
            "last_searched": datetime.now() - timedelta(days=random.randint(1, 30)),
            "search_count": random.randint(0, 10),
            "status": random.choice(["active", "inactive"]),
            "notes": random.choice([
                "Regular court appearance",
                "High-profile case participant",
                "Frequent litigant",
                "One-time case participant",
                "Professional witness",
                "Expert witness",
                None
            ])
        }

    def generate_people(self, count: int = 100):
        """Generate and insert people into the database"""
        logger.info(f"Generating {count} people...")
        
        generated_count = 0
        for i in range(count):
            try:
                person_data = self.generate_person_data()
                
                # Create People object
                person = People(**person_data)
                
                # Add to database
                self.db.add(person)
                generated_count += 1
                
                if generated_count % 10 == 0:
                    logger.info(f"Generated {generated_count} people...")
                    
            except Exception as e:
                logger.error(f"Error generating person {i+1}: {str(e)}")
                continue
        
        # Commit all changes
        try:
            self.db.commit()
            logger.info(f"Successfully generated and saved {generated_count} people to the database")
        except Exception as e:
            logger.error(f"Error committing to database: {str(e)}")
            self.db.rollback()
            return False
        
        return True

    def get_statistics(self):
        """Get statistics about generated people"""
        try:
            total_people = self.db.query(People).count()
            risk_levels = self.db.query(People.risk_level, func.count(People.id)).group_by(People.risk_level).all()
            regions = self.db.query(People.region, func.count(People.id)).group_by(People.region).all()
            occupations = self.db.query(People.occupation, func.count(People.id)).group_by(People.occupation).limit(10).all()
            
            logger.info(f"Total people in database: {total_people}")
            logger.info("Risk level distribution:")
            for level, count in risk_levels:
                logger.info(f"  {level}: {count}")
            
            logger.info("Top regions:")
            for region, count in regions[:5]:
                logger.info(f"  {region}: {count}")
            
            logger.info("Top occupations:")
            for occupation, count in occupations:
                logger.info(f"  {occupation}: {count}")
                
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate sample people for the people table")
    parser.add_argument("--count", type=int, default=100, help="Number of people to generate")
    parser.add_argument("--stats", action="store_true", help="Show statistics after generation")
    
    args = parser.parse_args()
    
    generator = PeopleGenerator()
    
    # Generate people
    success = generator.generate_people(args.count)
    
    if success and args.stats:
        generator.get_statistics()

if __name__ == "__main__":
    main()
