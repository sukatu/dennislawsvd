#!/usr/bin/env python3
"""
Simple test script for AI case analysis functionality.
This script tests the AI analysis service without loading problematic models.
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection and get a sample case"""
    try:
        # Initialize database connection
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get a sample case using raw SQL to avoid model loading issues
        result = db.execute(text("""
            SELECT id, title, decision, judgement, conclusion, case_summary, area_of_law, protagonist, antagonist
            FROM reported_cases 
            WHERE (decision IS NOT NULL AND decision != '') 
               OR (judgement IS NOT NULL AND judgement != '')
            LIMIT 1
        """)).fetchone()
        
        if not result:
            logger.error("No cases with decision content found for testing")
            return None
        
        case_data = {
            'id': result[0],
            'title': result[1],
            'decision': result[2],
            'judgement': result[3],
            'conclusion': result[4],
            'case_summary': result[5],
            'area_of_law': result[6],
            'protagonist': result[7],
            'antagonist': result[8]
        }
        
        logger.info(f"Found sample case: ID {case_data['id']}, Title: {case_data['title']}")
        return case_data, db
        
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None, None

def test_openai_connection():
    """Test OpenAI API connection"""
    try:
        import openai
        
        # Check environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            return False
        
        # Test with a simple request
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10
        )
        
        logger.info("OpenAI API connection successful")
        return True
        
    except Exception as e:
        logger.error(f"OpenAI API connection failed: {e}")
        return False

def test_ai_analysis_with_case(case_data, db):
    """Test AI analysis with a specific case"""
    try:
        # Import the AI service
        from backend.services.ai_case_analysis_service import AICaseAnalysisService
        
        # Create a mock case object
        class MockCase:
            def __init__(self, data):
                self.id = data['id']
                self.title = data['title']
                self.decision = data['decision']
                self.judgement = data['judgement']
                self.conclusion = data['conclusion']
                self.case_summary = data['case_summary']
                self.area_of_law = data['area_of_law']
                self.protagonist = data['protagonist']
                self.antagonist = data['antagonist']
        
        mock_case = MockCase(case_data)
        
        # Initialize AI service
        ai_service = AICaseAnalysisService(db)
        
        # Test analysis
        logger.info("Testing AI analysis...")
        analysis = ai_service.analyze_case(mock_case)
        
        logger.info("AI Analysis Results:")
        logger.info("=" * 50)
        logger.info(f"Case Outcome: {analysis.get('case_outcome', 'N/A')}")
        logger.info(f"Court Orders: {analysis.get('court_orders', 'N/A')}")
        logger.info(f"Financial Impact: {analysis.get('financial_impact', 'N/A')}")
        logger.info(f"Detailed Outcome: {analysis.get('detailed_outcome', 'N/A')}")
        
        return True
        
    except Exception as e:
        logger.error(f"AI analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    logger.info("Starting AI Case Analysis Test")
    logger.info("=" * 50)
    
    # Test database connection
    logger.info("1. Testing database connection...")
    case_data, db = test_database_connection()
    if not case_data:
        logger.error("Cannot proceed without database connection")
        return
    
    # Test OpenAI connection
    logger.info("2. Testing OpenAI connection...")
    if not test_openai_connection():
        logger.error("Cannot proceed without OpenAI connection")
        return
    
    # Test AI analysis
    logger.info("3. Testing AI analysis...")
    if test_ai_analysis_with_case(case_data, db):
        logger.info("✅ All tests passed!")
    else:
        logger.error("❌ AI analysis test failed")
    
    # Close database connection
    if db:
        db.close()

if __name__ == "__main__":
    main()
