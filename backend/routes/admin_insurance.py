from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.insurance import Insurance
from models.insurance_analytics import InsuranceAnalytics
from models.insurance_case_statistics import InsuranceCaseStatistics
from typing import List, Optional
import math

router = APIRouter()

@router.get("/stats")
async def get_insurance_stats(db: Session = Depends(get_db)):
    """Get comprehensive insurance statistics for admin dashboard"""
    try:
        # Basic counts
        total_insurance = db.query(Insurance).count()
        
        # Financial analysis
        total_assets = db.query(Insurance.total_assets).filter(Insurance.total_assets.isnot(None)).all()
        total_assets = sum([assets[0] for assets in total_assets]) if total_assets else 0
        
        total_branches = db.query(Insurance.branches_count).filter(Insurance.branches_count.isnot(None)).all()
        total_branches = sum([branches[0] for branches in total_branches]) if total_branches else 0
        
        # Average rating
        avg_rating = db.query(Insurance.rating).filter(Insurance.rating.isnot(None)).all()
        avg_rating = sum([rating[0] for rating in avg_rating]) / len(avg_rating) if avg_rating else 0
        
        # Active insurance companies
        active_insurance = db.query(Insurance).filter(Insurance.is_active == True).count()
        
        return {
            "total_insurance": total_insurance,
            "total_assets": total_assets,
            "total_branches": total_branches,
            "avg_rating": avg_rating,
            "active_insurance": active_insurance,
            "last_updated": db.query(Insurance.updated_at).order_by(Insurance.updated_at.desc()).first()[0].isoformat() if db.query(Insurance.updated_at).first() else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insurance stats: {str(e)}")

@router.get("/")
async def get_insurance(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    insurance_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get paginated list of insurance companies with optional filtering"""
    try:
        query = db.query(Insurance)
        
        # Apply search filter
        if search:
            query = query.filter(
                Insurance.name.ilike(f"%{search}%") |
                Insurance.short_name.ilike(f"%{search}%") |
                Insurance.email.ilike(f"%{search}%")
            )
        
        # Apply insurance type filter
        if insurance_type:
            query = query.filter(Insurance.insurance_type == insurance_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        insurance = query.offset(offset).limit(limit).all()
        
        # Calculate total pages
        total_pages = math.ceil(total / limit)
        
        return {
            "insurance": insurance,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insurance: {str(e)}")

@router.get("/{insurance_id}")
async def get_insurance_company(insurance_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific insurance company"""
    try:
        insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not insurance:
            raise HTTPException(status_code=404, detail="Insurance company not found")
        
        # Get analytics if available
        analytics = db.query(InsuranceAnalytics).filter(InsuranceAnalytics.insurance_id == insurance_id).first()
        case_stats = db.query(InsuranceCaseStatistics).filter(InsuranceCaseStatistics.insurance_id == insurance_id).first()
        
        return {
            "insurance": insurance,
            "analytics": analytics,
            "case_statistics": case_stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insurance: {str(e)}")

@router.delete("/{insurance_id}")
async def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
    """Delete an insurance company and all associated data"""
    try:
        insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not insurance:
            raise HTTPException(status_code=404, detail="Insurance company not found")
        
        # Delete associated analytics and statistics
        db.query(InsuranceAnalytics).filter(InsuranceAnalytics.insurance_id == insurance_id).delete()
        db.query(InsuranceCaseStatistics).filter(InsuranceCaseStatistics.insurance_id == insurance_id).delete()
        
        # Delete the insurance company
        db.delete(insurance)
        db.commit()
        
        return {"message": "Insurance company deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting insurance: {str(e)}")
