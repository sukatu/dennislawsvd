import os
import openai
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from models.settings import Settings
from models.reported_cases import ReportedCases
from models.case_metadata import CaseMetadata
from models.case_hearings import CaseHearing
from datetime import datetime
import json
import re

class AIChatService:
    def __init__(self, db: Session):
        self.db = db
        self.openai_client = self._get_openai_client()
        self.model = self._get_ai_model()
        
    def _get_openai_client(self):
        """Get OpenAI client with API key from database or environment"""
        try:
            setting = self.db.query(Settings).filter(Settings.key == "openai_api_key").first()
            if setting and setting.value:
                return openai.OpenAI(api_key=setting.value)
        except Exception as e:
            print(f"Error fetching API key from database: {e}")
        
        # Fallback to environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in database or environment variables")
        return openai.OpenAI(api_key=api_key)
    
    def _get_ai_model(self) -> str:
        """Get AI model from settings"""
        try:
            setting = self.db.query(Settings).filter(Settings.key == "ai_model").first()
            return setting.value if setting and setting.value else "gpt-3.5-turbo"
        except Exception as e:
            print(f"Error fetching AI model from database: {e}")
            return "gpt-3.5-turbo"
    
    def _truncate_content(self, content: str, max_length: int = 2000) -> str:
        """Truncate content to prevent token limit issues"""
        if not content or len(content) <= max_length:
            return content
        return content[:max_length] + "... [Content truncated]"
    
    def get_case_context(self, case_id: int) -> Dict[str, Any]:
        """Get comprehensive case context for AI chat"""
        try:
            # Get case with metadata
            case = self.db.query(ReportedCases).outerjoin(
                CaseMetadata, ReportedCases.id == CaseMetadata.case_id
            ).filter(ReportedCases.id == case_id).first()
            
            if not case:
                return {"error": "Case not found"}
            
            metadata = case.case_metadata
            
            # Get case hearings
            hearings = self.db.query(CaseHearing).filter(
                CaseHearing.case_id == case_id
            ).order_by(CaseHearing.hearing_date).all()
            
            # Build comprehensive context
            context = {
                "case_id": case.id,
                "title": case.title,
                "suit_reference_number": case.suit_reference_number,
                "date": case.date.isoformat() if case.date else None,
                "year": case.year,
                "court_type": case.court_type,
                "court_division": case.court_division,
                "area_of_law": case.area_of_law,
                "status": str(case.status) if case.status is not None else None,
                "protagonist": case.protagonist,
                "antagonist": case.antagonist,
                "lawyers": case.lawyers,
                "region": case.region,
                "town": case.town,
                "presiding_judge": case.presiding_judge,
                "judgement_by": case.judgement_by,
                "opinion_by": case.opinion_by,
                
                # Case content (truncated to prevent token limit issues)
                "case_summary": self._truncate_content(case.case_summary, 1000),
                "detail_content": self._truncate_content(case.detail_content, 2000),
                "decision": self._truncate_content(case.decision, 1500),
                "judgement": self._truncate_content(case.judgement, 1500),
                "commentary": self._truncate_content(case.commentary, 1000),
                "headnotes": self._truncate_content(case.headnotes, 1000),
                "keywords_phrases": self._truncate_content(case.keywords_phrases, 500),
                
                # Hearings
                "hearings": [
                    {
                        "hearing_date": hearing.hearing_date.isoformat() if hearing.hearing_date else None,
                        "hearing_time": hearing.hearing_time,
                        "coram": hearing.coram,
                        "remark": hearing.remark.value if hearing.remark else None,
                        "proceedings": hearing.proceedings
                    }
                    for hearing in hearings
                ],
                
                # Metadata (truncated to prevent token limit issues)
                "metadata": {
                    "case_type": metadata.case_type if metadata else None,
                    "keywords": self._truncate_content(metadata.keywords, 500) if metadata else None,
                    "judges": self._truncate_content(metadata.judges, 500) if metadata else None,
                    "lawyers": self._truncate_content(metadata.lawyers, 500) if metadata else None,
                    "related_people": self._truncate_content(metadata.related_people, 500) if metadata else None,
                    "organizations": self._truncate_content(metadata.organizations, 500) if metadata else None,
                    "banks_involved": self._truncate_content(metadata.banks_involved, 500) if metadata else None,
                    "insurance_involved": self._truncate_content(metadata.insurance_involved, 500) if metadata else None,
                    "resolution_status": metadata.resolution_status if metadata else None,
                    "outcome": metadata.outcome if metadata else None,
                    "decision_type": metadata.decision_type if metadata else None,
                    "monetary_amount": metadata.monetary_amount if metadata else None,
                    "statutes_cited": self._truncate_content(metadata.statutes_cited, 500) if metadata else None,
                    "cases_cited": self._truncate_content(metadata.cases_cited, 500) if metadata else None,
                    "relevance_score": metadata.relevance_score if metadata else None
                } if metadata else {}
            }
            
            return context
            
        except Exception as e:
            print(f"Error getting case context: {e}")
            return {"error": f"Failed to get case context: {str(e)}"}
    
    def generate_ai_response(self, case_id: int, user_message: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate AI response based on case context and user message"""
        try:
            # Get case context
            case_context = self.get_case_context(case_id)
            if "error" in case_context:
                return case_context
            
            # Build system prompt
            system_prompt = self._build_system_prompt(case_context)
            
            # Build messages for OpenAI
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add chat history if provided
            if chat_history:
                for msg in chat_history[-10:]:  # Limit to last 10 messages
                    messages.append({
                        "role": "user" if msg["role"] == "user" else "assistant",
                        "content": msg["content"]
                    })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=800,
                temperature=0.7,
                stream=False
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": ai_response,
                "case_context": case_context,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return {
                "success": False,
                "error": f"Failed to generate AI response: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _build_system_prompt(self, case_context: Dict[str, Any]) -> str:
        """Build comprehensive system prompt for AI chat"""
        return f"""You are an expert legal AI assistant specializing in Ghanaian law and financial legal matters. You are analyzing the following case and providing expert legal and financial insights.

CASE INFORMATION:
Title: {case_context.get('title', 'N/A')}
Case Number: {case_context.get('suit_reference_number', 'N/A')}
Date: {case_context.get('date', 'N/A')}
Court: {case_context.get('court_type', 'N/A')} - {case_context.get('court_division', 'N/A')}
Area of Law: {case_context.get('area_of_law', 'N/A')}
Status: {case_context.get('status', 'N/A')}

PARTIES:
Protagonist: {case_context.get('protagonist', 'N/A')}
Antagonist: {case_context.get('antagonist', 'N/A')}
Lawyers: {case_context.get('lawyers', 'N/A')}
Presiding Judge: {case_context.get('presiding_judge', 'N/A')}

CASE CONTENT:
Summary: {case_context.get('case_summary', 'N/A')}
Decision: {case_context.get('decision', 'N/A')}
Judgement: {case_context.get('judgement', 'N/A')}
Commentary: {case_context.get('commentary', 'N/A')}
Headnotes: {case_context.get('headnotes', 'N/A')}

FINANCIAL/LEGAL METADATA:
Monetary Amount: {case_context.get('metadata', {}).get('monetary_amount', 'N/A')}
Resolution Status: {case_context.get('metadata', {}).get('resolution_status', 'N/A')}
Outcome: {case_context.get('metadata', {}).get('outcome', 'N/A')}
Decision Type: {case_context.get('metadata', {}).get('decision_type', 'N/A')}
Banks Involved: {case_context.get('metadata', {}).get('banks_involved', 'N/A')}
Insurance Involved: {case_context.get('metadata', {}).get('insurance_involved', 'N/A')}

HEARINGS:
{self._format_hearings(case_context.get('hearings', []))}

Your role is to:
1. Provide expert legal analysis of the case
2. Explain financial implications and risks
3. Suggest legal strategies and precedents
4. Answer questions about case law and legal principles
5. Provide insights on potential outcomes and next steps
6. Explain complex legal concepts in simple terms
7. Identify key legal and financial risks
8. Suggest relevant statutes and regulations

Always base your responses on the specific case details provided and Ghanaian law. Be thorough, accurate, and professional in your analysis."""
    
    def _format_hearings(self, hearings: List[Dict]) -> str:
        """Format hearings for system prompt"""
        if not hearings:
            return "No hearings recorded"
        
        formatted = []
        for hearing in hearings:
            formatted.append(f"- Date: {hearing.get('hearing_date', 'N/A')}, Time: {hearing.get('hearing_time', 'N/A')}, Coram: {hearing.get('coram', 'N/A')}, Remark: {hearing.get('remark', 'N/A')}")
        
        return "\n".join(formatted)
    
    def generate_case_summary(self, case_id: int) -> Dict[str, Any]:
        """Generate a comprehensive case summary for quick reference"""
        try:
            case_context = self.get_case_context(case_id)
            if "error" in case_context:
                return case_context
            
            system_prompt = f"""You are a legal expert. Provide a comprehensive summary of this case in 3-4 paragraphs covering:
1. Case overview and key facts
2. Legal issues and arguments
3. Financial implications and risks
4. Potential outcomes and recommendations

Case: {case_context.get('title', 'N/A')}
Parties: {case_context.get('protagonist', 'N/A')} vs {case_context.get('antagonist', 'N/A')}
Area of Law: {case_context.get('area_of_law', 'N/A')}
Court: {case_context.get('court_type', 'N/A')}"""
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please provide a comprehensive summary of this case: {case_context.get('case_summary', 'N/A')}"}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return {
                "success": True,
                "summary": response.choices[0].message.content,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating case summary: {e}")
            return {
                "success": False,
                "error": f"Failed to generate case summary: {str(e)}"
            }

