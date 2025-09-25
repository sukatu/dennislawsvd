from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class JudgeStatus(str, Enum):
    active = "active"
    retired = "retired"
    deceased = "deceased"
    suspended = "suspended"

class JudgeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Full name of the judge")
    title: Optional[str] = Field(None, max_length=100, description="Title of the judge")
    court_type: Optional[str] = Field(None, max_length=50, description="Type of court")
    court_division: Optional[str] = Field(None, max_length=100, description="Court division")
    region: Optional[str] = Field(None, max_length=50, description="Region or jurisdiction")
    status: JudgeStatus = Field(default=JudgeStatus.active, description="Current status of the judge")
    bio: Optional[str] = Field(None, description="Brief biography or background")
    appointment_date: Optional[datetime] = Field(None, description="Date of appointment")
    retirement_date: Optional[datetime] = Field(None, description="Date of retirement")
    contact_info: Optional[str] = Field(None, description="Contact information")
    specializations: Optional[str] = Field(None, description="Areas of law expertise")

class JudgeCreate(JudgeBase):
    pass

class JudgeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    title: Optional[str] = Field(None, max_length=100)
    court_type: Optional[str] = Field(None, max_length=50)
    court_division: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=50)
    status: Optional[JudgeStatus] = None
    bio: Optional[str] = None
    appointment_date: Optional[datetime] = None
    retirement_date: Optional[datetime] = None
    contact_info: Optional[str] = None
    specializations: Optional[str] = None
    is_active: Optional[bool] = None

class JudgeResponse(JudgeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

class JudgeListResponse(BaseModel):
    judges: List[JudgeResponse]
    total: int
    page: int
    limit: int
    total_pages: int
