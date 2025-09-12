#!/usr/bin/env python3
"""
Script to populate case_hearings table with sample data for ALL cases
"""

from sqlalchemy import create_engine, text
from config import settings
from datetime import datetime, timedelta
import random

def get_all_cases():
    """Get all case IDs from the database"""
    engine = create_engine(settings.database_url)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id FROM reported_cases ORDER BY id"))
        case_ids = [row[0] for row in result.fetchall()]
        return case_ids

def create_hearings_for_all_cases():
    """Create hearings for all cases in the database"""
    engine = create_engine(settings.database_url)
    
    # Get all case IDs
    case_ids = get_all_cases()
    print(f"Found {len(case_ids)} cases to process")
    
    if not case_ids:
        print("No cases found in database")
        return
    
    # Sample hearing templates
    hearing_templates = [
        {
            "time": "9:00 AM",
            "coram": "Justice John Doe",
            "remark": "fh",
            "proceedings": "Case called for hearing. Plaintiff's counsel presented opening arguments. Defendant's counsel requested adjournment for further preparation. Case adjourned to next available date."
        },
        {
            "time": "10:30 AM", 
            "coram": "Justice Jane Smith, Justice Michael Brown",
            "remark": "fh",
            "proceedings": "Preliminary hearing conducted. Both parties confirmed readiness. Discovery timeline established. Case set down for full hearing."
        },
        {
            "time": "2:00 PM",
            "coram": "Justice Sarah Wilson, Justice David Johnson",
            "remark": "fr",
            "proceedings": "Court delivered ruling on preliminary objections. Objections overruled. Case to proceed to full hearing. Parties directed to file witness statements within 14 days."
        },
        {
            "time": "11:00 AM",
            "coram": "Justice Robert Taylor",
            "remark": "fr",
            "proceedings": "Ruling on admissibility of evidence. Expert witness testimony admitted. Documentary evidence marked as exhibits. Case set down for final hearing."
        },
        {
            "time": "3:30 PM",
            "coram": "Justice Mary Davis, Justice Lisa Anderson",
            "remark": "fj",
            "proceedings": "Final judgment delivered. Court found in favor of plaintiff. Defendant ordered to pay damages of $50,000 plus costs. Judgment to be executed within 30 days."
        },
        {
            "time": "10:15 AM",
            "coram": "Justice Michael Brown, Justice Sarah Wilson",
            "remark": "fj",
            "proceedings": "Judgment delivered. Court dismissed the action. Plaintiff's claim found to be without merit. Costs awarded to defendant."
        },
        {
            "time": "9:30 AM",
            "coram": "Justice John Doe, Justice Jane Smith",
            "remark": "fh",
            "proceedings": "Interim application heard. Plaintiff's application for interim injunction granted. Defendant restrained from disposing of property pending final determination of case."
        },
        {
            "time": "1:45 PM",
            "coram": "Justice David Johnson",
            "remark": "fr",
            "proceedings": "Ruling on summary judgment application. Application granted in part. Some claims dismissed, others to proceed to trial."
        },
        {
            "time": "11:30 AM",
            "coram": "Justice Robert Taylor, Justice Lisa Anderson",
            "remark": "fj",
            "proceedings": "Final judgment. Court awarded damages of $25,000 to plaintiff. Interest at 10% per annum from date of breach."
        },
        {
            "time": "2:15 PM",
            "coram": "Justice Mary Davis",
            "remark": "fh",
            "proceedings": "Case management conference. Parties agreed on discovery timeline. Trial date fixed for next term."
        },
        {
            "time": "10:45 AM",
            "coram": "Justice Sarah Wilson, Justice Michael Brown",
            "remark": "fr",
            "proceedings": "Ruling on jurisdiction. Court found it has jurisdiction. Case to proceed."
        },
        {
            "time": "3:00 PM",
            "coram": "Justice John Doe, Justice Jane Smith, Justice David Johnson",
            "remark": "fj",
            "proceedings": "Final judgment. Court granted specific performance. Defendant ordered to complete contract within 60 days."
        },
        {
            "time": "9:45 AM",
            "coram": "Justice Lisa Anderson",
            "remark": "fh",
            "proceedings": "Preliminary hearing. Parties confirmed readiness for trial. Witness list finalized."
        },
        {
            "time": "1:30 PM",
            "coram": "Justice Robert Taylor, Justice Mary Davis",
            "remark": "fr",
            "proceedings": "Ruling on expert evidence. Expert reports admitted. Court directed parties to file closing submissions."
        },
        {
            "time": "12:00 PM",
            "coram": "Justice Michael Brown, Justice Sarah Wilson",
            "remark": "fj",
            "proceedings": "Judgment delivered. Court found defendant liable. Damages assessed at $75,000. Costs follow the event."
        }
    ]
    
    # Clear existing hearings first
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM case_hearings"))
        conn.commit()
        print("Cleared existing hearings")
    
    hearings_created = 0
    
    with engine.connect() as conn:
        for case_id in case_ids:
            # Create 2-5 hearings per case (random)
            num_hearings = random.randint(2, 5)
            
            # Get case date for reference
            case_result = conn.execute(text("SELECT date FROM reported_cases WHERE id = :case_id"), {"case_id": case_id})
            case_row = case_result.fetchone()
            if case_row and case_row[0]:
                case_date = case_row[0]
                # Convert to datetime if it's a string
                if isinstance(case_date, str):
                    try:
                        case_date = datetime.strptime(case_date, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        try:
                            case_date = datetime.strptime(case_date, '%Y-%m-%d')
                        except ValueError:
                            case_date = datetime.now()
            else:
                case_date = datetime.now()
            
            for i in range(num_hearings):
                # Select random hearing template
                template = random.choice(hearing_templates)
                
                # Calculate hearing date (spread over time)
                hearing_date = case_date + timedelta(days=i * 30 + random.randint(0, 15))  # 30 days apart with some variation
                
                # Insert hearing
                insert_sql = """
                INSERT INTO case_hearings (case_id, hearing_date, hearing_time, coram, remark, proceedings)
                VALUES (:case_id, :hearing_date, :hearing_time, :coram, :remark, :proceedings)
                """
                
                hearing_data = {
                    'case_id': case_id,
                    'hearing_date': hearing_date,
                    'hearing_time': template['time'],
                    'coram': template['coram'],
                    'remark': template['remark'],
                    'proceedings': template['proceedings']
                }
                
                conn.execute(text(insert_sql), hearing_data)
                hearings_created += 1
            
            # Progress indicator
            if case_id % 100 == 0:
                print(f"Processed {case_id} cases...")
        
        conn.commit()
        print(f"Successfully created {hearings_created} case hearings for {len(case_ids)} cases")
    
    # Show statistics
    with engine.connect() as conn:
        total_hearings = conn.execute(text("SELECT COUNT(*) FROM case_hearings")).fetchone()[0]
        fh_count = conn.execute(text("SELECT COUNT(*) FROM case_hearings WHERE remark = 'fh'")).fetchone()[0]
        fr_count = conn.execute(text("SELECT COUNT(*) FROM case_hearings WHERE remark = 'fr'")).fetchone()[0]
        fj_count = conn.execute(text("SELECT COUNT(*) FROM case_hearings WHERE remark = 'fj'")).fetchone()[0]
        
        print(f"\nHearing Statistics:")
        print(f"Total hearings: {total_hearings}")
        print(f"For Hearing (FH): {fh_count}")
        print(f"For Ruling (FR): {fr_count}")
        print(f"For Judgement (FJ): {fj_count}")

if __name__ == "__main__":
    print("Creating case hearings for all cases...")
    create_hearings_for_all_cases()
    print("Done!")
