from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Insurance(Base):
    __tablename__ = "insurance"

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
    
    # Insurance specific fields
    license_number = Column(String(100), nullable=True, unique=True)
    registration_number = Column(String(100), nullable=True)
    established_date = Column(DateTime, nullable=True)
    insurance_type = Column(String(50), nullable=True)  # Life, General, Health, Motor, etc.
    ownership_type = Column(String(50), nullable=True)  # Public, Private, Foreign, etc.
    
    # Services offered
    services = Column(JSON, nullable=True)  # Array of insurance products
    previous_names = Column(JSON, nullable=True)  # Array of previous names
    coverage_areas = Column(JSON, nullable=True)  # Array of regions covered
    branches_count = Column(Integer, default=0)
    agents_count = Column(Integer, default=0)
    
    # Financial information
    total_assets = Column(Float, nullable=True)
    net_worth = Column(Float, nullable=True)
    premium_income = Column(Float, nullable=True)
    claims_paid = Column(Float, nullable=True)
    rating = Column(String(10), nullable=True)  # A+, A, B+, etc.
    
    # Contact information
    head_office_address = Column(Text, nullable=True)
    customer_service_phone = Column(String(50), nullable=True)
    customer_service_email = Column(String(255), nullable=True)
    claims_phone = Column(String(50), nullable=True)
    claims_email = Column(String(255), nullable=True)
    
    # Digital services
    has_mobile_app = Column(Boolean, default=False)
    has_online_portal = Column(Boolean, default=False)
    has_online_claims = Column(Boolean, default=False)
    has_24_7_support = Column(Boolean, default=False)
    
    # Specializations
    specializes_in = Column(JSON, nullable=True)  # Array of specializations
    target_market = Column(String(100), nullable=True)  # Individual, Corporate, SME, etc.
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime, nullable=True)
    verification_notes = Column(Text, nullable=True)
    
    # Search and analytics
    search_count = Column(Integer, default=0)
    last_searched = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    # Additional fields
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, INACTIVE, SUSPENDED
    
    # Relationships
    analytics = relationship("InsuranceAnalytics", back_populates="insurance", uselist=False)
    case_statistics = relationship("InsuranceCaseStatistics", back_populates="insurance", uselist=False)
    gazette_entries = relationship("Gazette", back_populates="insurance", lazy="dynamic")
