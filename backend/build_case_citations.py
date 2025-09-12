#!/usr/bin/env python3
"""
Case Citation Builder

This script analyzes case decisions to find which cases cite other cases,
and builds a reverse citation index for efficient lookup.
"""

import os
import sys
import re
import json
from datetime import datetime
from typing import Dict, List, Set, Optional
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, SessionLocal
from models.reported_cases import ReportedCases
from models.case_metadata import CaseMetadata
from sqlalchemy.orm import Session
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CaseCitationBuilder:
    def __init__(self):
        self.db = SessionLocal()
        self.citation_patterns = [
            # Common case citation patterns
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+vs\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+v\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+and\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+&amp;\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+&\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            # Single party patterns
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+case',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+decision',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+judgment',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.citation_patterns]
    
    def extract_case_citations(self, text: str) -> Set[str]:
        """Extract potential case citations from text."""
        if not text:
            return set()
        
        citations = set()
        text_lower = text.lower()
        
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    # Handle two-party cases
                    if len(match) == 2:
                        case_name = f"{match[0]} vs {match[1]}"
                        citations.add(case_name)
                        # Also add individual parties
                        citations.add(match[0])
                        citations.add(match[1])
                    else:
                        citations.add(match[0])
                else:
                    citations.add(match)
        
        # Clean up citations
        cleaned_citations = set()
        for citation in citations:
            # Remove common words that aren't part of case names
            citation = re.sub(r'\b(case|decision|judgment|ruling|matter|proceedings?)\b', '', citation, flags=re.IGNORECASE)
            citation = citation.strip()
            if len(citation) > 2 and len(citation) < 100:  # Reasonable length
                cleaned_citations.add(citation)
        
        return cleaned_citations
    
    def normalize_case_title(self, title: str) -> str:
        """Normalize case title for better matching."""
        if not title:
            return ""
        
        # Convert to lowercase and clean up
        normalized = title.lower().strip()
        
        # Remove common variations
        normalized = re.sub(r'\s+vs\.?\s+', ' vs ', normalized)
        normalized = re.sub(r'\s+v\.?\s+', ' vs ', normalized)
        normalized = re.sub(r'\s+and\s+', ' vs ', normalized)
        normalized = re.sub(r'\s+&\s+', ' vs ', normalized)
        normalized = re.sub(r'\s+&amp;\s+', ' vs ', normalized)
        
        # Remove extra spaces
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def find_citing_cases(self, target_case: ReportedCases) -> List[Dict]:
        """Find all cases that cite the target case."""
        if not target_case.title:
            return []
        
        target_title = self.normalize_case_title(target_case.title)
        citing_cases = []
        
        # Get all cases with decision text
        cases_query = self.db.query(ReportedCases).filter(
            ReportedCases.decision.isnot(None),
            ReportedCases.decision != "",
            ReportedCases.id != target_case.id
        )
        
        logger.info(f"Searching for citations of: {target_case.title}")
        logger.info(f"Normalized title: {target_title}")
        
        total_cases = cases_query.count()
        processed = 0
        
        for case in cases_query:
            try:
                # Extract citations from decision text
                citations = self.extract_case_citations(case.decision)
                
                # Check if this case cites our target case
                case_cites_target = False
                citation_context = ""
                
                for citation in citations:
                    citation_normalized = self.normalize_case_title(citation)
                    
                    # Check for exact match or partial match
                    if (citation_normalized == target_title or 
                        target_title in citation_normalized or 
                        citation_normalized in target_title):
                        case_cites_target = True
                        citation_context = citation
                        break
                
                if case_cites_target:
                    citing_cases.append({
                        'id': case.id,
                        'title': case.title,
                        'date': case.date,
                        'court_type': case.court_type,
                        'citation_context': citation_context,
                        'suit_reference_number': case.suit_reference_number
                    })
                
                processed += 1
                if processed % 1000 == 0:
                    logger.info(f"Processed {processed}/{total_cases} cases")
            
            except Exception as e:
                logger.error(f"Error processing case {case.id}: {str(e)}")
                continue
        
        logger.info(f"Found {len(citing_cases)} cases citing '{target_case.title}'")
        return citing_cases
    
    def build_citation_index(self, limit: Optional[int] = None, batch_size: int = 100):
        """Build a complete citation index for all cases."""
        logger.info("Starting citation index build...")
        
        # Get all cases with decision text
        query = self.db.query(ReportedCases).filter(
            ReportedCases.decision.isnot(None),
            ReportedCases.decision != ""
        )
        
        if limit:
            query = query.limit(limit)
        
        total_cases = query.count()
        logger.info(f"Building citation index for {total_cases} cases")
        
        citation_index = {}
        processed = 0
        
        # Process in batches
        offset = 0
        while offset < total_cases:
            cases = query.offset(offset).limit(batch_size).all()
            if not cases:
                break
            
            logger.info(f"Processing batch {offset//batch_size + 1} ({len(cases)} cases)")
            
            for case in cases:
                try:
                    # Find cases that cite this case
                    citing_cases = self.find_citing_cases(case)
                    
                    if citing_cases:
                        citation_index[case.id] = {
                            'case_title': case.title,
                            'citing_cases': citing_cases,
                            'citation_count': len(citing_cases)
                        }
                    
                    processed += 1
                    
                    if processed % 100 == 0:
                        logger.info(f"Processed {processed}/{total_cases} cases")
                
                except Exception as e:
                    logger.error(f"Error processing case {case.id}: {str(e)}")
                    continue
            
            offset += batch_size
        
        # Save citation index to file
        index_file = 'case_citation_index.json'
        with open(index_file, 'w') as f:
            json.dump(citation_index, f, indent=2, default=str)
        
        logger.info(f"Citation index saved to {index_file}")
        logger.info(f"Total cases with citations: {len(citation_index)}")
        
        return citation_index
    
    def get_citing_cases(self, case_id: int) -> List[Dict]:
        """Get cases that cite the specified case."""
        # Try to load from file first
        index_file = 'case_citation_index.json'
        if os.path.exists(index_file):
            try:
                with open(index_file, 'r') as f:
                    citation_index = json.load(f)
                    if str(case_id) in citation_index:
                        return citation_index[str(case_id)]['citing_cases']
            except Exception as e:
                logger.error(f"Error loading citation index: {str(e)}")
        
        # Fallback to real-time search
        case = self.db.query(ReportedCases).filter(ReportedCases.id == case_id).first()
        if not case:
            return []
        
        return self.find_citing_cases(case)
    
    def update_case_metadata_citations(self, case_id: int, citing_cases: List[Dict]):
        """Update case metadata with citation information."""
        try:
            metadata = self.db.query(CaseMetadata).filter(CaseMetadata.case_id == case_id).first()
            
            if metadata:
                # Store citation data as JSON
                citation_data = {
                    'citing_cases': citing_cases,
                    'citation_count': len(citing_cases),
                    'last_updated': datetime.utcnow().isoformat()
                }
                
                # Store in cases_cited field (repurposing it for reverse citations)
                metadata.cases_cited = json.dumps(citation_data)
                metadata.updated_at = datetime.utcnow()
                
                self.db.commit()
                logger.info(f"Updated case {case_id} with {len(citing_cases)} citations")
            else:
                logger.warning(f"No metadata found for case {case_id}")
        
        except Exception as e:
            logger.error(f"Error updating metadata for case {case_id}: {str(e)}")
            self.db.rollback()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Build case citation index")
    parser.add_argument("--limit", type=int, help="Limit number of cases to process")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size for processing")
    parser.add_argument("--case-id", type=int, help="Get citations for specific case ID")
    parser.add_argument("--build-index", action="store_true", help="Build complete citation index")
    
    args = parser.parse_args()
    
    builder = CaseCitationBuilder()
    
    if args.case_id:
        # Get citations for specific case
        citing_cases = builder.get_citing_cases(args.case_id)
        print(f"\nCases citing case ID {args.case_id}:")
        for case in citing_cases:
            print(f"- {case['title']} (ID: {case['id']})")
        print(f"Total: {len(citing_cases)} cases")
        
        # Update metadata
        builder.update_case_metadata_citations(args.case_id, citing_cases)
    
    elif args.build_index:
        # Build complete index
        citation_index = builder.build_citation_index(limit=args.limit, batch_size=args.batch_size)
        print(f"\nCitation index built with {len(citation_index)} cases having citations")
    
    else:
        print("Please specify --case-id or --build-index")

if __name__ == "__main__":
    main()
