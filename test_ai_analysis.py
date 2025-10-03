#!/usr/bin/env python3
"""
Test script for AI case analysis functionality.
This script tests the AI analysis service with a sample case.
"""

import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.config import settings
from backend.services.ai_case_analysis_service import AICaseAnalysisService
from backend.models.reported_cases import ReportedCases

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ai_analysis():
    """Test AI analysis with a sample case"""
    try:
        # Initialize database connection
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get a sample case
        sample_case = db.query(ReportedCases).filter(
            ReportedCases.decision.isnot(None),
            ReportedCases.decision != ''
        ).first()
        
        if not sample_case:
            logger.error("No cases with decision content found for testing")
            return
        
        logger.info(f"Testing AI analysis with case ID: {sample_case.id}")
        logger.info(f"Case title: {sample_case.title}")
        
        # Initialize AI service
        ai_service = AICaseAnalysisService(db)
        
        # Test analysis
        analysis = ai_service.analyze_case(sample_case)
        
        logger.info("AI Analysis Results:")
        logger.info("=" * 50)
        logger.info(f"Case Outcome: {analysis.get('case_outcome', 'N/A')}")
        logger.info(f"Court Orders: {analysis.get('court_orders', 'N/A')}")
        logger.info(f"Financial Impact: {analysis.get('financial_impact', 'N/A')}")
        logger.info(f"Detailed Outcome: {analysis.get('detailed_outcome', 'N/A')}")
        
        # Test updating the case
        success = ai_service.update_case_with_ai_analysis(sample_case.id)
        
        if success:
            logger.info("✅ Case successfully updated with AI analysis")
        else:
            logger.error("❌ Failed to update case with AI analysis")
        
        # Get updated case
        updated_case = db.query(ReportedCases).filter(ReportedCases.id == sample_case.id).first()
        
        logger.info("\nUpdated Case AI Fields:")
        logger.info("=" * 50)
        logger.info(f"AI Case Outcome: {updated_case.ai_case_outcome}")
        logger.info(f"AI Court Orders: {updated_case.ai_court_orders}")
        logger.info(f"AI Financial Impact: {updated_case.ai_financial_impact}")
        logger.info(f"AI Detailed Outcome: {updated_case.ai_detailed_outcome}")
        logger.info(f"Generated At: {updated_case.ai_summary_generated_at}")
        logger.info(f"Version: {updated_case.ai_summary_version}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_ai_analysis()
