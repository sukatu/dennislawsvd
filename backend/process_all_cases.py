#!/usr/bin/env python3
"""
Process all cases with AI analysis - simplified version that bypasses model loading issues.
"""

import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import openai
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_analysis_migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleAICaseProcessor:
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.openai_client = None
        self.model = "gpt-3.5-turbo"
        
    def setup_openai(self):
        """Setup OpenAI client"""
        try:
            # Get API key from database
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT value FROM settings WHERE key = 'openai_api_key' LIMIT 1")).fetchone()
                if result:
                    api_key = result[0]
                    self.openai_client = openai.OpenAI(api_key=api_key)
                    logger.info("OpenAI client initialized successfully")
                    return True
                else:
                    logger.error("OpenAI API key not found in database")
                    return False
        except Exception as e:
            logger.error(f"Failed to setup OpenAI: {e}")
            return False
    
    def get_case_count(self):
        """Get total number of cases"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM reported_cases")).scalar()
                return result
        except Exception as e:
            logger.error(f"Error getting case count: {e}")
            return 0
    
    def get_analyzed_count(self):
        """Get number of already analyzed cases"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM reported_cases 
                    WHERE ai_detailed_outcome IS NOT NULL 
                    AND ai_detailed_outcome != ''
                """)).scalar()
                return result
        except Exception as e:
            logger.error(f"Error getting analyzed count: {e}")
            return 0
    
    def get_cases_batch(self, offset, limit):
        """Get a batch of cases"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT id, title, decision, judgement, conclusion, case_summary, 
                           area_of_law, protagonist, antagonist
                    FROM reported_cases 
                    WHERE (decision IS NOT NULL AND decision != '') 
                       OR (judgement IS NOT NULL AND judgement != '')
                    ORDER BY id
                    OFFSET :offset LIMIT :limit
                """), {"offset": offset, "limit": limit})
                
                cases = []
                for row in result:
                    cases.append({
                        'id': row[0],
                        'title': row[1],
                        'decision': row[2],
                        'judgement': row[3],
                        'conclusion': row[4],
                        'case_summary': row[5],
                        'area_of_law': row[6],
                        'protagonist': row[7],
                        'antagonist': row[8]
                    })
                return cases
        except Exception as e:
            logger.error(f"Error getting cases batch: {e}")
            return []
    
    def prepare_case_content(self, case):
        """Prepare case content for AI analysis"""
        content_parts = []
        
        if case['title']:
            content_parts.append(f"Case Title: {case['title']}")
        
        if case['decision']:
            content_parts.append(f"Decision: {case['decision']}")
        elif case['judgement']:
            content_parts.append(f"Judgement: {case['judgement']}")
        
        if case['conclusion']:
            content_parts.append(f"Conclusion: {case['conclusion']}")
        
        if case['case_summary']:
            content_parts.append(f"Case Summary: {case['case_summary']}")
        
        if case['area_of_law']:
            content_parts.append(f"Area of Law: {case['area_of_law']}")
        
        if case['protagonist']:
            content_parts.append(f"Plaintiff/Appellant: {case['protagonist']}")
        if case['antagonist']:
            content_parts.append(f"Defendant/Respondent: {case['antagonist']}")
        
        return "\n\n".join(content_parts)
    
    def analyze_case(self, case):
        """Analyze a single case with AI"""
        try:
            case_content = self.prepare_case_content(case)
            
            if not case_content.strip():
                return self.get_default_analysis()
            
            # Truncate content to fit within token limits
            if len(case_content) > 6000:
                case_content = case_content[:6000] + "..."
            
            prompt = f"""
Analyze the following legal case and provide structured insights for banking and financial assessment purposes:

CASE CONTENT:
{case_content}

Please provide a JSON response with the following structure:

{{
    "case_outcome": "WON|LOST|PARTIALLY_WON|PARTIALLY_LOST|UNRESOLVED",
    "court_orders": "Detailed description of any court orders, judgments, or directives issued",
    "financial_impact": "HIGH|MODERATE|LOW - Brief explanation of financial implications",
    "detailed_outcome": "Comprehensive summary of the case outcome, key findings, and implications for banking/credit assessment"
}}

Guidelines:
1. Determine case outcome based on who prevailed (plaintiff/appellant vs defendant/respondent)
2. Extract specific court orders, monetary awards, injunctions, or other directives
3. Assess financial impact considering monetary damages, costs, and business implications
4. Provide a detailed summary focusing on banking and credit risk assessment
5. Be objective and factual in your analysis
6. If information is unclear, mark as "UNRESOLVED" and explain limitations

Respond only with valid JSON, no additional text.
"""
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a legal AI assistant specializing in case analysis for banking and financial institutions. Analyze legal cases and provide structured insights for credit assessment and risk evaluation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            return self.parse_ai_response(ai_response)
            
        except Exception as e:
            logger.error(f"Error analyzing case {case['id']}: {e}")
            return self.get_default_analysis()
    
    def parse_ai_response(self, ai_response):
        """Parse AI response and extract structured data"""
        try:
            response_text = ai_response.strip()
            
            if response_text.startswith('{') and response_text.endswith('}'):
                return json.loads(response_text)
            else:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    raise ValueError("No valid JSON found in response")
                    
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return self.get_default_analysis()
    
    def get_default_analysis(self):
        """Return default analysis when AI processing fails"""
        return {
            "case_outcome": "UNRESOLVED",
            "court_orders": "Unable to determine court orders from available information.",
            "financial_impact": "UNKNOWN - Unable to assess financial impact due to insufficient information.",
            "detailed_outcome": "Case analysis could not be completed due to insufficient information or processing error."
        }
    
    def update_case_with_analysis(self, case_id, analysis):
        """Update case with AI analysis"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    UPDATE reported_cases 
                    SET ai_case_outcome = :case_outcome,
                        ai_court_orders = :court_orders,
                        ai_financial_impact = :financial_impact,
                        ai_detailed_outcome = :detailed_outcome,
                        ai_summary_generated_at = :generated_at,
                        ai_summary_version = :version
                    WHERE id = :case_id
                """), {
                    "case_id": case_id,
                    "case_outcome": analysis.get('case_outcome', 'UNRESOLVED'),
                    "court_orders": analysis.get('court_orders', ''),
                    "financial_impact": analysis.get('financial_impact', 'UNKNOWN'),
                    "detailed_outcome": analysis.get('detailed_outcome', ''),
                    "generated_at": datetime.utcnow(),
                    "version": "1.0"
                })
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating case {case_id}: {e}")
            return False
    
    def process_all_cases(self, batch_size=5):
        """Process all cases in batches"""
        try:
            total_cases = self.get_case_count()
            analyzed_cases = self.get_analyzed_count()
            pending_cases = total_cases - analyzed_cases
            
            logger.info(f"Total cases: {total_cases}")
            logger.info(f"Already analyzed: {analyzed_cases}")
            logger.info(f"Pending analysis: {pending_cases}")
            
            if pending_cases == 0:
                logger.info("All cases have already been analyzed!")
                return
            
            processed = 0
            successful = 0
            failed = 0
            
            # Process cases in batches
            offset = analyzed_cases  # Start from where we left off
            while offset < total_cases:
                cases = self.get_cases_batch(offset, batch_size)
                if not cases:
                    break
                
                for case in cases:
                    try:
                        logger.info(f"Processing case {case['id']}: {case['title'][:50]}...")
                        analysis = self.analyze_case(case)
                        
                        if self.update_case_with_analysis(case['id'], analysis):
                            successful += 1
                            logger.info(f"✅ Case {case['id']} analyzed successfully")
                        else:
                            failed += 1
                            logger.error(f"❌ Failed to update case {case['id']}")
                        
                        processed += 1
                        
                        # Log progress every 10 cases
                        if processed % 10 == 0:
                            logger.info(f"Progress: {processed}/{pending_cases} cases processed")
                            
                    except Exception as e:
                        logger.error(f"Error processing case {case['id']}: {e}")
                        failed += 1
                        processed += 1
                
                offset += batch_size
            
            result = {
                "total_cases": total_cases,
                "processed": processed,
                "successful": successful,
                "failed": failed,
                "completion_percentage": (processed / pending_cases * 100) if pending_cases > 0 else 100
            }
            
            logger.info("=" * 50)
            logger.info("AI Analysis Processing Completed")
            logger.info(f"Total cases: {result['total_cases']}")
            logger.info(f"Processed: {result['processed']}")
            logger.info(f"Successful: {result['successful']}")
            logger.info(f"Failed: {result['failed']}")
            logger.info(f"Completion: {result['completion_percentage']:.2f}%")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing all cases: {e}")
            return None

def main():
    """Main function"""
    logger.info("Starting AI Case Analysis Processing")
    logger.info("=" * 50)
    
    processor = SimpleAICaseProcessor()
    
    # Setup OpenAI
    if not processor.setup_openai():
        logger.error("Cannot proceed without OpenAI setup")
        return
    
    # Process all cases
    result = processor.process_all_cases(batch_size=3)  # Small batch size for stability
    
    if result:
        logger.info("✅ Processing completed successfully!")
    else:
        logger.error("❌ Processing failed")

if __name__ == "__main__":
    main()
