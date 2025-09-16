from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.people import People
from models.person_analytics import PersonAnalytics
from models.person_case_statistics import PersonCaseStatistics
from schemas.admin import AdminStatsResponse
from typing import List, Optional
import math

router = APIRouter()

@router.get("/stats")
async def get_people_stats(db: Session = Depends(get_db)):
    """Get comprehensive people statistics for admin dashboard"""
    try:
        # Basic counts
        total_people = db.query(People).count()
        
        # Risk analysis
        high_risk_count = db.query(People).filter(People.risk_level.in_(['high', 'very high'])).count()
        verified_count = db.query(People).filter(People.is_verified == True).count()
        
        # Average risk score
        avg_risk_score = db.query(People.risk_score).filter(People.risk_score.isnot(None)).all()
        avg_risk_score = sum([score[0] for score in avg_risk_score]) / len(avg_risk_score) if avg_risk_score else 0
        
        # Recent activity (last 24 hours)
        from datetime import datetime, timedelta
        recent_people = db.query(People).filter(
            People.created_at >= datetime.now() - timedelta(days=1)
        ).count()
        
        return {
            "total_people": total_people,
            "high_risk_count": high_risk_count,
            "verified_count": verified_count,
            "avg_risk_score": avg_risk_score,
            "recent_people": recent_people,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching people stats: {str(e)}")

@router.get("/")
async def get_people(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get paginated list of people with optional filtering"""
    try:
        query = db.query(People)
        
        # Apply search filter
        if search:
            query = query.filter(
                People.full_name.ilike(f"%{search}%") |
                People.first_name.ilike(f"%{search}%") |
                People.last_name.ilike(f"%{search}%") |
                People.email.ilike(f"%{search}%")
            )
        
        # Apply risk level filter
        if risk_level:
            query = query.filter(People.risk_level == risk_level)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        people = query.offset(offset).limit(limit).all()
        
        # Calculate total pages
        total_pages = math.ceil(total / limit)
        
        return {
            "people": people,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching people: {str(e)}")

@router.get("/{person_id}")
async def get_person(person_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific person"""
    try:
        person = db.query(People).filter(People.id == person_id).first()
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        
        # Get analytics if available
        analytics = db.query(PersonAnalytics).filter(PersonAnalytics.person_id == person_id).first()
        case_stats = db.query(PersonCaseStatistics).filter(PersonCaseStatistics.person_id == person_id).first()
        
        return {
            "person": person,
            "analytics": analytics,
            "case_statistics": case_stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching person: {str(e)}")

@router.delete("/{person_id}")
async def delete_person(person_id: int, db: Session = Depends(get_db)):
    """Delete a person and all associated data"""
    try:
        person = db.query(People).filter(People.id == person_id).first()
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        
        # Delete associated analytics and statistics
        db.query(PersonAnalytics).filter(PersonAnalytics.person_id == person_id).delete()
        db.query(PersonCaseStatistics).filter(PersonCaseStatistics.person_id == person_id).delete()
        
        # Delete the person
        db.delete(person)
        db.commit()
        
        return {"message": "Person deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting person: {str(e)}")
