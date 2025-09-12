#!/usr/bin/env python3
"""
AI Case Summary Generator

This script generates intelligent case summaries from the decision column
and stores them in the case_metadata table.
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Optional, List
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

class AICaseSummarizer:
    def __init__(self):
        self.db = SessionLocal()
    
    def generate_summary(self, decision_text: str, title: str = "", court_type: str = "") -> str:
        """
        Generate an intelligent case summary from the decision text.
        This is a rule-based approach that extracts key information.
        """
        if not decision_text or len(decision_text.strip()) < 50:
            return ""
        
        # Clean the text
        text = decision_text.strip()
        
        # Extract key elements
        summary_parts = []
        
        # Try to extract the main holding/decision
        holding = self._extract_holding(text)
        if holding:
            summary_parts.append(f"HOLDING: {holding}")
        
        # Try to extract key facts
        facts = self._extract_key_facts(text, title)
        if facts:
            summary_parts.append(f"FACTS: {facts}")
        
        # Try to extract legal principles
        principles = self._extract_legal_principles(text)
        if principles:
            summary_parts.append(f"LEGAL PRINCIPLES: {principles}")
        
        # Try to extract outcome
        outcome = self._extract_outcome(text)
        if outcome:
            summary_parts.append(f"OUTCOME: {outcome}")
        
        # If we have good parts, join them
        if summary_parts:
            summary = " | ".join(summary_parts)
            # Limit to reasonable length
            if len(summary) > 800:
                summary = summary[:800] + "..."
            return summary
        
        # Fallback: create a basic summary
        return self._create_basic_summary(text, title, court_type)
    
    def _extract_holding(self, text: str) -> Optional[str]:
        """Extract the main holding or decision from the text."""
        # Look for common holding patterns
        holding_patterns = [
            r"(?:holding|decision|ruling|conclusion)[:\s]+([^.]{20,200})",
            r"(?:the court|this court|we|i)\s+(?:holds?|finds?|concludes?|rules?)\s+that\s+([^.]{20,200})",
            r"(?:therefore|accordingly|in conclusion)[,\s]+([^.]{20,200})",
        ]
        
        import re
        for pattern in holding_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                holding = match.group(1).strip()
                if len(holding) > 20:
                    return holding
        return None
    
    def _extract_key_facts(self, text: str, title: str) -> Optional[str]:
        """Extract key facts from the case."""
        # Use the title to understand the parties
        if title and " vs " in title:
            parties = title.split(" vs ")[0].strip()
            if len(parties) < 100:
                return f"Case involving {parties}"
        
        # Look for fact patterns
        fact_patterns = [
            r"(?:facts?|background|circumstances)[:\s]+([^.]{30,200})",
            r"(?:the plaintiff|the defendant|the appellant|the respondent)\s+([^.]{20,150})",
        ]
        
        import re
        for pattern in fact_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                facts = match.group(1).strip()
                if len(facts) > 20:
                    return facts
        return None
    
    def _extract_legal_principles(self, text: str) -> Optional[str]:
        """Extract legal principles or statutes mentioned."""
        # Look for legal references
        legal_patterns = [
            r"(?:section|article|act|law|statute|provision)\s+[\d\w\s]+(?:of\s+[\w\s]+)?",
            r"(?:principle|rule|doctrine|test)\s+(?:of\s+)?[\w\s]+",
            r"(?:constitutional|statutory|common law|equitable)\s+[\w\s]+",
        ]
        
        import re
        principles = []
        for pattern in legal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:3]:  # Limit to first 3 matches
                if len(match.strip()) > 10:
                    principles.append(match.strip())
        
        if principles:
            return "; ".join(principles)
        return None
    
    def _extract_outcome(self, text: str) -> Optional[str]:
        """Extract the outcome or result of the case."""
        outcome_patterns = [
            r"(?:appeal|application|motion|petition)\s+(?:is\s+)?(?:allowed|dismissed|granted|refused|upheld|overturned)",
            r"(?:judgment|decision|ruling)\s+(?:is\s+)?(?:for|against|in favor of|in favour of)",
            r"(?:plaintiff|defendant|appellant|respondent)\s+(?:succeeds?|fails?|wins?|loses?)",
        ]
        
        import re
        for pattern in outcome_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        return None
    
    def _create_basic_summary(self, text: str, title: str, court_type: str) -> str:
        """Create a basic summary when specific patterns aren't found."""
        # Get first few sentences
        sentences = text.split('. ')
        if len(sentences) > 3:
            summary = '. '.join(sentences[:3]) + '.'
        else:
            summary = text[:300] + "..." if len(text) > 300 else text
        
        # Add context
        context_parts = []
        if court_type:
            context_parts.append(f"Court: {court_type}")
        if title and " vs " in title:
            parties = title.split(" vs ")[0].strip()
            context_parts.append(f"Parties: {parties}")
        
        if context_parts:
            summary = f"{' | '.join(context_parts)} | {summary}"
        
        return summary
    
    def process_cases(self, limit: Optional[int] = None, batch_size: int = 100):
        """Process cases to generate AI summaries."""
        logger.info("Starting AI case summary generation...")
        
        # Get cases that need processing
        query = self.db.query(ReportedCases).filter(
            ReportedCases.decision.isnot(None),
            ReportedCases.decision != ""
        )
        
        if limit:
            query = query.limit(limit)
        
        total_cases = query.count()
        logger.info(f"Found {total_cases} cases with decision data to process")
        
        processed = 0
        updated = 0
        created = 0
        
        # Process in batches
        offset = 0
        while offset < total_cases:
            cases = query.offset(offset).limit(batch_size).all()
            if not cases:
                break
            
            logger.info(f"Processing batch {offset//batch_size + 1} ({len(cases)} cases)")
            
            for case in cases:
                try:
                    # Generate AI summary
                    ai_summary = self.generate_summary(
                        case.decision,
                        case.title or "",
                        case.court_type or ""
                    )
                    
                    if not ai_summary:
                        logger.warning(f"No summary generated for case {case.id}")
                        processed += 1
                        continue
                    
                    # Check if metadata exists
                    metadata = self.db.query(CaseMetadata).filter(
                        CaseMetadata.case_id == case.id
                    ).first()
                    
                    if metadata:
                        # Update existing metadata
                        metadata.case_summary = ai_summary
                        metadata.updated_at = datetime.utcnow()
                        updated += 1
                    else:
                        # Create new metadata
                        metadata = CaseMetadata(
                            case_id=case.id,
                            case_summary=ai_summary,
                            case_type=case.type,
                            area_of_law=case.area_of_law,
                            protagonist=case.protagonist,
                            antagonist=case.antagonist,
                            court_type=case.court_type,
                            court_division=case.court_division,
                            is_processed=True,
                            processed_at=datetime.utcnow()
                        )
                        self.db.add(metadata)
                        created += 1
                    
                    processed += 1
                    
                    if processed % 50 == 0:
                        logger.info(f"Processed {processed}/{total_cases} cases")
                        self.db.commit()
                
                except Exception as e:
                    logger.error(f"Error processing case {case.id}: {str(e)}")
                    continue
            
            # Commit batch
            try:
                self.db.commit()
                logger.info(f"Batch committed successfully")
            except Exception as e:
                logger.error(f"Error committing batch: {str(e)}")
                self.db.rollback()
            
            offset += batch_size
        
        logger.info(f"AI Summary Generation Complete!")
        logger.info(f"Total processed: {processed}")
        logger.info(f"Metadata updated: {updated}")
        logger.info(f"Metadata created: {created}")
        
        return {
            "processed": processed,
            "updated": updated,
            "created": created
        }
    
    def get_summary_stats(self):
        """Get statistics about generated summaries."""
        total_cases = self.db.query(ReportedCases).count()
        cases_with_decision = self.db.query(ReportedCases).filter(
            ReportedCases.decision.isnot(None),
            ReportedCases.decision != ""
        ).count()
        cases_with_ai_summary = self.db.query(CaseMetadata).filter(
            CaseMetadata.case_summary.isnot(None),
            CaseMetadata.case_summary != ""
        ).count()
        
        return {
            "total_cases": total_cases,
            "cases_with_decision": cases_with_decision,
            "cases_with_ai_summary": cases_with_ai_summary,
            "coverage_percentage": (cases_with_ai_summary / cases_with_decision * 100) if cases_with_decision > 0 else 0
        }

def main():
    parser = argparse.ArgumentParser(description="Generate AI case summaries")
    parser.add_argument("--limit", type=int, help="Limit number of cases to process")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size for processing")
    parser.add_argument("--stats", action="store_true", help="Show summary statistics")
    
    args = parser.parse_args()
    
    summarizer = AICaseSummarizer()
    
    if args.stats:
        stats = summarizer.get_summary_stats()
        print(f"\n=== AI Summary Statistics ===")
        print(f"Total cases: {stats['total_cases']}")
        print(f"Cases with decision data: {stats['cases_with_decision']}")
        print(f"Cases with AI summaries: {stats['cases_with_ai_summary']}")
        print(f"Coverage: {stats['coverage_percentage']:.1f}%")
        return
    
    try:
        results = summarizer.process_cases(limit=args.limit, batch_size=args.batch_size)
        print(f"\n=== Processing Complete ===")
        print(f"Processed: {results['processed']}")
        print(f"Updated: {results['updated']}")
        print(f"Created: {results['created']}")
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        sys.exit(1)
    finally:
        summarizer.db.close()

if __name__ == "__main__":
    main()
