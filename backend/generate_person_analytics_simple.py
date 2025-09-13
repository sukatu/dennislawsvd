#!/usr/bin/env python3
"""
Simple script to generate person analytics using direct database queries
"""

import os
import sys
import asyncio
import mysql.connector
from mysql.connector import Error
from decimal import Decimal
import re
import json

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from config import settings

DATABASE_CONFIG = {
    'host': settings.mysql_host,
    'port': settings.mysql_port,
    'user': settings.mysql_user,
    'password': settings.mysql_password,
    'database': settings.mysql_database
}

class SimplePersonAnalyticsService:
    def __init__(self):
        self.risk_keywords = {
            'criminal': {'weight': 10, 'keywords': ['criminal', 'fraud', 'theft', 'murder', 'assault', 'robbery', 'drug', 'money laundering']},
            'financial': {'weight': 8, 'keywords': ['fraud', 'embezzlement', 'money laundering', 'tax evasion', 'financial crime']},
            'violence': {'weight': 9, 'keywords': ['assault', 'battery', 'domestic violence', 'murder', 'manslaughter', 'violence']},
            'corruption': {'weight': 7, 'keywords': ['corruption', 'bribery', 'kickback', 'misappropriation', 'abuse of office']},
            'business_dispute': {'weight': 3, 'keywords': ['contract', 'breach', 'business', 'commercial', 'partnership']},
            'family': {'weight': 2, 'keywords': ['divorce', 'custody', 'alimony', 'family', 'domestic']},
            'property': {'weight': 4, 'keywords': ['property', 'land', 'real estate', 'boundary', 'ownership']}
        }
        
        self.subject_categories = {
            'Contract Dispute': ['contract', 'agreement', 'breach', 'specific performance', 'damages'],
            'Property Dispute': ['land', 'property', 'title', 'ownership', 'boundary', 'lease'],
            'Fraud': ['fraud', 'deception', 'misrepresentation', 'embezzlement', 'forgery'],
            'Family Law': ['divorce', 'marriage', 'child custody', 'alimony', 'adoption'],
            'Criminal': ['murder', 'theft', 'assault', 'robbery', 'homicide', 'manslaughter'],
            'Commercial': ['company', 'corporate', 'business', 'merger', 'acquisition', 'shareholder'],
            'Employment': ['employment', 'dismissal', 'termination', 'harassment', 'discrimination'],
            'Tort': ['negligence', 'defamation', 'slander', 'libel', 'personal injury'],
            'Constitutional': ['constitution', 'human rights', 'fundamental rights', 'election'],
            'Administrative': ['administrative', 'public body', 'government', 'permit', 'license']
        }

    def get_connection(self):
        return mysql.connector.connect(**DATABASE_CONFIG)

    def calculate_risk_score(self, cases):
        """Calculate risk score based on case analysis"""
        if not cases:
            return 0, "Low", []
        
        total_score = 0
        risk_factors = []
        
        for case in cases:
            case_text = self.get_case_text(case)
            case_score = 0
            case_risk_factors = []
            
            # Analyze case text for risk indicators
            for category, data in self.risk_keywords.items():
                weight = data['weight']
                keywords = data['keywords']
                
                for keyword in keywords:
                    if keyword.lower() in case_text.lower():
                        case_score += weight
                        case_risk_factors.append(f"{category}: {keyword}")
            
            # Additional factors
            if case.get('area_of_law') and 'criminal' in str(case.get('area_of_law')).lower():
                case_score += 5
                case_risk_factors.append("criminal case type")
            
            if case.get('status') and 'convicted' in str(case.get('status')).lower():
                case_score += 10
                case_risk_factors.append("conviction")
            
            total_score += case_score
            risk_factors.extend(case_risk_factors)
        
        # Normalize score to 0-100
        max_possible_score = len(cases) * 50
        normalized_score = min(int((total_score / max_possible_score) * 100), 100)
        
        # Determine risk level
        if normalized_score >= 80:
            risk_level = "Critical"
        elif normalized_score >= 60:
            risk_level = "High"
        elif normalized_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return normalized_score, risk_level, list(set(risk_factors))

    def calculate_financial_impact(self, cases):
        """Calculate financial impact metrics"""
        monetary_amounts = []
        
        for case in cases:
            case_text = self.get_case_text(case)
            amounts = self.extract_monetary_amounts(case_text)
            monetary_amounts.extend(amounts)
        
        if not monetary_amounts:
            return Decimal('0.00'), Decimal('0.00'), "Low"
        
        total_amount = sum(monetary_amounts)
        average_amount = total_amount / len(monetary_amounts)
        
        # Determine financial risk level
        if total_amount >= 1000000:
            financial_risk_level = "Critical"
        elif total_amount >= 500000:
            financial_risk_level = "High"
        elif total_amount >= 100000:
            financial_risk_level = "Medium"
        else:
            financial_risk_level = "Low"
        
        return total_amount, average_amount, financial_risk_level

    def analyze_subject_matter(self, cases):
        """Analyze subject matter and legal issues"""
        if not cases:
            return "N/A", [], [], []
        
        all_text = " ".join([self.get_case_text(case) for case in cases])
        
        # Analyze subject matter categories
        category_scores = {}
        for category, keywords in self.subject_categories.items():
            score = sum(1 for keyword in keywords if keyword.lower() in all_text.lower())
            if score > 0:
                category_scores[category] = score
        
        primary_subject = max(category_scores.items(), key=lambda x: x[1])[0] if category_scores else "Other"
        subject_categories = list(category_scores.keys())
        
        # Extract legal issues and financial terms
        legal_issues = self.extract_legal_issues(all_text)
        financial_terms = self.extract_financial_terms(all_text)
        
        return primary_subject, subject_categories, legal_issues, financial_terms

    def calculate_success_rate(self, cases):
        """Calculate success rate based on case outcomes"""
        if not cases:
            return Decimal('0.00')
        
        resolved_cases = [case for case in cases if case.get('status') and 'resolved' in str(case.get('status')).lower()]
        if not resolved_cases:
            return Decimal('0.00')
        
        favorable_outcomes = 0
        for case in resolved_cases:
            case_text = self.get_case_text(case)
            if any(word in case_text.lower() for word in ['dismissed', 'acquitted', 'favorable', 'won', 'successful']):
                favorable_outcomes += 1
        
        success_rate = (favorable_outcomes / len(resolved_cases)) * 100
        return Decimal(str(round(success_rate, 2)))

    def get_case_text(self, case):
        """Extract all relevant text from a case"""
        text_parts = []
        if case.get('title'):
            text_parts.append(str(case['title']))
        if case.get('case_summary'):
            text_parts.append(str(case['case_summary']))
        if case.get('decision'):
            text_parts.append(str(case['decision']))
        if case.get('judgement'):
            text_parts.append(str(case['judgement']))
        if case.get('conclusion'):
            text_parts.append(str(case['conclusion']))
        if case.get('keywords_phrases'):
            text_parts.append(str(case['keywords_phrases']))
        if case.get('area_of_law'):
            text_parts.append(str(case['area_of_law']))
        
        return " ".join(text_parts)

    def extract_monetary_amounts(self, text):
        """Extract monetary amounts from text"""
        amounts = []
        patterns = [
            r'\$[\d,]+(?:\.\d{2})?',
            r'GHS\s*[\d,]+(?:\.\d{2})?',
            r'GH₵\s*[\d,]+(?:\.\d{2})?',
            r'[\d,]+(?:\.\d{2})?\s*(?:dollars?|cedis?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                clean_amount = re.sub(r'[^\d.,]', '', match)
                if clean_amount:
                    try:
                        amount = Decimal(clean_amount.replace(',', ''))
                        amounts.append(amount)
                    except:
                        continue
        
        return amounts

    def extract_legal_issues(self, text):
        """Extract legal issues from text"""
        legal_issues = []
        issue_keywords = [
            'constitutional', 'human rights', 'due process', 'equal protection',
            'contract breach', 'negligence', 'fraud', 'misrepresentation',
            'employment law', 'discrimination', 'harassment', 'wrongful termination',
            'property rights', 'intellectual property', 'patent', 'copyright',
            'criminal law', 'evidence', 'procedure', 'jurisdiction'
        ]
        
        for keyword in issue_keywords:
            if keyword.lower() in text.lower():
                legal_issues.append(keyword.title())
        
        return list(set(legal_issues))

    def extract_financial_terms(self, text):
        """Extract financial terms from text"""
        financial_terms = []
        term_keywords = [
            'interest rate', 'compound interest', 'penalty', 'fine',
            'damages', 'compensation', 'restitution', 'remedy',
            'injunction', 'specific performance', 'liquidated damages',
            'breach of contract', 'unjust enrichment', 'quantum meruit'
        ]
        
        for keyword in term_keywords:
            if keyword.lower() in text.lower():
                financial_terms.append(keyword.title())
        
        return list(set(financial_terms))

    def generate_analytics_for_person(self, person_id, person_name):
        """Generate comprehensive analytics for a person"""
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            # Get related cases
            cursor.execute("""
                SELECT id, title, case_summary, decision, judgement, conclusion, 
                       keywords_phrases, area_of_law, status, type
                FROM reported_cases 
                WHERE title LIKE %s OR case_summary LIKE %s OR decision LIKE %s
            """, (f'%{person_name}%', f'%{person_name}%', f'%{person_name}%'))
            
            cases = cursor.fetchall()
            
            if not cases:
                # Create minimal analytics for person with no cases
                analytics = {
                    'person_id': person_id,
                    'risk_score': 0,
                    'risk_level': 'Low',
                    'risk_factors': [],
                    'total_monetary_amount': Decimal('0.00'),
                    'average_case_value': Decimal('0.00'),
                    'financial_risk_level': 'Low',
                    'primary_subject_matter': 'N/A',
                    'subject_matter_categories': [],
                    'legal_issues': [],
                    'financial_terms': [],
                    'case_complexity_score': 0,
                    'success_rate': Decimal('0.00')
                }
            else:
                # Calculate all analytics
                risk_score, risk_level, risk_factors = self.calculate_risk_score(cases)
                total_amount, avg_amount, financial_risk = self.calculate_financial_impact(cases)
                primary_subject, subject_categories, legal_issues, financial_terms = self.analyze_subject_matter(cases)
                success_rate = self.calculate_success_rate(cases)
                
                analytics = {
                    'person_id': person_id,
                    'risk_score': risk_score,
                    'risk_level': risk_level,
                    'risk_factors': risk_factors,
                    'total_monetary_amount': total_amount,
                    'average_case_value': avg_amount,
                    'financial_risk_level': financial_risk,
                    'primary_subject_matter': primary_subject,
                    'subject_matter_categories': subject_categories,
                    'legal_issues': legal_issues,
                    'financial_terms': financial_terms,
                    'case_complexity_score': min(len(cases) * 2, 100),
                    'success_rate': success_rate
                }
            
            # Save or update analytics
            cursor.execute("""
                INSERT INTO person_analytics 
                (person_id, risk_score, risk_level, risk_factors, total_monetary_amount, 
                 average_case_value, financial_risk_level, primary_subject_matter, 
                 subject_matter_categories, legal_issues, financial_terms, 
                 case_complexity_score, success_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                risk_score = VALUES(risk_score),
                risk_level = VALUES(risk_level),
                risk_factors = VALUES(risk_factors),
                total_monetary_amount = VALUES(total_monetary_amount),
                average_case_value = VALUES(average_case_value),
                financial_risk_level = VALUES(financial_risk_level),
                primary_subject_matter = VALUES(primary_subject_matter),
                subject_matter_categories = VALUES(subject_matter_categories),
                legal_issues = VALUES(legal_issues),
                financial_terms = VALUES(financial_terms),
                case_complexity_score = VALUES(case_complexity_score),
                success_rate = VALUES(success_rate)
            """, (
                analytics['person_id'],
                analytics['risk_score'],
                analytics['risk_level'],
                json.dumps(analytics['risk_factors']),
                analytics['total_monetary_amount'],
                analytics['average_case_value'],
                analytics['financial_risk_level'],
                analytics['primary_subject_matter'],
                json.dumps(analytics['subject_matter_categories']),
                json.dumps(analytics['legal_issues']),
                json.dumps(analytics['financial_terms']),
                analytics['case_complexity_score'],
                analytics['success_rate']
            ))
            
            connection.commit()
            return analytics
            
        except Error as e:
            print(f"Error generating analytics for person {person_id}: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

async def generate_analytics_for_all_persons():
    """Generate analytics for all persons in the database"""
    print("🚀 Starting person analytics generation...")
    
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Get all persons
        cursor.execute("SELECT id, full_name FROM people LIMIT 10")  # Start with first 10 for testing
        persons = cursor.fetchall()
        total_persons = len(persons)
        print(f"📊 Found {total_persons} persons to process")
        
        if total_persons == 0:
            print("✅ No persons found. Exiting.")
            return
        
        # Initialize analytics service
        analytics_service = SimplePersonAnalyticsService()
        
        processed_count = 0
        success_count = 0
        error_count = 0
        
        for person in persons:
            processed_count += 1
            print(f"\n🔍 Processing person {processed_count}/{total_persons}: {person['full_name']} (ID: {person['id']})...")
            
            try:
                analytics = analytics_service.generate_analytics_for_person(person['id'], person['full_name'])
                if analytics:
                    success_count += 1
                    print(f"   ✅ Analytics generated - Risk: {analytics['risk_level']} ({analytics['risk_score']}%), Financial: {analytics['financial_risk_level']}")
                else:
                    error_count += 1
                    print(f"   ❌ Failed to generate analytics")
            except Exception as e:
                error_count += 1
                print(f"   ❌ Error: {str(e)}")
            
            # Progress update every 5 persons
            if processed_count % 5 == 0:
                print(f"\n📈 Progress: {processed_count}/{total_persons} - ✅ {success_count} successful, ❌ {error_count} failed")
        
        print(f"\n🎉 Person analytics generation complete!")
        print(f"📊 Final stats:")
        print(f"   Total processed: {processed_count}")
        print(f"   Successful: {success_count}")
        print(f"   Failed: {error_count}")
        print(f"   Success rate: {(success_count/processed_count)*100:.1f}%")
        
    except Error as e:
        print(f"❌ Error during analytics generation: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    asyncio.run(generate_analytics_for_all_persons())
