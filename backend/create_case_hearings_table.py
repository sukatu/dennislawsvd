#!/usr/bin/env python3
"""
Script to create case_hearings table and populate with sample data
"""

from sqlalchemy import create_engine, text
from config import settings

def create_hearings_table():
    """Create the case_hearings table"""
    engine = create_engine(settings.database_url)
    
    # Create table SQL
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS case_hearings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        case_id BIGINT NOT NULL,
        hearing_date DATETIME NOT NULL,
        hearing_time VARCHAR(20),
        coram TEXT,
        remark ENUM('fh', 'fr', 'fj') NOT NULL,
        proceedings TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
        print("Case hearings table created successfully")

def populate_hearings_data():
    """Populate the case_hearings table with sample data"""
    engine = create_engine(settings.database_url)
    
    # Sample hearings data
    sample_hearings = [
        (1, '2024-01-15 10:00:00', '10:00 AM', 'Justice John Doe, Justice Jane Smith', 'fh', 'Case called for hearing. Plaintiff\'s counsel presented opening arguments. Defendant\'s counsel requested adjournment for further preparation. Case adjourned to next available date.'),
        (1, '2024-02-15 14:00:00', '2:00 PM', 'Justice John Doe, Justice Jane Smith', 'fr', 'Court delivered ruling on preliminary objections. Objections overruled. Case to proceed to full hearing. Parties directed to file witness statements within 14 days.'),
        (1, '2024-03-15 11:30:00', '11:30 AM', 'Justice John Doe, Justice Jane Smith, Justice Michael Brown', 'fj', 'Final judgment delivered. Court found in favor of plaintiff. Defendant ordered to pay damages of $50,000 plus costs. Judgment to be executed within 30 days.'),
        (2, '2024-01-20 09:30:00', '9:30 AM', 'Justice Sarah Wilson', 'fh', 'Interim application heard. Plaintiff\'s application for interim injunction granted. Defendant restrained from disposing of property pending final determination of case.'),
        (2, '2024-02-20 15:15:00', '3:15 PM', 'Justice David Johnson, Justice Mary Davis', 'fr', 'Ruling on admissibility of evidence. Expert witness testimony admitted. Documentary evidence marked as exhibits. Case set down for final hearing.'),
        (2, '2024-03-20 10:45:00', '10:45 AM', 'Justice David Johnson, Justice Mary Davis', 'fj', 'Judgment delivered. Court dismissed the action. Plaintiff\'s claim found to be without merit. Costs awarded to defendant.'),
        (3, '2024-01-25 11:00:00', '11:00 AM', 'Justice Robert Taylor', 'fh', 'Case management conference. Parties agreed on discovery timeline. Trial date fixed for next term.'),
        (3, '2024-02-25 14:30:00', '2:30 PM', 'Justice Robert Taylor, Justice Lisa Anderson', 'fr', 'Ruling on summary judgment application. Application granted in part. Some claims dismissed, others to proceed to trial.'),
        (3, '2024-03-25 10:00:00', '10:00 AM', 'Justice Robert Taylor, Justice Lisa Anderson', 'fj', 'Final judgment. Court awarded damages of $25,000 to plaintiff. Interest at 10% per annum from date of breach.'),
        (4, '2024-01-30 09:00:00', '9:00 AM', 'Justice Michael Brown', 'fh', 'Preliminary hearing. Parties confirmed readiness for trial. Witness list finalized.'),
        (4, '2024-02-28 13:00:00', '1:00 PM', 'Justice Michael Brown, Justice Sarah Wilson', 'fr', 'Ruling on expert evidence. Expert reports admitted. Court directed parties to file closing submissions.'),
        (4, '2024-03-30 12:00:00', '12:00 PM', 'Justice Michael Brown, Justice Sarah Wilson', 'fj', 'Judgment delivered. Court found defendant liable. Damages assessed at $75,000. Costs follow the event.'),
        (5, '2024-02-05 10:30:00', '10:30 AM', 'Justice Jane Smith', 'fh', 'Case called for directions. Parties agreed on procedural matters. Discovery ordered.'),
        (5, '2024-03-05 15:00:00', '3:00 PM', 'Justice Jane Smith, Justice David Johnson', 'fr', 'Ruling on jurisdiction. Court found it has jurisdiction. Case to proceed.'),
        (5, '2024-04-05 11:15:00', '11:15 AM', 'Justice Jane Smith, Justice David Johnson', 'fj', 'Final judgment. Court granted specific performance. Defendant ordered to complete contract within 60 days.')
    ]
    
    insert_sql = """
    INSERT INTO case_hearings (case_id, hearing_date, hearing_time, coram, remark, proceedings)
    VALUES (:case_id, :hearing_date, :hearing_time, :coram, :remark, :proceedings)
    """
    
    with engine.connect() as conn:
        for hearing in sample_hearings:
            hearing_dict = {
                'case_id': hearing[0],
                'hearing_date': hearing[1],
                'hearing_time': hearing[2],
                'coram': hearing[3],
                'remark': hearing[4],
                'proceedings': hearing[5]
            }
            conn.execute(text(insert_sql), hearing_dict)
        conn.commit()
        print(f"Inserted {len(sample_hearings)} case hearings")

if __name__ == "__main__":
    print("Creating case hearings table...")
    create_hearings_table()
    
    print("Populating case hearings data...")
    populate_hearings_data()
    
    print("Done!")
