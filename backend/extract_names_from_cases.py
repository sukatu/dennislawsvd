#!/usr/bin/env python3
"""
Script to extract person names from reported_cases titles and populate the people table.
This will enable name-based searching where users can search for "Charlse" and find
all people with names containing that term.
"""

import re
import json
import pymysql
from config import settings
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for generating additional person data
fake = Faker()

def connect_to_database():
    """Connect to the MySQL database"""
    db_config = {
        'host': settings.mysql_host,
        'user': settings.mysql_user,
        'password': settings.mysql_password,
        'database': settings.mysql_database,
        'charset': 'utf8mb4'
    }
    return pymysql.connect(**db_config)

def extract_names_from_title(title):
    """
    Extract potential person names from a case title.
    This function looks for patterns that typically indicate person names.
    """
    if not title:
        return []
    
    names = []
    
    # More selective patterns for person names only (avoid company names and full case titles)
    patterns = [
        # Pattern 1: Names at the beginning before "vs." (plaintiffs) - limit to 2-4 words
        r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s+(?:vs\.|v\.)',
        # Pattern 2: Names after "vs." or "v." but before next "vs." or end - limit to 2-4 words
        r'(?:vs\.|v\.)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})(?:\s+and\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})*(?:\s+vs\.|$)',
        # Pattern 3: Names in parentheses - limit to 2-4 words
        r'\(([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\)',
        # Pattern 4: Names after "Ex parte" - limit to 2-4 words
        r'Ex parte\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
        # Pattern 5: Names after "In re" or "In the matter of" - limit to 2-4 words
        r'(?:In re|In the matter of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
        # Pattern 6: Names after "State v" or "Republic v" - limit to 2-4 words
        r'(?:State|Republic)\s+v\.?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, title, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                # Handle patterns that capture multiple groups
                for name in match:
                    if name and len(name.strip()) > 2:
                        names.append(name.strip())
            else:
                if match and len(match.strip()) > 2:
                    names.append(match.strip())
    
    # Additional processing to clean up names and filter out company names/case titles
    cleaned_names = []
    for name in names:
        # Extensive list of terms to filter out (company indicators, legal terms, etc.)
        filter_terms = [
            'Ltd', 'Limited', 'Company', 'Corp', 'Corporation', 'Inc', 'Incorporated',
            'Bank', 'Insurance', 'Group', 'Holdings', 'Enterprises', 'Services', 'Ghana',
            'Co', 'vs', 'v', 'and', 'AND', 'versus', 'against', 'against', 'et', 'al',
            'ENTERPRISE', 'ENTERPRISES', 'LIMITED', 'COMPANY', 'CORPORATION', 'BANK',
            'INSURANCE', 'GROUP', 'HOLDINGS', 'SERVICES', 'GHANA', 'LTD', 'CORP',
            'INC', 'INCORPORATED', 'CO', 'VS', 'V', 'AND', 'VERSUS', 'AGAINST',
            'ET', 'AL', 'ENTERPRISE', 'ENTERPRISES', 'LIMITED', 'COMPANY',
            'CORPORATION', 'BANK', 'INSURANCE', 'GROUP', 'HOLDINGS', 'SERVICES',
            'GHANA', 'LTD', 'CORP', 'INC', 'INCORPORATED', 'CO', 'VS', 'V',
            'AND', 'VERSUS', 'AGAINST', 'ET', 'AL'
        ]
        
        # Split by spaces and filter out unwanted terms
        name_parts = name.split()
        filtered_parts = [part for part in name_parts if part.upper() not in filter_terms]
        
        # Only keep names with 2-4 words (typical person name length)
        if 2 <= len(filtered_parts) <= 4:
            cleaned_name = ' '.join(filtered_parts)
            
            # Additional checks to ensure it's a person name
            if (len(cleaned_name) > 4 and 
                not any(term in cleaned_name.upper() for term in ['ENTERPRISE', 'COMPANY', 'BANK', 'INSURANCE', 'GROUP', 'HOLDINGS', 'SERVICES', 'LTD', 'CORP', 'INC', 'LIMITED']) and
                not re.search(r'\b(?:vs|v|versus|against)\b', cleaned_name, re.IGNORECASE)):
                
                # Check if this is a combined name with "AND" and split it
                if ' AND ' in cleaned_name.upper():
                    parts = re.split(r'\s+AND\s+', cleaned_name, flags=re.IGNORECASE)
                    for part in parts:
                        part = part.strip()
                        if (len(part) > 4 and 
                            2 <= len(part.split()) <= 4 and
                            not any(term in part.upper() for term in ['ENTERPRISE', 'COMPANY', 'BANK', 'INSURANCE', 'GROUP', 'HOLDINGS', 'SERVICES', 'LTD', 'CORP', 'INC', 'LIMITED'])):
                            cleaned_names.append(part)
                else:
                    cleaned_names.append(cleaned_name)
    
    return list(set(cleaned_names))  # Remove duplicates

def generate_person_data(full_name):
    """Generate additional person data for the extracted name"""
    name_parts = full_name.split()
    first_name = name_parts[0] if name_parts else fake.first_name()
    last_name = name_parts[-1] if len(name_parts) > 1 else fake.last_name()
    
    # Generate additional data
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
    
    # Generate Ghanaian phone number
    phone_prefixes = ['024', '054', '055', '059', '020', '050', '026', '027', '028', '056', '057']
    phone_number = f"+233{random.choice(phone_prefixes)}{fake.random_number(digits=7)}"
    
    # Generate email
    email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
    
    # Generate address
    address = fake.address().replace('\n', ', ')
    
    # Generate Ghanaian cities and regions
    ghana_cities = ['Accra', 'Kumasi', 'Tamale', 'Takoradi', 'Cape Coast', 'Koforidua', 'Sunyani', 'Ho', 'Bolgatanga', 'Wa']
    ghana_regions = ['GAR', 'ASR', 'NR', 'WR', 'CR', 'ER', 'VR', 'BR', 'UER', 'UWR']
    
    city = random.choice(ghana_cities)
    region = random.choice(ghana_regions)
    
    # Generate occupation
    occupations = [
        'Lawyer', 'Judge', 'Business Owner', 'Civil Servant', 'Teacher', 'Doctor', 'Engineer',
        'Accountant', 'Banker', 'Farmer', 'Trader', 'Student', 'Retired', 'Unemployed',
        'Politician', 'Journalist', 'Artist', 'Musician', 'Sports Person', 'Consultant'
    ]
    
    occupation = random.choice(occupations)
    
    # Generate case types
    case_types = [
        'Civil', 'Criminal', 'Commercial', 'Family', 'Property', 'Employment', 'Contract',
        'Tort', 'Constitutional', 'Administrative', 'Tax', 'Immigration', 'Personal Injury'
    ]
    
    # Generate languages
    languages = ['English', 'Twi', 'Ga', 'Ewe', 'Hausa', 'Dagbani', 'Fante', 'Akan']
    person_languages = random.sample(languages, random.randint(1, 3))
    
    # Generate previous names (some people might have changed names)
    previous_names = []
    if random.random() < 0.3:  # 30% chance of having previous names
        prev_first = fake.first_name()
        prev_last = fake.last_name()
        previous_names = [f"{prev_first} {prev_last}"]
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'full_name': full_name,
        'date_of_birth': date_of_birth,
        'phone_number': phone_number,
        'email': email,
        'address': address,
        'city': city,
        'region': region,
        'occupation': occupation,
        'case_types': case_types[:random.randint(1, 3)],
        'languages': person_languages,
        'previous_names': previous_names,
        'is_verified': random.choice([True, False]),
        'status': 'ACTIVE',
        'notes': f"Name extracted from case titles. {occupation} with {len(person_languages)} languages."
    }

def main():
    """Main function to extract names and populate people table"""
    print("Starting name extraction from case titles...")
    
    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        # Get all case titles
        print("Fetching case titles...")
        cursor.execute("SELECT id, title FROM reported_cases WHERE title IS NOT NULL AND title != ''")
        cases = cursor.fetchall()
        
        print(f"Found {len(cases)} cases to process")
        
        # Extract names from all titles
        all_names = set()  # Use set to avoid duplicates
        case_name_mapping = {}  # Track which names came from which cases
        
        for case_id, title in cases:
            names = extract_names_from_title(title)
            for name in names:
                all_names.add(name)
                if name not in case_name_mapping:
                    case_name_mapping[name] = []
                case_name_mapping[name].append(case_id)
        
        print(f"Extracted {len(all_names)} unique names")
        
        # Clear existing people data (optional - comment out if you want to keep existing data)
        print("Clearing existing people data...")
        cursor.execute("DELETE FROM people")
        conn.commit()
        
        # Insert extracted names into people table
        print("Inserting names into people table...")
        inserted_count = 0
        
        for full_name in all_names:
            try:
                person_data = generate_person_data(full_name)
                
                # Insert into people table
                cursor.execute("""
                    INSERT INTO people (
                        first_name, last_name, full_name, date_of_birth, phone_number, email, address,
                        city, region, occupation, case_types, languages, previous_names,
                        is_verified, status, notes, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    person_data['first_name'],
                    person_data['last_name'],
                    person_data['full_name'],
                    person_data['date_of_birth'],
                    person_data['phone_number'],
                    person_data['email'],
                    person_data['address'],
                    person_data['city'],
                    person_data['region'],
                    person_data['occupation'],
                    json.dumps(person_data['case_types']),
                    json.dumps(person_data['languages']),
                    json.dumps(person_data['previous_names']),
                    person_data['is_verified'],
                    person_data['status'],
                    person_data['notes'],
                    datetime.now(),
                    datetime.now()
                ))
                
                inserted_count += 1
                
                if inserted_count % 100 == 0:
                    print(f"Inserted {inserted_count} people...")
                    
            except Exception as e:
                print(f"Error inserting {full_name}: {e}")
                continue
        
        conn.commit()
        print(f"Successfully inserted {inserted_count} people into the database")
        
        # Show some statistics
        cursor.execute("SELECT COUNT(*) FROM people")
        total_people = cursor.fetchone()[0]
        
        cursor.execute("SELECT region, COUNT(*) FROM people GROUP BY region ORDER BY COUNT(*) DESC LIMIT 5")
        region_stats = cursor.fetchall()
        
        cursor.execute("SELECT occupation, COUNT(*) FROM people GROUP BY occupation ORDER BY COUNT(*) DESC LIMIT 5")
        occupation_stats = cursor.fetchall()
        
        print(f"\n=== EXTRACTION COMPLETE ===")
        print(f"Total people in database: {total_people}")
        print(f"\nTop regions:")
        for region, count in region_stats:
            print(f"  {region}: {count}")
        
        print(f"\nTop occupations:")
        for occupation, count in occupation_stats:
            print(f"  {occupation}: {count}")
        
        # Show some sample names
        cursor.execute("SELECT full_name, city, occupation FROM people ORDER BY RAND() LIMIT 10")
        sample_people = cursor.fetchall()
        
        print(f"\nSample extracted names:")
        for name, city, occupation in sample_people:
            print(f"  {name} - {city} - {occupation}")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
