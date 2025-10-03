#!/usr/bin/env python3
"""
Re-analyze a specific case with fresh AI analysis.
"""

import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine, text
import openai
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def reanalyze_case(case_id):
    """Re-analyze a specific case"""
    try:
        # Setup database connection
        engine = create_engine(settings.database_url)
        
        # Get case details
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, title, decision, judgement, conclusion, case_summary, 
                       area_of_law, protagonist, antagonist
                FROM reported_cases 
                WHERE id = :case_id
            """), {"case_id": case_id}).fetchone()
            
            if not result:
                print(f"❌ Case {case_id} not found")
                return
            
            case = {
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
        
        print(f"🔍 Re-analyzing Case ID: {case_id}")
        print(f"Title: {case['title']}")
        print("=" * 60)
        
        # Prepare case content
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
        
        case_content = "\n\n".join(content_parts)
        
        if not case_content.strip():
            print("❌ No content available for analysis")
            return
        
        print(f"📄 Case Content Length: {len(case_content)} characters")
        print(f"📄 Content Preview:\n{case_content[:500]}...")
        print("=" * 60)
        
        # Setup OpenAI
        with engine.connect() as conn:
            api_key_result = conn.execute(text("SELECT value FROM settings WHERE key = 'openai_api_key' LIMIT 1")).fetchone()
            if not api_key_result:
                print("❌ OpenAI API key not found")
                return
            
            openai_client = openai.OpenAI(api_key=api_key_result[0])
        
        # Truncate content if too long
        if len(case_content) > 6000:
            case_content = case_content[:6000] + "..."
            print("⚠️ Content truncated to fit token limits")
        
        # AI Analysis
        print("🤖 Running AI Analysis...")
        
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
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
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
        print(f"🤖 AI Response:\n{ai_response}")
        print("=" * 60)
        
        # Parse AI response
        try:
            response_text = ai_response.strip()
            
            if response_text.startswith('{') and response_text.endswith('}'):
                analysis = json.loads(response_text)
            else:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                else:
                    raise ValueError("No valid JSON found in response")
            
            print("✅ AI Analysis Parsed Successfully:")
            print(f"   Case Outcome: {analysis.get('case_outcome', 'UNRESOLVED')}")
            print(f"   Financial Impact: {analysis.get('financial_impact', 'UNKNOWN')}")
            print(f"   Court Orders: {analysis.get('court_orders', 'None')[:100]}...")
            print(f"   Detailed Outcome: {analysis.get('detailed_outcome', 'None')[:100]}...")
            
            # Update database
            with engine.connect() as conn:
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
                    "version": "2.0"  # Updated version
                })
                conn.commit()
            
            print("✅ Database updated successfully!")
            
        except Exception as e:
            print(f"❌ Error parsing AI response: {e}")
            print(f"Raw response: {ai_response}")
            
    except Exception as e:
        print(f"❌ Error re-analyzing case: {e}")
        logger.error(f"Error re-analyzing case {case_id}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python reanalyze_case.py <case_id>")
        sys.exit(1)
    
    case_id = int(sys.argv[1])
    reanalyze_case(case_id)
