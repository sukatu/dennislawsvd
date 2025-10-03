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

def create_tables_if_not_exist():
    """Create database tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables checked/created.")

def parse_date_string(date_str: str) -> Optional[datetime]:
    """Parses various date string formats into datetime objects."""
    if pd.isna(date_str):
        return None
    
    # Remove ordinal suffixes (e.g., "st", "nd", "rd", "th")
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    
    formats = [
        "%d %B, %Y",  # 23rd October, 2019
        "%d %B %Y",   # 23 October 2019
        "%Y-%m-%d",   # YYYY-MM-DD
        "%m/%d/%Y",   # MM/DD/YYYY
        "%d/%m/%Y"    # DD/MM/YYYY
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    logging.warning(f"Could not parse date: {date_str}")
    return None

def extract_gazette_info(source_str: str) -> Tuple[Optional[str], Optional[datetime], Optional[str]]:
    """Extracts Gazette Number, Date, and Page from the source string."""
    gazette_number = None
    gazette_date = None
    page_number = None

    # Example: "No. 172, 18th November 2019, Page 3520, 24237"
    match = re.search(r'No\. (\d+),\s*(\d+(?:st|nd|rd|th)?\s+\w+\s+\d{4}),\s*Page\s+(\d+)', source_str, re.IGNORECASE)
    if match:
        gazette_number = match.group(1)
        date_str = match.group(2)
        page_number = match.group(3)
        gazette_date = parse_date_string(date_str)
    
    return gazette_number, gazette_date, page_number

def find_or_create_person(db: Session, name: str, address: Optional[str], profession: Optional[str]) -> People:
    """Finds an existing person or creates a new one."""
    # Try to find by full name (case-insensitive)
    person = db.query(People).filter(func.lower(People.full_name) == func.lower(name)).first()
    
    if not person:
        # Attempt to parse first and last name
        parts = name.split()
        first_name = parts[0] if parts else None
        last_name = parts[-1] if len(parts) > 1 else None
        
        # Remove common prefixes for better matching/creation
        prefixes = ["Mr.", "Mrs.", "Miss", "Dr.", "Prof.", "Rev.", "Hon."]
        for prefix in prefixes:
            if first_name and first_name.startswith(prefix):
                first_name = first_name[len(prefix):].strip()
                break
        
        # Try to find by first and last name
        if first_name and last_name:
            person = db.query(People).filter(
                func.lower(People.first_name) == func.lower(first_name),
                func.lower(People.last_name) == func.lower(last_name)
            ).first()

        if not person:
            logging.info(f"Creating new person: {name}")
            person = People(
                full_name=name,
                first_name=first_name,
                last_name=last_name,
                address=address,
                occupation=profession,
                created_by=1  # Use admin user ID
            )
            db.add(person)
            db.flush()  # Flush to get person.id
            
            # Generate analytics for the new person
            try:
                generator = AutoAnalyticsGenerator(db)
                generator.generate_analytics_for_person(person.id)
                logging.info(f"Analytics generated for new person {person.id}")
            except Exception as analytics_error:
                logging.warning(f"Failed to generate analytics for new person {person.id}: {str(analytics_error)}")
    
    return person

def update_person_gazette_data(db: Session):
    """Update person records with gazette data."""
    # Get all people who have gazette entries - simplified query
    gazette_entries = db.query(Gazette).filter(
        Gazette.gazette_type == 'CHANGE_OF_PLACE_OF_BIRTH'
    ).all()
    
    updated_count = 0
    for gazette in gazette_entries:
        if gazette.person_id:
            person = db.query(People).filter(People.id == gazette.person_id).first()
            if person:
                # Update person with gazette data
                person.place_of_birth = gazette.new_place_of_birth
                person.old_place_of_birth = gazette.old_place_of_birth
                person.effective_date_of_change = gazette.effective_date_of_change
                person.gazette_source = gazette.source
                person.gazette_reference = gazette.gazette_number
                person.updated_at = datetime.utcnow()
                updated_count += 1
    
    db.commit()
    logging.info(f"Updated {updated_count} person records with gazette data")

def import_place_of_birth_data(file_path: str = "../Change of Place of Birth.xlsx", sheet_name: str = "GN172-Change of Place of Birth"):
    """Imports Change of Place of Birth data from Excel into the database."""
    create_tables_if_not_exist()
    
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    df = df.where(pd.notna(df), None)  # Replace NaN with None
    
    # Get database session
    db = SessionLocal()
    
    imported_count = 0
    skipped_count = 0
    errors = []
    
    for index, row in df.iterrows():
        try:
            # Extract data
            item_number = row['Item No.']
            name = row['Name of Person']
            profession = row['Profession'] if pd.notna(row['Profession']) else None
            address = row['Address'] if pd.notna(row['Address']) else None
            old_place_of_birth = row['Mistaken Place of Birth']
            new_place_of_birth = row['Correct Place of Birth']
            effective_date = row['Effective Date of Change']
            remarks = row['Remarks'] if pd.notna(row['Remarks']) else None
            source = row['Source (Gazette No., Date, Page, Number)']
            
            # Parse dates
            effective_date_parsed = parse_date_string(effective_date)
            
            # Extract gazette info
            gazette_number, gazette_date, page = extract_gazette_info(source)
            
            # Find or create person
            person = find_or_create_person(db, name, address, profession)
            
            # Create gazette entry
            content = f"Change of Place of Birth for {name}\n\n"
            content += f"Mistaken Place of Birth: {old_place_of_birth}\n"
            content += f"Correct Place of Birth: {new_place_of_birth}\n"
            content += f"Effective Date of Change: {effective_date}\n"
            if address:
                content += f"Address: {address}\n"
            if profession:
                content += f"Profession: {profession}\n"
            content += f"Source: {source}\n"
            
            gazette = Gazette(
                item_number=str(item_number),
                gazette_type='CHANGE_OF_PLACE_OF_BIRTH',
                title=f"Change of Place of Birth - {name}",
                content=content,
                old_name=name,  # Store the full name
                new_name=name,  # Same name, just place of birth changed
                old_place_of_birth=old_place_of_birth,
                new_place_of_birth=new_place_of_birth,
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
    
    print("Import completed successfully!")

if __name__ == "__main__":
    import_place_of_birth_data()
