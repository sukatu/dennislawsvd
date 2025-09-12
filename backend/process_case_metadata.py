#!/usr/bin/env python3
"""
Case Metadata Processing Script

This script processes the reported_cases table and creates metadata
for better search functionality and case analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models.reported_cases import ReportedCases
from models.case_metadata import CaseMetadata, CaseSearchIndex
from sqlalchemy import text
import re
import json
from datetime import datetime
from typing import List, Dict, Set, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaseMetadataProcessor:
    def __init__(self):
        self.db = next(get_db())
        self.processed_count = 0
        self.error_count = 0
        
        # Common patterns for extraction
        self.person_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # First Last
            r'\b[A-Z]\. [A-Z][a-z]+\b',     # F. Last
            r'\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b',  # First M. Last
        ]
        
        self.organization_patterns = [
            r'\b[A-Z][a-z]+ (?:Bank|Insurance|Company|Corp|Ltd|Limited|Inc|Incorporated)\b',
            r'\b(?:Bank|Insurance|Company|Corp|Ltd|Limited|Inc|Incorporated) of [A-Z][a-z]+\b',
            r'\b[A-Z][a-z]+ (?:Group|Holdings|Enterprises|Associates)\b',
        ]
        
        self.bank_keywords = [
            'bank', 'banking', 'financial', 'credit', 'loan', 'mortgage',
            'savings', 'commercial', 'investment', 'merchant'
        ]
        
        self.insurance_keywords = [
            'insurance', 'assurance', 'coverage', 'policy', 'premium',
            'claim', 'underwriting', 'actuarial'
        ]

    def extract_people(self, text: str) -> List[str]:
        """Extract people names from text"""
        if not text:
            return []
        
        people = set()
        text = str(text)
        
        # Use regex patterns
        for pattern in self.person_patterns:
            matches = re.findall(pattern, text)
            people.update(matches)
        
        # Filter out common false positives
        false_positives = {
            'Court', 'Judge', 'Justice', 'High Court', 'Supreme Court',
            'Appeal Court', 'District Court', 'Magistrate Court',
            'Bank', 'Insurance', 'Company', 'Corp', 'Ltd', 'Limited'
        }
        
        people = [p for p in people if p not in false_positives and len(p) > 3]
        return list(people)

    def extract_organizations(self, text: str) -> List[str]:
        """Extract organization names from text"""
        if not text:
            return []
        
        organizations = set()
        text = str(text)
        
        # Use regex patterns
        for pattern in self.organization_patterns:
            matches = re.findall(pattern, text)
            organizations.update(matches)
        
        return list(organizations)

    def extract_banks(self, text: str) -> List[str]:
        """Extract bank names from text"""
        if not text:
            return []
        
        banks = set()
        text = str(text).lower()
        
        # Look for bank-related keywords
        for keyword in self.bank_keywords:
            if keyword in text:
                # Try to extract the bank name
                pattern = rf'\b[A-Z][a-z]+ (?:{keyword}|Bank|Banking)\b'
                matches = re.findall(pattern, text, re.IGNORECASE)
                banks.update(matches)
        
        return list(banks)

    def extract_insurance(self, text: str) -> List[str]:
        """Extract insurance company names from text"""
        if not text:
            return []
        
        insurance = set()
        text = str(text).lower()
        
        # Look for insurance-related keywords
        for keyword in self.insurance_keywords:
            if keyword in text:
                # Try to extract the insurance company name
                pattern = rf'\b[A-Z][a-z]+ (?:{keyword}|Insurance|Assurance)\b'
                matches = re.findall(pattern, text, re.IGNORECASE)
                insurance.update(matches)
        
        return list(insurance)

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        if not text:
            return []
        
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', str(text).lower())
        
        # Filter out common words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'under', 'over',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            'his', 'her', 'its', 'our', 'their', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'shall', 'ought', 'need', 'dare', 'used', 'court', 'case', 'judge',
            'justice', 'law', 'legal', 'plaintiff', 'defendant', 'appellant',
            'respondent', 'petitioner', 'respondent'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return list(set(keywords))[:20]  # Limit to 20 keywords

    def determine_resolution_status(self, case: ReportedCases) -> Optional[str]:
        """Determine case resolution status"""
        if not case.status:
            return None
        
        status = str(case.status).lower()
        if status in ['1', 'resolved', 'decided', 'completed']:
            return 'resolved'
        elif status in ['0', 'pending', 'ongoing', 'active']:
            return 'pending'
        elif status in ['dismissed', 'withdrawn']:
            return 'dismissed'
        else:
            return 'unknown'

    def determine_outcome(self, case: ReportedCases) -> Optional[str]:
        """Determine case outcome"""
        if not case.decision and not case.judgement:
            return None
        
        decision_text = (case.decision or case.judgement or '').lower()
        
        if any(word in decision_text for word in ['favorable', 'won', 'successful', 'granted', 'allowed']):
            return 'favorable'
        elif any(word in decision_text for word in ['unfavorable', 'lost', 'unsuccessful', 'dismissed', 'denied']):
            return 'unfavorable'
        elif any(word in decision_text for word in ['partial', 'mixed', 'some', 'partially']):
            return 'mixed'
        else:
            return 'unknown'

    def create_searchable_text(self, case: ReportedCases) -> str:
        """Create searchable text for the case"""
        text_parts = []
        
        if case.title:
            text_parts.append(case.title)
        if case.protagonist:
            text_parts.append(case.protagonist)
        if case.antagonist:
            text_parts.append(case.antagonist)
        if case.presiding_judge:
            text_parts.append(case.presiding_judge)
        if case.lawyers:
            text_parts.append(case.lawyers)
        if case.case_summary:
            text_parts.append(case.case_summary)
        if case.area_of_law:
            text_parts.append(case.area_of_law)
        if case.keywords_phrases:
            text_parts.append(case.keywords_phrases)
        if case.decision:
            text_parts.append(case.decision)
        
        return ' '.join(text_parts)

    def extract_case_summary(self, case: ReportedCases) -> str:
        """Extract case summary from decision column"""
        if not case.decision:
            return case.case_summary or ""
        
        decision_text = str(case.decision).strip()
        
        # If decision is too long, truncate it to a reasonable summary length
        if len(decision_text) > 1000:
            # Try to find a good breaking point (end of sentence)
            sentences = decision_text.split('. ')
            summary_parts = []
            current_length = 0
            
            for sentence in sentences:
                if current_length + len(sentence) > 800:  # Leave some room for "..."
                    break
                summary_parts.append(sentence)
                current_length += len(sentence) + 2  # +2 for ". "
            
            if summary_parts:
                summary = '. '.join(summary_parts)
                if len(summary_parts) < len(sentences):
                    summary += "..."
                return summary
            else:
                # Fallback to truncation
                return decision_text[:800] + "..."
        
        return decision_text

    def process_case(self, case: ReportedCases) -> bool:
        """Process a single case and create metadata"""
        try:
            # Check if metadata already exists
            existing_metadata = self.db.query(CaseMetadata).filter(
                CaseMetadata.case_id == case.id
            ).first()
            
            if existing_metadata and existing_metadata.is_processed:
                return True
            
            # Create searchable text
            searchable_text = self.create_searchable_text(case)
            
            # Extract case summary from decision column
            case_summary = self.extract_case_summary(case)
            
            # Extract entities
            all_text = f"{case.title or ''} {case.detail_content or ''} {case.judgement or ''} {case.decision or ''}"
            people = self.extract_people(all_text)
            organizations = self.extract_organizations(all_text)
            banks = self.extract_banks(all_text)
            insurance = self.extract_insurance(all_text)
            keywords = self.extract_keywords(all_text)
            
            # Determine status and outcome
            resolution_status = self.determine_resolution_status(case)
            outcome = self.determine_outcome(case)
            
            # Create or update metadata
            if existing_metadata:
                existing_metadata.case_summary = case_summary
                existing_metadata.case_type = case.type
                existing_metadata.area_of_law = case.area_of_law
                existing_metadata.keywords = keywords
                existing_metadata.judges = [case.presiding_judge] if case.presiding_judge else None
                existing_metadata.lawyers = [case.lawyers] if case.lawyers else None
                existing_metadata.related_people = people
                existing_metadata.protagonist = case.protagonist
                existing_metadata.antagonist = case.antagonist
                existing_metadata.organizations = organizations
                existing_metadata.banks_involved = banks
                existing_metadata.insurance_involved = insurance
                existing_metadata.resolution_status = resolution_status
                existing_metadata.outcome = outcome
                existing_metadata.court_type = case.court_type
                existing_metadata.court_division = case.court_division
                existing_metadata.statutes_cited = [case.statutes_cited] if case.statutes_cited else None
                existing_metadata.cases_cited = [case.cases_cited] if case.cases_cited else None
                existing_metadata.search_keywords = keywords
                existing_metadata.is_processed = True
                existing_metadata.processed_at = datetime.utcnow()
                existing_metadata.updated_at = datetime.utcnow()
            else:
                metadata = CaseMetadata(
                    case_id=case.id,
                    case_summary=case_summary,
                    case_type=case.type,
                    area_of_law=case.area_of_law,
                    keywords=keywords,
                    judges=[case.presiding_judge] if case.presiding_judge else None,
                    lawyers=[case.lawyers] if case.lawyers else None,
                    related_people=people,
                    protagonist=case.protagonist,
                    antagonist=case.antagonist,
                    organizations=organizations,
                    banks_involved=banks,
                    insurance_involved=insurance,
                    resolution_status=resolution_status,
                    outcome=outcome,
                    court_type=case.court_type,
                    court_division=case.court_division,
                    statutes_cited=[case.statutes_cited] if case.statutes_cited else None,
                    cases_cited=[case.cases_cited] if case.cases_cited else None,
                    search_keywords=keywords,
                    is_processed=True,
                    processed_at=datetime.utcnow()
                )
                self.db.add(metadata)
            
            # Create or update search index
            existing_index = self.db.query(CaseSearchIndex).filter(
                CaseSearchIndex.case_id == case.id
            ).first()
            
            if existing_index:
                existing_index.searchable_text = searchable_text
                existing_index.person_names = people
                existing_index.organization_names = organizations
                existing_index.keywords = keywords
                existing_index.word_count = len(searchable_text.split())
                existing_index.last_indexed = datetime.utcnow()
            else:
                search_index = CaseSearchIndex(
                    case_id=case.id,
                    searchable_text=searchable_text,
                    person_names=people,
                    organization_names=organizations,
                    keywords=keywords,
                    word_count=len(searchable_text.split())
                )
                self.db.add(search_index)
            
            self.db.commit()
            self.processed_count += 1
            
            if self.processed_count % 100 == 0:
                logger.info(f"Processed {self.processed_count} cases...")
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing case {case.id}: {str(e)}")
            self.error_count += 1
            self.db.rollback()
            return False

    def process_all_cases(self, limit: Optional[int] = None):
        """Process all cases in the database"""
        logger.info("Starting case metadata processing...")
        
        # Get cases to process
        query = self.db.query(ReportedCases)
        if limit:
            query = query.limit(limit)
        
        cases = query.all()
        total_cases = len(cases)
        
        logger.info(f"Found {total_cases} cases to process")
        
        for i, case in enumerate(cases):
            if i % 1000 == 0:
                logger.info(f"Processing case {i+1}/{total_cases} (ID: {case.id})")
            
            self.process_case(case)
        
        logger.info(f"Processing complete!")
        logger.info(f"Successfully processed: {self.processed_count}")
        logger.info(f"Errors: {self.error_count}")

    def process_unprocessed_cases(self):
        """Process only cases that haven't been processed yet"""
        logger.info("Processing unprocessed cases...")
        
        # Get cases without metadata
        cases = self.db.query(ReportedCases).outerjoin(
            CaseMetadata, ReportedCases.id == CaseMetadata.case_id
        ).filter(CaseMetadata.id.is_(None)).all()
        
        total_cases = len(cases)
        logger.info(f"Found {total_cases} unprocessed cases")
        
        for i, case in enumerate(cases):
            if i % 100 == 0:
                logger.info(f"Processing case {i+1}/{total_cases} (ID: {case.id})")
            
            self.process_case(case)
        
        logger.info(f"Processing complete!")
        logger.info(f"Successfully processed: {self.processed_count}")
        logger.info(f"Errors: {self.error_count}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process case metadata')
    parser.add_argument('--limit', type=int, help='Limit number of cases to process')
    parser.add_argument('--unprocessed-only', action='store_true', 
                       help='Process only unprocessed cases')
    
    args = parser.parse_args()
    
    processor = CaseMetadataProcessor()
    
    if args.unprocessed_only:
        processor.process_unprocessed_cases()
    else:
        processor.process_all_cases(args.limit)

if __name__ == "__main__":
    main()
