from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class JudgeStatus(enum.Enum):
    active = "active"
    retired = "retired"
    deceased = "deceased"
    suspended = "suspended"

class Judges(Base):
    __tablename__ = "judges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    title = Column(String(100), nullable=True)  # e.g., "Justice", "Judge", "Chief Justice"
    court_type = Column(String(50), nullable=True, index=True)  # e.g., "Supreme Court", "High Court"
    court_division = Column(String(100), nullable=True)  # e.g., "Commercial Division", "Criminal Division"
    region = Column(String(50), nullable=True, index=True)
    status = Column(Enum(JudgeStatus), default=JudgeStatus.active, nullable=False)
    bio = Column(Text, nullable=True)  # Brief biography or background
    appointment_date = Column(DateTime, nullable=True)
    retirement_date = Column(DateTime, nullable=True)
    contact_info = Column(Text, nullable=True)  # JSON string for contact details
    specializations = Column(Text, nullable=True)  # Areas of law expertise
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Judge(name='{self.name}', title='{self.title}', court_type='{self.court_type}')>"
