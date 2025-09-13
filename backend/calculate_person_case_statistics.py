#!/usr/bin/env python3
"""
Calculate and populate case statistics for all people.
This script analyzes all cases and calculates statistics for each person.
"""

import mysql.connector
from config import settings

# Create DATABASE_CONFIG from settings
DATABASE_CONFIG = {
    'host': settings.mysql_host,
    'port': settings.mysql_port,
    'user': settings.mysql_user,
    'password': settings.mysql_password,
    'database': settings.mysql_database
}
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class PersonCaseStatisticsCalculator:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database."""
        try:
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ Connected to database successfully!")
            return True
        except mysql.connector.Error as e:
            print(f"❌ Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Database connection closed.")
    
    def get_all_people(self) -> List[Dict]:
        """Get all people from the database."""
        try:
            query = """
            SELECT id, full_name, first_name, last_name 
            FROM people 
            WHERE status = 'active' 
            ORDER BY id
            """
            self.cursor.execute(query)
            people = self.cursor.fetchall()
            print(f"📊 Found {len(people)} people to process")
            return people
        except mysql.connector.Error as e:
            print(f"❌ Error fetching people: {e}")
            return []
    
    def get_cases_for_person(self, person_id: int, person_name: str) -> List[Dict]:
        """Get all cases for a specific person."""
        try:
            # Search for cases where the person's name appears in the title
            # Use multiple search patterns to catch variations
            search_patterns = [
                person_name,
                person_name.replace(" ", ""),
                person_name.replace("-", " "),
                person_name.replace("'", ""),
                person_name.replace(".", ""),
            ]
            
            # Create a regex pattern for case-insensitive search
            pattern = "|".join([re.escape(p) for p in search_patterns])
            
            query = """
            SELECT id, title, status, decision, judgement, conclusion,
                   court_type, region, town, case_summary
            FROM reported_cases 
            WHERE title REGEXP %s
            ORDER BY id
            """
            
            self.cursor.execute(query, (pattern,))
            cases = self.cursor.fetchall()
            
            # Additional filtering to ensure relevance
            relevant_cases = []
            person_name_lower = person_name.lower()
            
            for case in cases:
                title_lower = case['title'].lower()
                # Check if person name appears in title (more strict matching)
                if (person_name_lower in title_lower or 
                    any(part in title_lower for part in person_name_lower.split() if len(part) > 2)):
                    relevant_cases.append(case)
            
            return relevant_cases
        except mysql.connector.Error as e:
            print(f"❌ Error fetching cases for {person_name}: {e}")
            return []
    
    def analyze_case_outcome(self, case: Dict) -> str:
        """Analyze a case to determine its outcome."""
        decision = case.get('decision', '').lower() if case.get('decision') else ''
        judgement = case.get('judgement', '').lower() if case.get('judgement') else ''
        conclusion = case.get('conclusion', '').lower() if case.get('conclusion') else ''
        case_summary = case.get('case_summary', '').lower() if case.get('case_summary') else ''
        
        # Combine all text for analysis
        combined_text = f"{decision} {judgement} {conclusion} {case_summary}"
        
        # Keywords for favorable outcomes
        favorable_keywords = [
            'favorable', 'won', 'success', 'successful', 'granted', 'allowed',
            'approved', 'accepted', 'dismissed', 'withdrawn', 'settled',
            'compensation', 'awarded', 'upheld', 'confirmed', 'validated'
        ]
        
        # Keywords for unfavorable outcomes
        unfavorable_keywords = [
            'unfavorable', 'lost', 'failed', 'denied', 'rejected', 'dismissed',
            'struck out', 'overruled', 'overturned', 'reversed', 'quashed',
            'liability', 'guilty', 'convicted', 'penalty', 'fine'
        ]
        
        favorable_count = sum(1 for keyword in favorable_keywords if keyword in combined_text)
        unfavorable_count = sum(1 for keyword in unfavorable_keywords if keyword in combined_text)
        
        if favorable_count > unfavorable_count:
            return 'favorable'
        elif unfavorable_count > favorable_count:
            return 'unfavorable'
        else:
            return 'mixed'
    
    def calculate_statistics(self, cases: List[Dict]) -> Dict:
        """Calculate case statistics from a list of cases."""
        total_cases = len(cases)
        resolved_cases = sum(1 for case in cases if case.get('status') == 1)
        unresolved_cases = total_cases - resolved_cases
        
        # Analyze outcomes for resolved cases
        resolved_cases_list = [case for case in cases if case.get('status') == 1]
        favorable_cases = 0
        unfavorable_cases = 0
        mixed_cases = 0
        
        for case in resolved_cases_list:
            outcome = self.analyze_case_outcome(case)
            if outcome == 'favorable':
                favorable_cases += 1
            elif outcome == 'unfavorable':
                unfavorable_cases += 1
            else:
                mixed_cases += 1
        
        # Determine overall case outcome
        if resolved_cases == 0:
            case_outcome = 'N/A'
        elif favorable_cases == resolved_cases:
            case_outcome = 'Favorable'
        elif unfavorable_cases == resolved_cases:
            case_outcome = 'Unfavorable'
        else:
            case_outcome = 'Mixed'
        
        return {
            'total_cases': total_cases,
            'resolved_cases': resolved_cases,
            'unresolved_cases': unresolved_cases,
            'favorable_cases': favorable_cases,
            'unfavorable_cases': unfavorable_cases,
            'mixed_cases': mixed_cases,
            'case_outcome': case_outcome
        }
    
    def save_statistics(self, person_id: int, stats: Dict) -> bool:
        """Save calculated statistics to the database."""
        try:
            # Check if statistics already exist
            check_query = "SELECT id FROM person_case_statistics WHERE person_id = %s"
            self.cursor.execute(check_query, (person_id,))
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing statistics
                update_query = """
                UPDATE person_case_statistics 
                SET total_cases = %s, resolved_cases = %s, unresolved_cases = %s,
                    favorable_cases = %s, unfavorable_cases = %s, mixed_cases = %s,
                    case_outcome = %s, last_updated = NOW()
                WHERE person_id = %s
                """
                values = (
                    stats['total_cases'], stats['resolved_cases'], stats['unresolved_cases'],
                    stats['favorable_cases'], stats['unfavorable_cases'], stats['mixed_cases'],
                    stats['case_outcome'], person_id
                )
                self.cursor.execute(update_query, values)
            else:
                # Insert new statistics
                insert_query = """
                INSERT INTO person_case_statistics 
                (person_id, total_cases, resolved_cases, unresolved_cases,
                 favorable_cases, unfavorable_cases, mixed_cases, case_outcome)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    person_id, stats['total_cases'], stats['resolved_cases'], stats['unresolved_cases'],
                    stats['favorable_cases'], stats['unfavorable_cases'], stats['mixed_cases'],
                    stats['case_outcome']
                )
                self.cursor.execute(insert_query, values)
            
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"❌ Error saving statistics for person {person_id}: {e}")
            self.connection.rollback()
            return False
    
    def process_all_people(self):
        """Process all people and calculate their case statistics."""
        if not self.connect():
            return False
        
        try:
            people = self.get_all_people()
            if not people:
                print("❌ No people found to process")
                return False
            
            processed = 0
            errors = 0
            
            print(f"\n🚀 Starting to process {len(people)} people...")
            print("=" * 80)
            
            for i, person in enumerate(people, 1):
                person_id = person['id']
                person_name = person['full_name']
                
                print(f"[{i:4d}/{len(people)}] Processing: {person_name}")
                
                try:
                    # Get cases for this person
                    cases = self.get_cases_for_person(person_id, person_name)
                    
                    if cases:
                        # Calculate statistics
                        stats = self.calculate_statistics(cases)
                        
                        # Save statistics
                        if self.save_statistics(person_id, stats):
                            print(f"    ✅ Found {stats['total_cases']} cases - "
                                  f"Resolved: {stats['resolved_cases']}, "
                                  f"Outcome: {stats['case_outcome']}")
                            processed += 1
                        else:
                            print(f"    ❌ Failed to save statistics")
                            errors += 1
                    else:
                        # No cases found, save empty statistics
                        empty_stats = {
                            'total_cases': 0,
                            'resolved_cases': 0,
                            'unresolved_cases': 0,
                            'favorable_cases': 0,
                            'unfavorable_cases': 0,
                            'mixed_cases': 0,
                            'case_outcome': 'N/A'
                        }
                        if self.save_statistics(person_id, empty_stats):
                            print(f"    ⚪ No cases found")
                            processed += 1
                        else:
                            print(f"    ❌ Failed to save empty statistics")
                            errors += 1
                
                except Exception as e:
                    print(f"    ❌ Error processing {person_name}: {e}")
                    errors += 1
                
                # Progress indicator
                if i % 100 == 0:
                    print(f"\n📊 Progress: {i}/{len(people)} processed, {processed} successful, {errors} errors")
                    print("-" * 80)
            
            print(f"\n🎉 Processing completed!")
            print(f"✅ Successfully processed: {processed}")
            print(f"❌ Errors: {errors}")
            print(f"📊 Total people: {len(people)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Unexpected error during processing: {e}")
            return False
        finally:
            self.disconnect()

def main():
    """Main function to run the statistics calculation."""
    print("🚀 Person Case Statistics Calculator")
    print("=" * 50)
    
    calculator = PersonCaseStatisticsCalculator()
    success = calculator.process_all_people()
    
    if success:
        print("\n✅ Case statistics calculation completed successfully!")
    else:
        print("\n❌ Case statistics calculation failed!")

if __name__ == "__main__":
    main()
