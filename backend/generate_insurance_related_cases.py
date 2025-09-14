#!/usr/bin/env python3
"""
Script to generate real related cases for all insurance companies.
This will search the reported_cases table for cases that mention each insurance company.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models.insurance import Insurance
from models.reported_cases import ReportedCases
from sqlalchemy import or_, and_
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_related_cases_for_insurance(insurance_id: int, db):
    """Find real related cases for a specific insurance company."""
    try:
        insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not insurance:
            return []
        
        # Search for cases where the insurance company name appears in various fields
        insurance_name = insurance.name
        short_name = insurance.short_name
        
        # Create search terms
        search_terms = [insurance_name]
        if short_name and short_name != insurance_name:
            search_terms.append(short_name)
        
        # Search in multiple fields
        cases = []
        for term in search_terms:
            if term:
                term_cases = db.query(ReportedCases).filter(
                    or_(
                        ReportedCases.title.like(f"%{term}%"),
                        ReportedCases.protagonist.like(f"%{term}%"),
                        ReportedCases.antagonist.like(f"%{term}%"),
                        ReportedCases.case_summary.like(f"%{term}%"),
                        ReportedCases.headnotes.like(f"%{term}%"),
                        ReportedCases.commentary.like(f"%{term}%"),
                        ReportedCases.decision.like(f"%{term}%"),
                        ReportedCases.judgement.like(f"%{term}%"),
                        ReportedCases.conclusion.like(f"%{term}%")
                    )
                ).all()
                cases.extend(term_cases)
        
        # Remove duplicates
        unique_cases = []
        seen_ids = set()
        for case in cases:
            if case.id not in seen_ids:
                unique_cases.append(case)
                seen_ids.add(case.id)
        
        return unique_cases
        
    except Exception as e:
        logger.error(f"Error finding related cases for insurance ID {insurance_id}: {e}")
        return []

def format_case_for_api(case):
    """Format a case for API response."""
    # Handle date formatting
    formatted_date = "N/A"
    if case.date:
        if hasattr(case.date, 'strftime'):
            formatted_date = case.date.strftime("%Y-%m-%d")
        elif isinstance(case.date, str):
            formatted_date = case.date
        else:
            formatted_date = str(case.date)
    
    return {
        "id": case.id,
        "title": case.title or "N/A",
        "suit_reference_number": case.suit_reference_number or "N/A",
        "court_type": case.court_type or "N/A",
        "date": formatted_date,
        "area_of_law": case.area_of_law or "N/A",
        "ai_case_outcome": case.ai_case_outcome or "N/A",
        "case_summary": case.case_summary or "N/A",
        "protagonist": case.protagonist or "N/A",
        "antagonist": case.antagonist or "N/A",
        "presiding_judge": case.presiding_judge or "N/A",
        "lawyers": case.lawyers or "N/A",
        "year": case.year or "N/A",
        "region": case.region or "N/A",
        "town": case.town or "N/A"
    }

def generate_related_cases_report():
    """Generate a comprehensive report of related cases for all insurance companies."""
    try:
        db = next(get_db())
        
        # Get all active insurance companies
        insurance_companies = db.query(Insurance).filter(Insurance.is_active == True).all()
        
        logger.info(f"Found {len(insurance_companies)} active insurance companies to analyze")
        
        total_cases_found = 0
        companies_with_cases = 0
        case_details = []
        
        for insurance in insurance_companies:
            logger.info(f"Analyzing cases for: {insurance.name} (ID: {insurance.id})")
            
            # Find related cases
            related_cases = find_related_cases_for_insurance(insurance.id, db)
            
            if related_cases:
                companies_with_cases += 1
                total_cases_found += len(related_cases)
                
                logger.info(f"  Found {len(related_cases)} related cases")
                
                # Store case details for reporting
                for case in related_cases[:5]:  # Store first 5 cases for each company
                    case_details.append({
                        "insurance_name": insurance.name,
                        "insurance_id": insurance.id,
                        "case": format_case_for_api(case)
                    })
            else:
                logger.info(f"  No related cases found")
        
        # Generate summary report
        logger.info(f"\n📊 Related Cases Summary:")
        logger.info(f"   Total insurance companies analyzed: {len(insurance_companies)}")
        logger.info(f"   Companies with related cases: {companies_with_cases}")
        logger.info(f"   Total related cases found: {total_cases_found}")
        
        # Show sample cases
        if case_details:
            logger.info(f"\n📋 Sample Related Cases:")
            for detail in case_details[:10]:  # Show first 10 cases
                case = detail["case"]
                logger.info(f"   {detail['insurance_name']}:")
                logger.info(f"     Case: {case['title']}")
                logger.info(f"     Suit Ref: {case['suit_reference_number']}")
                logger.info(f"     Court: {case['court_type']}")
                logger.info(f"     Date: {case['date']}")
                logger.info(f"     Area of Law: {case['area_of_law']}")
                logger.info(f"     Outcome: {case['ai_case_outcome']}")
                logger.info("")
        
        return {
            "total_companies": len(insurance_companies),
            "companies_with_cases": companies_with_cases,
            "total_cases": total_cases_found,
            "case_details": case_details
        }
        
    except Exception as e:
        logger.error(f"Error in generate_related_cases_report: {e}")
        raise
    finally:
        if 'db' in locals():
            db.close()

def get_related_cases_for_insurance(insurance_id: int, limit: int = 10):
    """Get related cases for a specific insurance company (for API use)."""
    try:
        db = next(get_db())
        
        # Find related cases
        related_cases = find_related_cases_for_insurance(insurance_id, db)
        
        # Format cases for API response
        formatted_cases = [format_case_for_api(case) for case in related_cases[:limit]]
        
        return {
            "insurance_id": insurance_id,
            "related_cases": formatted_cases,
            "total_related_cases": len(related_cases)
        }
        
    except Exception as e:
        logger.error(f"Error getting related cases for insurance ID {insurance_id}: {e}")
        return {
            "insurance_id": insurance_id,
            "related_cases": [],
            "total_related_cases": 0
        }
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Get related cases for specific insurance company
        insurance_id = int(sys.argv[1])
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        result = get_related_cases_for_insurance(insurance_id, limit)
        print(f"Related cases for insurance ID {insurance_id}:")
        for case in result["related_cases"]:
            print(f"  - {case['title']} ({case['suit_reference_number']})")
    else:
        # Generate comprehensive report
        generate_related_cases_report()
