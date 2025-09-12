from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
from database import get_db
from models.companies import Companies
from schemas.companies import (
    CompaniesResponse, 
    CompaniesCreate, 
    CompaniesUpdate, 
    CompaniesSearchRequest, 
    CompaniesSearchResponse,
    CompaniesStats
)
from auth import get_current_user
from models.user import User

router = APIRouter()

@router.get("/", response_model=List[CompaniesResponse])
async def get_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all companies with pagination"""
    companies = db.query(Companies).offset(skip).limit(limit).all()
    return companies

@router.get("/search", response_model=CompaniesSearchResponse)
async def search_companies(
    query: Optional[str] = Query(None, description="Search term for company name, industry, or activities"),
    city: Optional[str] = Query(None, description="Filter by city"),
    region: Optional[str] = Query(None, description="Filter by region"),
    company_type: Optional[str] = Query(None, description="Filter by company type"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
    # Temporarily disabled authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """Search companies with filters and pagination"""
    
    # Build query
    db_query = db.query(Companies)
    
    # Apply filters
    if is_active is not None:
        db_query = db_query.filter(Companies.is_active == is_active)
    
    if city:
        db_query = db_query.filter(Companies.city.ilike(f"%{city}%"))
    
    if region:
        db_query = db_query.filter(Companies.region.ilike(f"%{region}%"))
    
    if company_type:
        db_query = db_query.filter(Companies.company_type.ilike(f"%{company_type}%"))
    
    if industry:
        db_query = db_query.filter(Companies.industry.ilike(f"%{industry}%"))
    
    # Apply search query
    if query:
        search_filter = or_(
            Companies.name.ilike(f"%{query}%"),
            Companies.short_name.ilike(f"%{query}%"),
            Companies.industry.ilike(f"%{query}%"),
            Companies.business_activities.like(f"%{query}%")
        )
        db_query = db_query.filter(search_filter)
    
    # Get total count
    total = db_query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    companies = db_query.offset(offset).limit(limit).all()
    
    # Calculate pagination info
    total_pages = (total + limit - 1) // limit
    has_next = page < total_pages
    has_prev = page > 1
    
    return CompaniesSearchResponse(
        results=companies,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        has_next=has_next,
        has_prev=has_prev
    )

@router.get("/{company_id}", response_model=CompaniesResponse)
async def get_company(
    company_id: int,
    db: Session = Depends(get_db)
    # Temporarily disabled authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """Get a specific company by ID"""
    company = db.query(Companies).filter(Companies.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Update search count and last searched
    if company.search_count is None:
        company.search_count = 0
    company.search_count += 1
    company.last_searched = func.now()
    db.commit()
    
    return company

@router.post("/", response_model=CompaniesResponse)
async def create_company(
    company: CompaniesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new company"""
    db_company = Companies(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.put("/{company_id}", response_model=CompaniesResponse)
async def update_company(
    company_id: int,
    company: CompaniesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a company"""
    db_company = db.query(Companies).filter(Companies.id == company_id).first()
    
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = company.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a company"""
    db_company = db.query(Companies).filter(Companies.id == company_id).first()
    
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}

@router.get("/stats/overview", response_model=CompaniesStats)
async def get_companies_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get companies statistics overview"""
    
    # Total companies
    total_companies = db.query(Companies).count()
    
    # Active companies
    active_companies = db.query(Companies).filter(Companies.is_active == True).count()
    
    # Verified companies
    verified_companies = db.query(Companies).filter(Companies.is_verified == True).count()
    
    # Companies by region
    region_stats = db.query(
        Companies.region, 
        func.count(Companies.id).label('count')
    ).group_by(Companies.region).all()
    companies_by_region = {region or 'Unknown': count for region, count in region_stats}
    
    # Companies by type
    type_stats = db.query(
        Companies.company_type, 
        func.count(Companies.id).label('count')
    ).group_by(Companies.company_type).all()
    companies_by_type = {company_type or 'Unknown': count for company_type, count in type_stats}
    
    # Companies by industry
    industry_stats = db.query(
        Companies.industry, 
        func.count(Companies.id).label('count')
    ).group_by(Companies.industry).all()
    companies_by_industry = {industry or 'Unknown': count for industry, count in industry_stats}
    
    return CompaniesStats(
        total_companies=total_companies,
        active_companies=active_companies,
        verified_companies=verified_companies,
        companies_by_region=companies_by_region,
        companies_by_type=companies_by_type,
        companies_by_industry=companies_by_industry
    )
