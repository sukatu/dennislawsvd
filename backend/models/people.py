from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base

class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    previous_names = Column(JSON, nullable=True)  # Array of previous names
    date_of_birth = Column(DateTime, nullable=True, index=True)
    date_of_death = Column(DateTime, nullable=True, index=True)
    id_number = Column(String(50), nullable=True, index=True)
    phone_number = Column(String(20), nullable=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    
    # Address Information
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    region = Column(String(100), nullable=True, index=True)
    country = Column(String(100), nullable=True, default="Ghana")
    postal_code = Column(String(20), nullable=True)
    
    # Legal Information
    risk_level = Column(String(20), nullable=True, index=True)  # Low, Medium, High
    risk_score = Column(Float, nullable=True, index=True)
    case_count = Column(Integer, default=0, index=True)
    case_types = Column(JSON, nullable=True)  # Array of case types
    court_records = Column(JSON, nullable=True)  # Array of court records
    
    # Professional Information
    occupation = Column(String(100), nullable=True, index=True)
    employer = Column(String(200), nullable=True, index=True)
    organization = Column(String(200), nullable=True, index=True)
    job_title = Column(String(100), nullable=True)
    
    # Family Information
    marital_status = Column(String(20), nullable=True)
    spouse_name = Column(String(200), nullable=True)
    children_count = Column(Integer, default=0)
    emergency_contact = Column(String(200), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    
    # Additional Information
    nationality = Column(String(100), nullable=True, default="Ghanaian")
    gender = Column(String(10), nullable=True, index=True)
    education_level = Column(String(50), nullable=True)
    languages = Column(JSON, nullable=True)  # Array of languages spoken
    
    # Search and Verification
    is_verified = Column(Boolean, default=False, index=True)
    verification_date = Column(DateTime, nullable=True)
    verification_notes = Column(Text, nullable=True)
    last_searched = Column(DateTime, nullable=True, index=True)
    search_count = Column(Integer, default=0, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=True)  # User ID who created this record
    updated_by = Column(Integer, nullable=True)  # User ID who last updated this record
    
    # Status
    status = Column(String(20), default="active", index=True)  # active, inactive, archived
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<People(id={self.id}, name='{self.full_name}', risk_level='{self.risk_level}')>"
