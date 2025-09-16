#!/usr/bin/env python3
"""
Extract people from newly added GhaLII cases and generate their analytics and statistics.
"""

import re
import logging
from datetime import datetime
from typing import List, Dict, Set, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings
from models.people import People
from models.person_analytics import PersonAnalytics
from models.person_case_statistics import PersonCaseStatistics
from services.person_analytics_service import PersonAnalyticsService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GhaLIIPeopleExtractor:
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Common titles and prefixes to filter out
        self.title_prefixes = {
            'mr', 'mrs', 'ms', 'miss', 'dr', 'prof', 'professor', 'sir', 'lady',
            'hon', 'honourable', 'justice', 'judge', 'magistrate', 'chief',
            'deputy', 'assistant', 'senior', 'junior', 'esq', 'esquire'
        }
        
        # Common legal terms to filter out
        self.legal_terms = {
            'plaintiff', 'defendant', 'appellant', 'respondent', 'petitioner',
            'applicant', 'claimant', 'complainant', 'accused', 'prosecutor',
            'counsel', 'attorney', 'solicitor', 'barrister', 'advocate',
            'court', 'tribunal', 'magistrate', 'judge', 'justice', 'commissioner',
            'registrar', 'clerk', 'bailiff', 'sheriff', 'constable', 'officer'
        }
        
        # Company suffixes to identify organizations
        self.company_suffixes = {
            'ltd', 'limited', 'inc', 'incorporated', 'corp', 'corporation',
            'llc', 'llp', 'plc', 'gmbh', 'ag', 'sa', 'sarl', 'bv', 'nv',
            'co', 'company', 'group', 'holdings', 'enterprises', 'ventures',
            'international', 'global', 'worldwide', 'services', 'solutions',
            'systems', 'technologies', 'consulting', 'partners', 'associates'
        }

    def clean_name(self, name: str) -> str:
        """Clean and normalize a person's name."""
        if not name or len(name.strip()) < 2:
            return ""
        
        # Remove extra whitespace and normalize
        name = re.sub(r'\s+', ' ', name.strip())
        
        # Remove common prefixes
        words = name.lower().split()
        if words and words[0] in self.title_prefixes:
            name = ' '.join(words[1:])
        
        # Remove common suffixes
        words = name.lower().split()
        if words and words[-1] in self.title_prefixes:
            name = ' '.join(words[:-1])
        
        # Capitalize properly
        name = ' '.join(word.capitalize() for word in name.split())
        
        return name.strip()

    def is_likely_person(self, name: str) -> bool:
        """Determine if a name is likely a person (not organization)."""
        if not name or len(name) < 2:
            return False
        
        name_lower = name.lower()
        
        # Check if it contains company suffixes
        for suffix in self.company_suffixes:
            if name_lower.endswith(suffix):
                return False
        
        # Check if it's a legal term
        if name_lower in self.legal_terms:
            return False
        
        # Check if it's too short or too long
        if len(name) < 2 or len(name) > 100:
            return False
        
        # Check if it contains only numbers or special characters
        if not re.search(r'[a-zA-Z]', name):
            return False
        
        # Check if it has reasonable structure (at least 2 words, not too many)
        words = name.split()
        if len(words) < 1 or len(words) > 5:
            return False
        
        return True

    def extract_people_from_title(self, title: str) -> List[str]:
        """Extract potential people names from a case title."""
        if not title:
            return []
        
        people = []
        
        # Common patterns for case titles
        patterns = [
            # "A vs B" or "A v B" pattern
            r'([A-Za-z\s,\.]+?)\s+(?:vs?\.?|v\.?)\s+([A-Za-z\s,\.]+?)(?:\s|$)',
            # "A and B vs C" pattern
            r'([A-Za-z\s,\.]+?)\s+and\s+([A-Za-z\s,\.]+?)\s+(?:vs?\.?|v\.?)\s+([A-Za-z\s,\.]+?)(?:\s|$)',
            # "A, B and C vs D" pattern
            r'([A-Za-z\s,\.]+?)\s+(?:vs?\.?|v\.?)\s+([A-Za-z\s,\.]+?)(?:\s|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, title, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    for name in match:
                        if name and name.strip():
                            people.append(name.strip())
                else:
                    if match and match.strip():
                        people.append(match.strip())
        
        # Also try to extract names from other parts of the title
        # Look for capitalized words that might be names
        words = title.split()
        potential_names = []
        current_name = []
        
        for i, word in enumerate(words):
            # If word starts with capital and is not a common legal term
            if word[0].isupper() and len(word) > 1:
                current_name.append(word)
            else:
                if len(current_name) >= 2:  # At least 2 words for a name
                    potential_names.append(' '.join(current_name))
                current_name = []
        
        # Add the last potential name
        if len(current_name) >= 2:
            potential_names.append(' '.join(current_name))
        
        people.extend(potential_names)
        
        # Clean and filter the extracted names
        cleaned_people = []
        for person in people:
            cleaned = self.clean_name(person)
            if cleaned and self.is_likely_person(cleaned):
                cleaned_people.append(cleaned)
        
        return list(set(cleaned_people))  # Remove duplicates

    def extract_people_from_ghalii_cases(self) -> Dict[str, int]:
        """Extract people from all GhaLII cases and save to database."""
        db = self.SessionLocal()
        stats = {
            'cases_processed': 0,
            'people_extracted': 0,
            'people_saved': 0,
            'people_updated': 0,
            'errors': 0
        }
        
        try:
            # Get all GhaLII cases (district and circuit)
            cases = db.execute(text("""
                SELECT id, title, protagonist, antagonist, court_type, citation
                FROM reported_cases 
                WHERE court_type IN ('district', 'circuit')
                ORDER BY created_at DESC
            """)).fetchall()
            
            logger.info(f"Processing {len(cases)} GhaLII cases...")
            
            for case in cases:
                try:
                    case_id, title, protagonist, antagonist, court_type, citation = case
                    stats['cases_processed'] += 1
                    
                    # Extract people from title
                    title_people = self.extract_people_from_title(title)
                    
                    # Also check protagonist and antagonist
                    all_people = set(title_people)
                    if protagonist:
                        all_people.add(self.clean_name(protagonist))
                    if antagonist:
                        all_people.add(self.clean_name(antagonist))
                    
                    # Filter out empty names and non-people
                    valid_people = [p for p in all_people if p and self.is_likely_person(p)]
                    stats['people_extracted'] += len(valid_people)
                    
                    # Save each person to database
                    for person_name in valid_people:
                        try:
                            # Check if person already exists
                            existing_person = db.query(People).filter(
                                People.name.ilike(f"%{person_name}%")
                            ).first()
                            
                            if existing_person:
                                # Update existing person
                                existing_person.updated_at = datetime.utcnow()
                                stats['people_updated'] += 1
                                logger.info(f"Updated existing person: {person_name}")
                            else:
                                # Create new person
                                new_person = People(
                                    name=person_name,
                                    nationality="Ghanaian",  # Default for GhaLII cases
                                    occupation="Unknown",
                                    email="",
                                    contact="",
                                    tax_identification_number="",
                                    other_directorship="",
                                    created_at=datetime.utcnow(),
                                    updated_at=datetime.utcnow()
                                )
                                db.add(new_person)
                                stats['people_saved'] += 1
                                logger.info(f"Saved new person: {person_name}")
                            
                        except Exception as e:
                            logger.error(f"Error saving person {person_name}: {str(e)}")
                            stats['errors'] += 1
                    
                    # Commit after each case
                    db.commit()
                    
                    if stats['cases_processed'] % 10 == 0:
                        logger.info(f"Processed {stats['cases_processed']} cases...")
                        
                except Exception as e:
                    logger.error(f"Error processing case {case_id}: {str(e)}")
                    stats['errors'] += 1
                    db.rollback()
                    continue
            
            logger.info("People extraction completed!")
            logger.info(f"Stats: {stats}")
            
        except Exception as e:
            logger.error(f"Error in extraction process: {str(e)}")
            stats['errors'] += 1
            db.rollback()
        finally:
            db.close()
        
        return stats

    def generate_people_analytics(self) -> Dict[str, int]:
        """Generate analytics and statistics for all people."""
        db = self.SessionLocal()
        stats = {
            'analytics_generated': 0,
            'statistics_generated': 0,
            'errors': 0
        }
        
        try:
            # Create analytics service with database session
            person_analytics_service = PersonAnalyticsService(db)
            
            # Get all people
            people = db.query(People).all()
            logger.info(f"Generating analytics for {len(people)} people...")
            
            for person in people:
                try:
                    # Generate analytics
                    analytics = person_analytics_service.generate_person_analytics(person.id)
                    if analytics:
                        stats['analytics_generated'] += 1
                    
                    # Generate case statistics
                    case_stats = person_analytics_service.generate_person_case_statistics(person.id)
                    if case_stats:
                        stats['statistics_generated'] += 1
                    
                    if (stats['analytics_generated'] + stats['statistics_generated']) % 50 == 0:
                        logger.info(f"Generated analytics for {stats['analytics_generated']} people...")
                        
                except Exception as e:
                    logger.error(f"Error generating analytics for person {person.id}: {str(e)}")
                    stats['errors'] += 1
                    continue
            
            logger.info("Analytics generation completed!")
            logger.info(f"Stats: {stats}")
            
        except Exception as e:
            logger.error(f"Error in analytics generation: {str(e)}")
            stats['errors'] += 1
        finally:
            db.close()
        
        return stats

def main():
    """Main function to run the extraction and analytics generation."""
    extractor = GhaLIIPeopleExtractor()
    
    logger.info("Starting GhaLII people extraction...")
    
    # Extract people from cases
    extraction_stats = extractor.extract_people_from_ghalii_cases()
    logger.info(f"Extraction completed: {extraction_stats}")
    
    # Generate analytics and statistics
    logger.info("Starting analytics generation...")
    analytics_stats = extractor.generate_people_analytics()
    logger.info(f"Analytics generation completed: {analytics_stats}")
    
    # Final summary
    logger.info("=" * 50)
    logger.info("FINAL SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Cases processed: {extraction_stats['cases_processed']}")
    logger.info(f"People extracted: {extraction_stats['people_extracted']}")
    logger.info(f"People saved: {extraction_stats['people_saved']}")
    logger.info(f"People updated: {extraction_stats['people_updated']}")
    logger.info(f"Analytics generated: {analytics_stats['analytics_generated']}")
    logger.info(f"Statistics generated: {analytics_stats['statistics_generated']}")
    logger.info(f"Total errors: {extraction_stats['errors'] + analytics_stats['errors']}")
    logger.info("=" * 50)

if __name__ == "__main__":
    main()
