#!/usr/bin/env python3
"""
Script to populate case_hearings table with sample data
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from database import engine, get_db
from models.case_hearings import CaseHearing, HearingRemark
from models.reported_cases import ReportedCases
from models.case_metadata import CaseMetadata
from models.case_search_index import CaseSearchIndex
from sqlalchemy import text

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def populate_case_hearings():
    """Populate case_hearings table with sample data"""
    db = SessionLocal()
    
    try:
        # Get some sample cases
        cases = db.query(ReportedCases).limit(50).all()
        
        if not cases:
            print("No cases found in database. Please ensure cases are populated first.")
            return
        
        print(f"Found {len(cases)} cases. Creating hearings...")
        
        # Sample hearing data
        sample_hearings = [
            {
                "hearing_time": "10:00 AM",
                "coram": "Justice John Doe, Justice Jane Smith",
                "remark": HearingRemark.FH,
                "proceedings": "Case called for hearing. Plaintiff's counsel presented opening arguments. Defendant's counsel requested adjournment for further preparation. Case adjourned to next available date."
            },
            {
                "hearing_time": "2:00 PM", 
                "coram": "Justice John Doe, Justice Jane Smith",
                "remark": HearingRemark.FR,
                "proceedings": "Court delivered ruling on preliminary objections. Objections overruled. Case to proceed to full hearing. Parties directed to file witness statements within 14 days."
            },
            {
                "hearing_time": "11:30 AM",
                "coram": "Justice John Doe, Justice Jane Smith, Justice Michael Brown",
                "remark": HearingRemark.FJ,
                "proceedings": "Final judgment delivered. Court found in favor of plaintiff. Defendant ordered to pay damages of $50,000 plus costs. Judgment to be executed within 30 days."
            },
            {
                "hearing_time": "9:30 AM",
                "coram": "Justice Sarah Wilson",
                "remark": HearingRemark.FH,
                "proceedings": "Interim application heard. Plaintiff's application for interim injunction granted. Defendant restrained from disposing of property pending final determination of case."
            },
            {
                "hearing_time": "3:15 PM",
                "coram": "Justice David Johnson, Justice Mary Davis",
                "remark": HearingRemark.FR,
                "proceedings": "Ruling on admissibility of evidence. Expert witness testimony admitted. Documentary evidence marked as exhibits. Case set down for final hearing."
            }
        ]
        
        hearings_created = 0
        
        for case in cases:
            # Create 2-4 hearings per case
            num_hearings = 2 + (case.id % 3)  # 2-4 hearings
            
            for i in range(num_hearings):
                hearing_data = sample_hearings[i % len(sample_hearings)]
                
                # Calculate hearing date (spread over time)
                base_date = case.date if case.date else datetime.now()
                hearing_date = base_date + timedelta(days=i * 30)  # 30 days apart
                
                hearing = CaseHearing(
                    case_id=case.id,
                    hearing_date=hearing_date,
                    hearing_time=hearing_data["hearing_time"],
                    coram=hearing_data["coram"],
                    remark=hearing_data["remark"],
                    proceedings=hearing_data["proceedings"]
                )
                
                db.add(hearing)
                hearings_created += 1
        
        db.commit()
        print(f"Successfully created {hearings_created} case hearings")
        
        # Show some statistics
        total_hearings = db.query(CaseHearing).count()
        fh_count = db.query(CaseHearing).filter(CaseHearing.remark == HearingRemark.FH).count()
        fr_count = db.query(CaseHearing).filter(CaseHearing.remark == HearingRemark.FR).count()
        fj_count = db.query(CaseHearing).filter(CaseHearing.remark == HearingRemark.FJ).count()
        
        print(f"\nHearing Statistics:")
        print(f"Total hearings: {total_hearings}")
        print(f"For Hearing (FH): {fh_count}")
        print(f"For Ruling (FR): {fr_count}")
        print(f"For Judgement (FJ): {fj_count}")
        
    except Exception as e:
        print(f"Error populating case hearings: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Populating case hearings table...")
    populate_case_hearings()
    print("Done!")
