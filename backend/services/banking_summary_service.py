"""
Service for generating and saving AI-powered banking summaries for cases.
"""

import os
import re
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from models.reported_cases import ReportedCases

class BankingSummaryService:
    def __init__(self, db: Session):
        self.db = db

    def generate_banking_summary(self, case: ReportedCases) -> Dict[str, Any]:
        """
        Generate comprehensive AI-based banking summary for a case.
        """
        case_text = case.decision or case.judgement or case.conclusion or ''
        title = case.title or ''
        full_text = (case_text + ' ' + title + ' ' + (case.case_summary or '')).lower()
        
        # Enhanced outcome analysis
        won_lost = self._analyze_case_outcome(full_text)
        court_orders = self._analyze_court_orders(full_text)
        financial_impact = self._analyze_financial_impact(full_text)
        detailed_outcome = self._generate_detailed_outcome(full_text, won_lost, court_orders, financial_impact)
        
        return {
            'ai_case_outcome': won_lost,
            'ai_court_orders': court_orders,
            'ai_financial_impact': financial_impact,
            'ai_detailed_outcome': detailed_outcome,
            'ai_summary_generated_at': datetime.now(),
            'ai_summary_version': '1.0'
        }

    def _analyze_case_outcome(self, text: str) -> str:
        """Analyze case outcome based on keywords."""
        strong_win_keywords = [
            'allowed', 'granted', 'upheld', 'successful', 'won', 'favorable', 
            'in favor', 'succeeded', 'victory', 'prevailed'
        ]
        moderate_win_keywords = [
            'partially allowed', 'partially granted', 'in part', 'some relief'
        ]
        strong_loss_keywords = [
            'dismissed', 'rejected', 'denied', 'unsuccessful', 'lost', 
            'unfavorable', 'against', 'failed', 'defeated', 'overruled'
        ]
        moderate_loss_keywords = [
            'partially dismissed', 'partially rejected', 'in part dismissed'
        ]
        
        if any(keyword in text for keyword in strong_win_keywords):
            return 'WON'
        elif any(keyword in text for keyword in moderate_win_keywords):
            return 'PARTIALLY_WON'
        elif any(keyword in text for keyword in strong_loss_keywords):
            return 'LOST'
        elif any(keyword in text for keyword in moderate_loss_keywords):
            return 'PARTIALLY_LOST'
        else:
            return 'UNRESOLVED'

    def _analyze_court_orders(self, text: str) -> str:
        """Analyze court orders based on keywords."""
        order_keywords = [
            'ordered', 'directed', 'injunction', 'restraining', 'mandatory', 'prohibitory',
            'enjoined', 'restrained', 'compelled', 'required', 'commanded', 'decreed',
            'permanent injunction', 'temporary injunction', 'interim order', 'final order'
        ]
        
        specific_order_keywords = [
            'pay', 'compensate', 'refund', 'return', 'restore', 'cease', 'desist',
            'remove', 'demolish', 'construct', 'repair', 'maintain', 'provide'
        ]
        
        if any(keyword in text for keyword in order_keywords):
            has_specific_orders = any(keyword in text for keyword in specific_order_keywords)
            return 'Court issued specific actionable orders requiring compliance' if has_specific_orders else 'Court issued general orders or directives'
        else:
            return 'No specific court orders identified'

    def _analyze_financial_impact(self, text: str) -> str:
        """Analyze financial impact based on keywords."""
        monetary_keywords = [
            'damages', 'compensation', 'fine', 'penalty', 'costs', 'award', 'settlement',
            'restitution', 'reimbursement', 'refund', 'payment', 'monetary', 'financial',
            'ghc', 'cedis', 'dollars', 'amount', 'sum', 'value', 'price'
        ]
        
        high_value_keywords = ['million', 'thousand', 'substantial', 'significant', 'large']
        low_value_keywords = ['nominal', 'minimal', 'small', 'token']
        
        if any(keyword in text for keyword in monetary_keywords):
            if any(keyword in text for keyword in high_value_keywords):
                return 'HIGH - Case involves substantial monetary amounts or significant financial implications'
            elif any(keyword in text for keyword in low_value_keywords):
                return 'LOW - Case involves minimal monetary amounts or token financial implications'
            else:
                return 'MODERATE - Case involves monetary amounts with moderate financial implications'
        else:
            return 'NONE - No clear monetary amounts or financial implications identified'

    def _generate_detailed_outcome(self, text: str, won_lost: str, court_orders: str, financial_impact: str) -> str:
        """Generate detailed outcome analysis."""
        outcome_keywords = [
            'judgment', 'ruling', 'decision', 'verdict', 'finding', 'conclusion',
            'determination', 'resolution', 'settlement', 'agreement'
        ]
        
        if any(keyword in text for keyword in outcome_keywords):
            detailed_outcome = f"Case {won_lost.lower().replace('_', ' ')} with {court_orders.lower()}. {financial_impact}. "
            
            # Add specific details based on case content
            if 'contract' in text:
                detailed_outcome += 'Contract-related dispute with legal implications for business relationships.'
            elif 'property' in text or 'land' in text:
                detailed_outcome += 'Property/land dispute with potential asset implications.'
            elif 'employment' in text or 'labor' in text:
                detailed_outcome += 'Employment-related matter with workplace implications.'
            elif 'criminal' in text or 'fraud' in text:
                detailed_outcome += 'Criminal or fraud-related matter with serious legal implications.'
            else:
                detailed_outcome += 'General legal matter with standard legal implications.'
        else:
            detailed_outcome = 'Case outcome details not clearly specified in available information.'
        
        return detailed_outcome

    def save_banking_summary(self, case_id: int, summary_data: Dict[str, Any]) -> bool:
        """Save banking summary to database."""
        try:
            case = self.db.query(ReportedCases).filter(ReportedCases.id == case_id).first()
            if not case:
                return False
            
            # Update case with AI summary data
            case.ai_case_outcome = summary_data['ai_case_outcome']
            case.ai_court_orders = summary_data['ai_court_orders']
            case.ai_financial_impact = summary_data['ai_financial_impact']
            case.ai_detailed_outcome = summary_data['ai_detailed_outcome']
            case.ai_summary_generated_at = summary_data['ai_summary_generated_at']
            case.ai_summary_version = summary_data['ai_summary_version']
            
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error saving banking summary: {e}")
            self.db.rollback()
            return False

    def get_banking_summary(self, case_id: int) -> Optional[Dict[str, Any]]:
        """Get existing banking summary from database."""
        try:
            case = self.db.query(ReportedCases).filter(ReportedCases.id == case_id).first()
            if not case or not case.ai_summary_generated_at:
                return None
            
            return {
                'ai_case_outcome': case.ai_case_outcome,
                'ai_court_orders': case.ai_court_orders,
                'ai_financial_impact': case.ai_financial_impact,
                'ai_detailed_outcome': case.ai_detailed_outcome,
                'ai_summary_generated_at': case.ai_summary_generated_at,
                'ai_summary_version': case.ai_summary_version
            }
        except Exception as e:
            print(f"Error getting banking summary: {e}")
            return None
