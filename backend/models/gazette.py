from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class GazetteType(str, enum.Enum):
    # Legal Notices
    CHANGE_OF_NAME = "CHANGE_OF_NAME"
    CHANGE_OF_DATE_OF_BIRTH = "CHANGE_OF_DATE_OF_BIRTH"
    CHANGE_OF_PLACE_OF_BIRTH = "CHANGE_OF_PLACE_OF_BIRTH"
    APPOINTMENT_OF_MARRIAGE_OFFICERS = "APPOINTMENT_OF_MARRIAGE_OFFICERS"
    
    # General Categories
    LEGAL_NOTICE = "LEGAL_NOTICE"
    BUSINESS_NOTICE = "BUSINESS_NOTICE"
    PROPERTY_NOTICE = "PROPERTY_NOTICE"
    PERSONAL_NOTICE = "PERSONAL_NOTICE"
    REGULATORY_NOTICE = "REGULATORY_NOTICE"
    COURT_NOTICE = "COURT_NOTICE"
    BANKRUPTCY_NOTICE = "BANKRUPTCY_NOTICE"
    PROBATE_NOTICE = "PROBATE_NOTICE"
    OTHER = "OTHER"

class GazetteStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    CANCELLED = "CANCELLED"

class GazettePriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class Gazette(Base):
    __tablename__ = "gazette_entries"

    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    
    # Classification
    gazette_type = Column(Enum(GazetteType), nullable=False, index=True)
    status = Column(Enum(GazetteStatus), default=GazetteStatus.DRAFT, index=True)
    priority = Column(Enum(GazettePriority), default=GazettePriority.MEDIUM)
    
    # Dates
    publication_date = Column(DateTime, nullable=False, index=True)
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime)
    
    # Source Information
    source = Column(String(200))  # e.g., "High Court", "Registrar General", "Bank of Ghana"
    reference_number = Column(String(100), index=True)
    gazette_number = Column(String(50), index=True)
    page_number = Column(Integer)
    
    # Location Information
    jurisdiction = Column(String(100))  # e.g., "Greater Accra", "Ashanti Region"
    court_location = Column(String(200))
    
    # People/Entities Involved
    person_id = Column(Integer, ForeignKey("people.id"), nullable=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=True, index=True)
    insurance_id = Column(Integer, ForeignKey("insurance.id"), nullable=True, index=True)
    
    # Additional Details
    keywords = Column(JSON)  # Array of keywords for search
    tags = Column(JSON)  # Array of tags for categorization
    gazette_metadata = Column(JSON)  # Additional structured data
    
    # Legal Notice Specific Fields
    # Change of Name Fields
    item_number = Column(String(50), index=True)  # Sequential number (e.g., 24024)
    old_name = Column(String(500), index=True)  # Name used prior to change
    alias_names = Column(JSON)  # Array of aliases/aka names
    new_name = Column(String(500), index=True)  # Name adopted or confirmed
    profession = Column(String(200))  # Current profession/occupation
    effective_date_of_change = Column(DateTime)  # Date the change took effect
    remarks = Column(Text)  # Correction notices or confirmation details
    
    # Change of Date of Birth Fields
    old_date_of_birth = Column(DateTime)  # Original date of birth
    new_date_of_birth = Column(DateTime)  # Corrected date of birth
    place_of_birth = Column(String(200))  # Place of birth
    
    # Change of Place of Birth Fields
    old_place_of_birth = Column(String(200))  # Original place of birth
    new_place_of_birth = Column(String(200))  # New place of birth
    
    # Marriage Officer Fields
    officer_name = Column(String(200))  # Name of appointed marriage officer
    officer_title = Column(String(100))  # Title/position
    appointment_authority = Column(String(200))  # Authority making the appointment
    jurisdiction_area = Column(String(200))  # Area of jurisdiction
    
    # Source Information (Enhanced)
    gazette_number = Column(String(50), index=True)  # Gazette number (e.g., No. 172)
    gazette_date = Column(DateTime)  # Gazette publication date
    gazette_page = Column(Integer)  # Page number in gazette
    source_item_number = Column(String(50))  # Item number in source
    
    # Document Attachments
    document_url = Column(String(500))  # URL to attached document
    document_filename = Column(String(255))
    document_size = Column(Integer)  # File size in bytes
    
    # System Fields
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Visibility
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    person = relationship("People", back_populates="gazette_entries")
    company = relationship("Companies", back_populates="gazette_entries")
    bank = relationship("Banks", back_populates="gazette_entries")
    insurance = relationship("Insurance", back_populates="gazette_entries")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])

class GazetteSearch(Base):
    __tablename__ = "gazette_search_index"
    
    id = Column(Integer, primary_key=True, index=True)
    gazette_id = Column(Integer, ForeignKey("gazette_entries.id"), nullable=False)
    search_text = Column(Text, nullable=False, index=True)  # Combined searchable text
    person_name = Column(String(255), index=True)
    company_name = Column(String(255), index=True)
    keywords_text = Column(Text, index=True)  # Flattened keywords for search
    
    # Relationships
    gazette_entry = relationship("Gazette")

class GazetteView(Base):
    __tablename__ = "gazette_views"
    
    id = Column(Integer, primary_key=True, index=True)
    gazette_id = Column(Integer, ForeignKey("gazette_entries.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    gazette_entry = relationship("Gazette")
    user = relationship("User")
