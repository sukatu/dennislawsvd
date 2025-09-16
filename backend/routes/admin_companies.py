from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.companies import Companies
from models.company_analytics import CompanyAnalytics
from models.company_case_statistics import CompanyCaseStatistics
from typing import List, Optional
import math

router = APIRouter()

@router.get("/stats")
async def get_companies_stats(db: Session = Depends(get_db)):
    """Get comprehensive company statistics for admin dashboard"""
    try:
        # Basic counts
        total_companies = db.query(Companies).count()
        
        # Financial analysis
        total_revenue = db.query(Companies.annual_revenue).filter(Companies.annual_revenue.isnot(None)).all()
        total_revenue = sum([revenue[0] for revenue in total_revenue]) if total_revenue else 0
        
        total_employees = db.query(Companies.employee_count).filter(Companies.employee_count.isnot(None)).all()
        total_employees = sum([employees[0] for employees in total_employees]) if total_employees else 0
        
        # Average rating
        avg_rating = db.query(Companies.rating).filter(Companies.rating.isnot(None)).all()
        avg_rating = sum([rating[0] for rating in avg_rating]) / len(avg_rating) if avg_rating else 0
        
        # Active companies
        active_companies = db.query(Companies).filter(Companies.is_active == True).count()
        
        return {
            "total_companies": total_companies,
            "total_revenue": total_revenue,
            "total_employees": total_employees,
            "avg_rating": avg_rating,
            "active_companies": active_companies,
            "last_updated": db.query(Companies.updated_at).order_by(Companies.updated_at.desc()).first()[0].isoformat() if db.query(Companies.updated_at).first() else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching companies stats: {str(e)}")

@router.get("/")
async def get_companies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    company_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get paginated list of companies with optional filtering"""
    try:
        query = db.query(Companies)
        
        # Apply search filter
        if search:
            query = query.filter(
                Companies.name.ilike(f"%{search}%") |
                Companies.short_name.ilike(f"%{search}%") |
                Companies.email.ilike(f"%{search}%")
            )
        
        # Apply company type filter
        if company_type:
            query = query.filter(Companies.company_type == company_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        companies = query.offset(offset).limit(limit).all()
        
        # Calculate total pages
        total_pages = math.ceil(total / limit)
        
        return {
            "companies": companies,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching companies: {str(e)}")

@router.get("/{company_id}")
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific company"""
    try:
        company = db.query(Companies).filter(Companies.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Get analytics if available
        analytics = db.query(CompanyAnalytics).filter(CompanyAnalytics.company_id == company_id).first()
        case_stats = db.query(CompanyCaseStatistics).filter(CompanyCaseStatistics.company_id == company_id).first()
        
        return {
            "company": company,
            "analytics": analytics,
            "case_statistics": case_stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company: {str(e)}")

@router.delete("/{company_id}")
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete a company and all associated data"""
    try:
        company = db.query(Companies).filter(Companies.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Delete associated analytics and statistics
        db.query(CompanyAnalytics).filter(CompanyAnalytics.company_id == company_id).delete()
        db.query(CompanyCaseStatistics).filter(CompanyCaseStatistics.company_id == company_id).delete()
        
        # Delete the company
        db.delete(company)
        db.commit()
        
        return {"message": "Company deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting company: {str(e)}")
