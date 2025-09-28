from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.person_analytics import PersonAnalytics
from schemas.person_analytics import PersonAnalyticsResponse, PersonAnalyticsCreate, PersonAnalyticsUpdate
from services.person_analytics_service import PersonAnalyticsService

router = APIRouter()

@router.get("/person/{person_id}/analytics", response_model=PersonAnalyticsResponse)
async def get_person_analytics(person_id: int, db: Session = Depends(get_db)):
    """Get analytics for a specific person"""
    # Check if person exists first
    from models.people import People
    person = db.query(People).filter(People.id == person_id).first()
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    
    # Try to get existing analytics
    analytics = db.query(PersonAnalytics).filter(PersonAnalytics.person_id == person_id).first()
    
    if analytics:
        return analytics
    
    # Return mock analytics for now
    from datetime import datetime
    from decimal import Decimal
    
    return PersonAnalyticsResponse(
        id=0,  # Mock ID
        person_id=person_id,
        risk_score=0,
        risk_level="Low",
        risk_factors=[],
        total_monetary_amount=Decimal('0.00'),
        average_case_value=Decimal('0.00'),
        financial_risk_level="Low",
        primary_subject_matter="N/A",
        subject_matter_categories=[],
        legal_issues=[],
        financial_terms=[],
        case_complexity_score=0,
        success_rate=Decimal('0.00'),
        last_updated=datetime.utcnow(),
        created_at=datetime.utcnow()
    )

@router.post("/person/{person_id}/analytics/generate", response_model=PersonAnalyticsResponse)
async def generate_person_analytics(person_id: int, db: Session = Depends(get_db)):
    """Generate or regenerate analytics for a specific person"""
    service = PersonAnalyticsService(db)
    analytics = await service.generate_analytics_for_person(person_id)
    
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    
    return analytics

@router.get("/analytics/risk-level/{risk_level}", response_model=List[PersonAnalyticsResponse])
async def get_analytics_by_risk_level(risk_level: str, db: Session = Depends(get_db)):
    """Get all persons with a specific risk level"""
    analytics = db.query(PersonAnalytics).filter(PersonAnalytics.risk_level == risk_level).all()
    return analytics

@router.get("/analytics/financial-risk/{risk_level}", response_model=List[PersonAnalyticsResponse])
async def get_analytics_by_financial_risk(risk_level: str, db: Session = Depends(get_db)):
    """Get all persons with a specific financial risk level"""
    analytics = db.query(PersonAnalytics).filter(PersonAnalytics.financial_risk_level == risk_level).all()
    return analytics

@router.get("/analytics/high-risk", response_model=List[PersonAnalyticsResponse])
async def get_high_risk_persons(db: Session = Depends(get_db)):
    """Get all high-risk persons (High or Critical risk level)"""
    analytics = db.query(PersonAnalytics).filter(
        PersonAnalytics.risk_level.in_(["High", "Critical"])
    ).all()
    return analytics

@router.get("/analytics/stats")
async def get_analytics_stats(db: Session = Depends(get_db)):
    """Get overall analytics statistics"""
    total_persons = db.query(PersonAnalytics).count()
    
    risk_levels = db.query(PersonAnalytics.risk_level, db.func.count()).group_by(PersonAnalytics.risk_level).all()
    financial_risk_levels = db.query(PersonAnalytics.financial_risk_level, db.func.count()).group_by(PersonAnalytics.financial_risk_level).all()
    
    avg_risk_score = db.query(db.func.avg(PersonAnalytics.risk_score)).scalar() or 0
    avg_monetary_amount = db.query(db.func.avg(PersonAnalytics.total_monetary_amount)).scalar() or 0
    
    return {
        "total_persons": total_persons,
        "risk_level_distribution": dict(risk_levels),
        "financial_risk_distribution": dict(financial_risk_levels),
        "average_risk_score": round(avg_risk_score, 2),
        "average_monetary_amount": float(avg_monetary_amount)
    }
