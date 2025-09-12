from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, Date, DECIMAL
from sqlalchemy.sql import func
from database import Base

class Companies(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    short_name = Column(String(100), nullable=True)
    logo_url = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    region = Column(String(100), nullable=True, index=True)
    country = Column(String(100), nullable=True, default="Ghana")
    postal_code = Column(String(20), nullable=True)
    
    # Comprehensive Company Profile Fields
    type_of_company = Column(String(100), nullable=True)  # Public Limited, Private Limited, etc.
    district = Column(String(100), nullable=True)
    date_of_incorporation = Column(Date, nullable=True)
    date_of_commencement = Column(Date, nullable=True)
    nature_of_business = Column(Text, nullable=True)
    registration_number = Column(String(100), nullable=True, unique=True)
    tax_identification_number = Column(String(50), nullable=True, unique=True)
    phone_number = Column(String(20), nullable=True)
    
    # Directors (JSON array)
    directors = Column(JSON, nullable=True)
    
    # Secretary (JSON object)
    secretary = Column(JSON, nullable=True)
    
    # Auditor (JSON object)
    auditor = Column(JSON, nullable=True)
    
    # Capital Details
    authorized_shares = Column(Integer, nullable=True)
    stated_capital = Column(DECIMAL(15, 2), nullable=True)
    
    # Shareholders (JSON array)
    shareholders = Column(JSON, nullable=True)
    
    # Other Linked Companies (JSON array)
    other_linked_companies = Column(JSON, nullable=True)
    
    # Legacy fields (keeping for backward compatibility)
    tin_number = Column(String(50), nullable=True, unique=True)
    established_date = Column(DateTime, nullable=True)
    company_type = Column(String(50), nullable=True)  # Limited, Partnership, Sole Proprietorship, etc.
    industry = Column(String(100), nullable=True)  # Technology, Manufacturing, Services, etc.
    ownership_type = Column(String(50), nullable=True)  # Public, Private, Foreign, etc.
    
    # Business information
    business_activities = Column(JSON, nullable=True)  # Array of business activities
    previous_names = Column(JSON, nullable=True)  # Array of previous names
    board_of_directors = Column(JSON, nullable=True)  # Array of board members
    key_personnel = Column(JSON, nullable=True)  # Array of key personnel
    subsidiaries = Column(JSON, nullable=True)  # Array of subsidiary companies
    
    # Financial information
    annual_revenue = Column(Float, nullable=True)
    net_worth = Column(Float, nullable=True)
    employee_count = Column(Integer, default=0)
    rating = Column(String(10), nullable=True)  # A+, A, B+, etc.
    
    # Contact information
    head_office_address = Column(Text, nullable=True)
    customer_service_phone = Column(String(50), nullable=True)
    customer_service_email = Column(String(255), nullable=True)
    
    # Digital presence
    has_website = Column(Boolean, default=False)
    has_social_media = Column(Boolean, default=False)
    has_mobile_app = Column(Boolean, default=False)
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime, nullable=True)
    verification_notes = Column(Text, nullable=True)
    search_count = Column(Integer, default=0)
    last_searched = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE")
