import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.gazette import Gazette, GazetteType, GazetteStatus, GazettePriority
from models.people import People
from services.auto_analytics_generator import AutoAnalyticsGenerator
import re
import logging
from typing import Optional, Tuple
from sqlalchemy import func

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def parse_gazette_date(date_str: str) -> Optional[datetime]:
    """Parses various date string formats for gazette dates."""
    if pd.isna(date_str):
        return None

    # Try common date formats
    formats = [
        "%d %B %Y",  # 18 November 2019
        "%Y-%m-%d %H:%M:%S", # 2019-11-18 00:00:00 (from Excel)
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str).strip(), fmt)
        except ValueError:
            continue
    logging.warning(f"Could not parse date: {date_str}")
    return None

def parse_appointment_date(date_str: str) -> Optional[datetime]:
    """Parses appointment date formats like '23rd February, 2017'"""
    if pd.isna(date_str):
        return None
    
    # Clean up the date string
    date_str = str(date_str).strip()
    
    # Try to parse formats like "23rd February, 2017"
    try:
        # Remove ordinal suffixes (st, nd, rd, th)
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
        return datetime.strptime(date_str, "%d %B, %Y")
    except ValueError:
        pass
    
    # Try other common formats
    formats = [
        "%d %B %Y",  # 23 February 2017
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    logging.warning(f"Could not parse appointment date: {date_str}")
    return None

def extract_gazette_info(source_str: str) -> Tuple[Optional[str], Optional[datetime], Optional[int]]:
    """Extract gazette number, date, and page from source string"""
    if pd.isna(source_str):
        return None, None, None
    
    source = str(source_str).strip()
    
    # Pattern: "No. 172, 18th November 2019, Page 3505"
    pattern = r'No\.\s*(\d+),\s*(\d+(?:st|nd|rd|th)?\s+\w+\s+\d{4}),\s*Page\s*(\d+)'
    match = re.search(pattern, source)
    
    if match:
        gazette_number = match.group(1)
        date_str = match.group(2)
        page_number = int(match.group(3))
        
        # Parse the date
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)  # Remove ordinal
        try:
            gazette_date = datetime.strptime(date_str, "%d %B %Y")
        except ValueError:
            gazette_date = None
            
        return gazette_number, gazette_date, page_number
    
    return None, None, None

def find_or_create_person(db: Session, full_name: str, church: Optional[str] = None, location: Optional[str] = None) -> People:
    """Finds an existing person or creates a new one."""
    person = db.query(People).filter(People.full_name.ilike(full_name)).first()
    if not person:
        logging.info(f"Creating new person: {full_name}")
        
        # Extract title and name parts
        title = ""
        name_parts = full_name.split()
        if name_parts[0] in ['Reverend', 'Rev.', 'Dr.', 'Archbishop', 'Bishop', 'Pastor']:
            title = name_parts[0]
            name_parts = name_parts[1:]
        
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        
        person = People(
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            occupation=f"Marriage Officer - {title}" if title else "Marriage Officer",
            organization=church,
            address=location,
            created_by=None
        )
        db.add(person)
        db.commit()
        db.refresh(person)

        # Generate analytics for the newly created person
        try:
            generator = AutoAnalyticsGenerator(db)
            generator.generate_analytics_for_person(person.id)
            logging.info(f"Analytics generated for new person {person.id}")
        except Exception as analytics_error:
            logging.warning(f"Failed to generate analytics for new person {person.id}: {analytics_error}")
    return person

def sync_gazette_to_people(db: Session, gazette_entry: Gazette, person: People):
    """Synchronizes relevant gazette data to the person's profile."""
    updated = False
    
    if gazette_entry.gazette_type == GazetteType.APPOINTMENT_OF_MARRIAGE_OFFICERS:
        # Update person with marriage officer information
        if gazette_entry.officer_title and (not person.occupation or "Marriage Officer" not in person.occupation):
            person.occupation = f"{gazette_entry.officer_title} - Marriage Officer"
            updated = True
        
        if gazette_entry.appointment_authority and (not person.organization or person.organization != gazette_entry.appointment_authority):
            person.organization = gazette_entry.appointment_authority
            updated = True
        
        if gazette_entry.jurisdiction_area and (not person.address or person.address != gazette_entry.jurisdiction_area):
            person.address = gazette_entry.jurisdiction_area
            updated = True
    
    if updated:
        db.commit()
        logging.info(f"Updated person {person.id} with gazette data")

def import_marriage_officers_data():
    """Import marriage officers data from Excel file"""
    db = SessionLocal()
    
    try:
        # Read the Excel file
        file_path = "../Appointment of Marriage Officers.xlsx"
        sheet_name = "GN172_Marriage Officers"
        
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
        
        logging.info(f"Found {len(df)} marriage officer records to import")
        
        imported_count = 0
        skipped_count = 0
        
        for index, row in df.iterrows():
            try:
                # Extract data from row
                officer_name = row['Name of the Appointed Marriage Officer']
                gender = row['Gender (Inferred)']
                church = row['Church of the Marriage Officer']
                denomination = row['Denomination (if available)']
                location = row['Location of the Church']
                appointing_authority = row['Appointing Authority']
                appointment_date_str = row['Appointment Date']
                source = row['Source (Gazette No., Date, Page)']
                
                if pd.isna(officer_name):
                    logging.warning(f"Row {index + 1}: Skipping record with no officer name")
                    skipped_count += 1
                    continue
                
                # Parse dates
                appointment_date = parse_appointment_date(appointment_date_str)
                gazette_number, gazette_date, page_number = extract_gazette_info(source)
                
                # Create content for the gazette entry
                content = f"""Appointment of Marriage Officer - {officer_name}

Officer Details:
- Name: {officer_name}
- Gender: {gender if not pd.isna(gender) else 'N/A'}
- Church: {church if not pd.isna(church) else 'N/A'}
- Denomination: {denomination if not pd.isna(denomination) else 'N/A'}
- Location: {location if not pd.isna(location) else 'N/A'}
- Appointing Authority: {appointing_authority if not pd.isna(appointing_authority) else 'N/A'}
- Appointment Date: {appointment_date_str if not pd.isna(appointment_date_str) else 'N/A'}
- Source: {source if not pd.isna(source) else 'N/A'}
"""
                
                # Create gazette entry
                gazette = Gazette(
                    title=f"Appointment of Marriage Officer - {officer_name}",
                    content=content,
                    gazette_type=GazetteType.APPOINTMENT_OF_MARRIAGE_OFFICERS,
                    status=GazetteStatus.PUBLISHED,
                    priority=GazettePriority.MEDIUM,
                    publication_date=gazette_date or datetime.utcnow(),
                    source=source,
                    gazette_number=gazette_number,
                    page_number=page_number,
                    jurisdiction="Ghana",
                    court_location="High Court",
                    officer_name=officer_name,
                    officer_title=officer_name.split()[0] if officer_name.split() else None,  # Extract title
                    appointment_authority=appointing_authority,
                    jurisdiction_area=location,
                    gazette_date=gazette_date,
                    gazette_page=page_number,
                    item_number=f"MO{index + 1:03d}",  # Marriage Officer item number
                    is_public=True,
                    created_by=None
                )
                
                db.add(gazette)
                db.commit()
                db.refresh(gazette)
                
                # Find or create person
                person = find_or_create_person(db, officer_name, church, location)
                
                # Link gazette to person
                gazette.person_id = person.id
                db.commit()
                db.refresh(gazette)
                
                # Sync gazette data to person
                sync_gazette_to_people(db, gazette, person)
                
                imported_count += 1
                logging.info(f"Imported marriage officer: {officer_name}")
                
            except Exception as e:
                logging.error(f"Error importing row {index + 1}: {e}")
                db.rollback()
                skipped_count += 1
                continue
        
        logging.info(f"\n=== IMPORT SUMMARY ===")
        logging.info(f"Total records processed: {len(df)}")
        logging.info(f"Successfully imported: {imported_count}")
        logging.info(f"Skipped: {skipped_count}")
        
        # Verify import
        total_gazettes = db.query(Gazette).filter(
            Gazette.gazette_type == GazetteType.APPOINTMENT_OF_MARRIAGE_OFFICERS
        ).count()
        logging.info(f"Total marriage officer gazettes in database: {total_gazettes}")
        
    except Exception as e:
        logging.error(f"Error during import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_marriage_officers_data()
