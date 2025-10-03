from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Set to True for SQL query logging
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections every 5 minutes
    pool_size=20,         # Increase pool size
    max_overflow=30,      # Allow more overflow connections
    pool_timeout=30,      # Timeout for getting connection from pool
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Create metadata
metadata = MetaData()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    # Import all models to ensure they are registered
    from models.user import User
    from models.people import People
    from models.banks import Banks
    from models.insurance import Insurance
    from models.reported_cases import ReportedCases
    from models.legal_history import LegalHistory, CaseMention, LegalSearchIndex
    from models.judges import Judges
    from models.court_types import CourtTypes
    from models.contact_request import ContactRequest
    Base.metadata.create_all(bind=engine)

# Drop all tables (use with caution)
def drop_tables():
    Base.metadata.drop_all(bind=engine)
