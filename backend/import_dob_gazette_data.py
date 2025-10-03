#!/usr/bin/env python3
"""
Script to import Change of Date of Birth data into the gazette system
"""

import pandas as pd
import sys
import os
from datetime import datetime
import re
from decimal import Decimal

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models.gazette import Gazette
from models.people import People
from sqlalchemy.orm import Session
from sqlalchemy import or_

def parse_date(date_str):
    """Parse date string in format like '22nd March, 1993' to datetime"""
    if pd.isna(date_str) or not date_str:
        return None
    
    try:
        # Remove ordinal suffixes (st, nd, rd, th)
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(date_str))
        
        # Parse the date
        date_obj = datetime.strptime(date_str, '%d %B, %Y')
        return date_obj
    except:
        try:
            # Try alternative format
            date_obj = datetime.strptime(date_str, '%d %b, %Y')
            return date_obj
        except:
            print(f"Could not parse date: {date_str}")
            return None

def extract_gazette_info(source_str):
    """Extract gazette number, date, and page from source string"""
    if pd.isna(source_str) or not source_str:
        return None, None, None
    
    # Pattern: "No. 172, 18th November 2019, Page 3516"
    pattern = r'No\. (\d+), (\d+(?:st|nd|rd|th)? \w+ \d{4}), Page (\d+)'
    match = re.search(pattern, str(source_str))
    
    if match:
        gazette_number = match.group(1)
        date_str = match.group(2)
        page = match.group(3)
        
        # Parse the date
        try:
            date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
            gazette_date = datetime.strptime(date_str, '%d %B %Y')
        except:
            try:
                gazette_date = datetime.strptime(date_str, '%d %b %Y')
            except:
                gazette_date = None
        
        return gazette_number, gazette_date, page
    
    return None, None, None

def find_or_create_person(db: Session, name: str, address: str = None, profession: str = None):
    """Find existing person or create new one"""
    # Clean the name (remove prefixes like Mr., Miss, etc.)
    clean_name = re.sub(r'^(Mr\.|Miss|Mrs\.|Ms\.|Dr\.|Prof\.|Rev\.)\s+', '', name)
    
    # Search for existing person
    person = db.query(People).filter(
        or_(
            People.full_name.ilike(f"%{clean_name}%"),
            People.full_name.ilike(f"%{name}%")
        )
    ).first()
    
    if person:
        return person
    
    # Create new person
    person = People(
        full_name=clean_name,
        first_name=clean_name.split()[0] if clean_name.split() else clean_name,
        last_name=' '.join(clean_name.split()[1:]) if len(clean_name.split()) > 1 else '',
        address=address,
        occupation=profession,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(person)
    db.flush()  # Get the ID
    return person

def import_dob_data():
    """Import Change of Date of Birth data"""
    try:
        # Read the Excel file
        file_path = "../Change of Date of Birth.xlsx"
        df = pd.read_excel(file_path, sheet_name='GN172_Change of Date of Birth ')
        
        print(f"Found {len(df)} records to import")
        
        # Get database session
        db = next(get_db())
        
        imported_count = 0
        skipped_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Extract data
                item_number = row['Item No.']
                name = row['Name of Person']
                address = row['Address'] if pd.notna(row['Address']) else None
                profession = row['Profession'] if pd.notna(row['Profession']) else None
                old_dob = row['Old Date of Birth']
                new_dob = row['New Date of Birth']
                effective_date = row['Effective Date of Change']
                remarks = row['Remarks'] if pd.notna(row['Remarks']) else None
                source = row['Source (Gazette No., Date, Page)']
                
                # Parse dates
                old_dob_parsed = parse_date(old_dob)
                new_dob_parsed = parse_date(new_dob)
                effective_date_parsed = parse_date(effective_date)
                
                # Extract gazette info
                gazette_number, gazette_date, page = extract_gazette_info(source)
                
                # Find or create person
                person = find_or_create_person(db, name, address, profession)
                
                # Create gazette entry
                content = f"Change of Date of Birth for {name}\n\n"
                content += f"Old Date of Birth: {old_dob}\n"
                content += f"New Date of Birth: {new_dob}\n"
                content += f"Effective Date of Change: {effective_date}\n"
                if address:
                    content += f"Address: {address}\n"
                if profession:
                    content += f"Profession: {profession}\n"
                content += f"Source: {source}\n"
                
                gazette = Gazette(
                           item_number=str(item_number),
                           gazette_type='CHANGE_OF_DATE_OF_BIRTH',
                           title=f"Change of Date of Birth - {name}",
                           content=content,
                           old_name=name,  # Store the full name with prefix
                           new_name=name,  # Same name, just DOB changed
                           old_date_of_birth=old_dob_parsed,
                           new_date_of_birth=new_dob_parsed,
                           effective_date_of_change=effective_date_parsed,
                           gazette_number=gazette_number,
                           gazette_date=gazette_date,
                           page_number=page,
                           source=source,
                           remarks=remarks,
                           person_id=person.id,
                           is_public=True,
                           status='PUBLISHED',
                           priority='MEDIUM',
                           jurisdiction='Ghana',
                           court_location='High Court',
                           publication_date=gazette_date,  # Use gazette_date as publication_date
                           created_at=datetime.utcnow(),
                           updated_at=datetime.utcnow()
                       )
                
                db.add(gazette)
                imported_count += 1
                
                if imported_count % 10 == 0:
                    print(f"Imported {imported_count} records...")
                
            except Exception as e:
                error_msg = f"Row {index + 1}: {str(e)}"
                errors.append(error_msg)
                skipped_count += 1
                print(f"Error processing row {index + 1}: {e}")
                db.rollback()  # Rollback on error
        
        # Commit all changes
        db.commit()
        
        print(f"\n=== IMPORT SUMMARY ===")
        print(f"Total records processed: {len(df)}")
        print(f"Successfully imported: {imported_count}")
        print(f"Skipped due to errors: {skipped_count}")
        
        if errors:
            print(f"\nErrors encountered:")
            for error in errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        # Update person records with gazette data
        print(f"\nUpdating person records with gazette data...")
        update_person_gazette_data(db)
        
        print(f"\nImport completed successfully!")
        
    except Exception as e:
        print(f"Fatal error during import: {e}")
        if 'db' in locals():
            db.rollback()
        raise
    finally:
        if 'db' in locals():
            db.close()

def update_person_gazette_data(db: Session):
    """Update person records with gazette data"""
    try:
        # Get all people with gazette entries
        people_with_gazette = db.query(People).join(Gazette).filter(
            Gazette.gazette_type == 'CHANGE_OF_DATE_OF_BIRTH'
        ).all()
        
        for person in people_with_gazette:
            # Get the latest gazette entry for this person
            latest_gazette = db.query(Gazette).filter(
                Gazette.person_id == person.id,
                Gazette.gazette_type == 'CHANGE_OF_DATE_OF_BIRTH'
            ).order_by(Gazette.effective_date_of_change.desc()).first()
            
            if latest_gazette:
                # Update person with gazette data
                person.date_of_birth = latest_gazette.new_date_of_birth
                person.old_date_of_birth = latest_gazette.old_date_of_birth
                person.effective_date_of_change = latest_gazette.effective_date_of_change
                person.gazette_remarks = latest_gazette.remarks
                person.gazette_source = latest_gazette.source
                person.gazette_reference = latest_gazette.gazette_number
                person.updated_at = datetime.utcnow()
        
        db.commit()
        print(f"Updated {len(people_with_gazette)} person records with gazette data")
        
    except Exception as e:
        print(f"Error updating person records: {e}")
        db.rollback()

if __name__ == "__main__":
    import_dob_data()
