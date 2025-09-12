from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc
from typing import Optional
import math

from database import get_db
from models.reported_cases import ReportedCases
from schemas.reported_cases import (
    ReportedCaseSearchRequest, 
    ReportedCaseSearchResponse, 
    ReportedCaseResponse,
    ReportedCaseDetailResponse
)
from auth import get_current_user

router = APIRouter()

@router.get("/search", response_model=ReportedCaseSearchResponse)
async def search_cases(
    query: Optional[str] = Query(None, description="Search query for title, antagonist, protagonist, or citation"),
    year: Optional[str] = Query(None, description="Filter by year"),
    court_type: Optional[str] = Query(None, description="Filter by court type (SC, CA, HC)"),
    region: Optional[str] = Query(None, description="Filter by region"),
    area_of_law: Optional[str] = Query(None, description="Filter by area of law"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    sort_by: str = Query("date", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Search reported cases with filters and pagination"""
    
    # Build query
    db_query = db.query(ReportedCases)
    
    # Apply filters
    if query:
        search_filter = or_(
            ReportedCases.title.ilike(f"%{query}%"),
            ReportedCases.antagonist.ilike(f"%{query}%"),
            ReportedCases.protagonist.ilike(f"%{query}%"),
            ReportedCases.citation.ilike(f"%{query}%"),
            ReportedCases.case_summary.ilike(f"%{query}%"),
            ReportedCases.keywords_phrases.ilike(f"%{query}%")
        )
        db_query = db_query.filter(search_filter)
    
    if year:
        db_query = db_query.filter(ReportedCases.year == year)
    
    if court_type:
        db_query = db_query.filter(ReportedCases.court_type == court_type)
    
    if region:
        db_query = db_query.filter(ReportedCases.region == region)
    
    if area_of_law:
        db_query = db_query.filter(ReportedCases.area_of_law.ilike(f"%{area_of_law}%"))
    
    # Get total count
    total = db_query.count()
    
    # Apply sorting
    if sort_by == "date":
        order_field = ReportedCases.date
    elif sort_by == "title":
        order_field = ReportedCases.title
    elif sort_by == "year":
        order_field = ReportedCases.year
    elif sort_by == "court_type":
        order_field = ReportedCases.court_type
    else:
        order_field = ReportedCases.date
    
    if sort_order == "desc":
        db_query = db_query.order_by(desc(order_field))
    else:
        db_query = db_query.order_by(asc(order_field))
    
    # Apply pagination
    offset = (page - 1) * limit
    cases = db_query.offset(offset).limit(limit).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / limit)
    
    return ReportedCaseSearchResponse(
        cases=cases,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )

@router.get("/{case_id}", response_model=ReportedCaseDetailResponse)
async def get_case_detail(
    case_id: int,
    db: Session = Depends(get_db)
    # Temporarily disabled authentication for testing
    # current_user = Depends(get_current_user)
):
    """Get detailed information about a specific case"""
    
    case = db.query(ReportedCases).filter(ReportedCases.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return case

@router.get("/", response_model=ReportedCaseSearchResponse)
async def get_recent_cases(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get recent cases with pagination"""
    
    # Get recent cases ordered by date
    db_query = db.query(ReportedCases).order_by(desc(ReportedCases.date))
    
    # Get total count
    total = db_query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    cases = db_query.offset(offset).limit(limit).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / limit)
    
    return ReportedCaseSearchResponse(
        cases=cases,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )

@router.get("/stats/overview")
async def get_case_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get overview statistics of reported cases"""
    
    # Total cases
    total_cases = db.query(ReportedCases).count()
    
    from sqlalchemy import func
    
    # Cases by year (last 10 years)
    year_stats = db.query(ReportedCases.year, func.count(ReportedCases.id)).group_by(ReportedCases.year).order_by(desc(ReportedCases.year)).limit(10).all()
    
    # Cases by court type
    court_stats = db.query(ReportedCases.court_type, func.count(ReportedCases.id)).group_by(ReportedCases.court_type).all()
    
    # Cases by region
    region_stats = db.query(ReportedCases.region, func.count(ReportedCases.id)).group_by(ReportedCases.region).order_by(desc(func.count(ReportedCases.id))).limit(10).all()
    
    return {
        "total_cases": total_cases,
        "year_distribution": [{"year": year, "count": count} for year, count in year_stats],
        "court_distribution": [{"court_type": court_type or "Unknown", "count": count} for court_type, count in court_stats],
        "region_distribution": [{"region": region or "Unknown", "count": count} for region, count in region_stats]
    }
