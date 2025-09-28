from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
from database import get_db
from models.companies import Companies
from models.company_analytics import CompanyAnalytics
from models.company_case_statistics import CompanyCaseStatistics
from services.company_analytics_service import CompanyAnalyticsService
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
            Companies.description.ilike(f"%{query}%")
        )
        db_query = db_query.filter(search_filter)
    
    # Get total count
    total = db_query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    companies = db_query.offset(offset).limit(limit).all()
    
    # Add analytics data to each company
    for company in companies:
        # Get analytics data
        analytics = db.query(CompanyAnalytics).filter(CompanyAnalytics.company_id == company.id).first()
        case_stats = db.query(CompanyCaseStatistics).filter(CompanyCaseStatistics.company_id == company.id).first()
        
        # Add analytics fields to company object
        company.total_cases = case_stats.total_cases if case_stats else 0
        company.risk_score = analytics.risk_score if analytics else 0
        company.risk_level = analytics.risk_level if analytics else 'Low'
        company.success_rate = float(analytics.success_rate) if analytics else 0.0
        company.analytics_available = analytics is not None
        company.case_statistics_available = case_stats is not None
    
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

@router.get("/{company_id}/analytics")
async def get_company_analytics(
    company_id: int,
    db: Session = Depends(get_db)
    # Temporarily removed authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """Get analytics for a specific company"""
    
    # Check if company exists
    company = db.query(Companies).filter(Companies.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Try to get existing analytics
    analytics = db.query(CompanyAnalytics).filter(CompanyAnalytics.company_id == company_id).first()
    
    if not analytics:
        # Generate analytics if not found
        analytics_service = CompanyAnalyticsService(db)
        analytics = analytics_service.generate_company_analytics(company_id)
        
        if not analytics:
            return {"message": "No analytics available for this company"}
    
    return {
        "company_id": company_id,
        "company_name": company.name,
        "risk_score": analytics.risk_score,
        "risk_level": analytics.risk_level,
        "risk_factors": analytics.risk_factors,
        "total_monetary_amount": float(analytics.total_monetary_amount),
        "average_case_value": float(analytics.average_case_value),
        "financial_risk_level": analytics.financial_risk_level,
        "primary_subject_matter": analytics.primary_subject_matter,
        "subject_matter_categories": analytics.subject_matter_categories,
        "legal_issues": analytics.legal_issues,
        "financial_terms": analytics.financial_terms,
        "regulatory_compliance_score": analytics.regulatory_compliance_score,
        "customer_dispute_rate": float(analytics.customer_dispute_rate),
        "operational_risk_score": analytics.operational_risk_score,
        "business_continuity_score": analytics.business_continuity_score,
        "market_risk_score": analytics.market_risk_score,
        "credit_risk_score": analytics.credit_risk_score,
        "reputation_risk_score": analytics.reputation_risk_score,
        "case_complexity_score": analytics.case_complexity_score,
        "success_rate": float(analytics.success_rate),
        "last_updated": analytics.last_updated.isoformat() if analytics.last_updated else None
    }

@router.get("/{company_id}/case-statistics")
async def get_company_case_statistics(
    company_id: int,
    db: Session = Depends(get_db)
    # Temporarily removed authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """Get case statistics for a specific company"""
    
    # Check if company exists
    company = db.query(Companies).filter(Companies.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Try to get existing case statistics
    case_stats = db.query(CompanyCaseStatistics).filter(CompanyCaseStatistics.company_id == company_id).first()
    
    if not case_stats:
        # Generate case statistics if not found
        analytics_service = CompanyAnalyticsService(db)
        case_stats = analytics_service.generate_company_case_statistics(company_id)
        
        if not case_stats:
            return {"message": "No case statistics available for this company"}
    
    return case_stats.to_dict()

@router.get("/{company_id}/related-cases")
async def get_company_related_cases(
    company_id: int,
    limit: int = Query(10, ge=1, le=50, description="Maximum related cases"),
    db: Session = Depends(get_db)
    # Temporarily removed authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """Get related cases for a specific company"""
    
    # Check if company exists
    company = db.query(Companies).filter(Companies.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Find cases related to this company
    from models.reported_cases import ReportedCases
    
    company_name = company.name.lower()
    short_name = company.short_name.lower() if company.short_name else ""
    
    # Create search terms
    search_terms = [company_name]
    if short_name and short_name != company_name:
        search_terms.append(short_name)
    
    # Build search conditions
    conditions = []
    for term in search_terms:
        conditions.extend([
            func.lower(ReportedCases.title).like(f"%{term}%"),
            func.lower(ReportedCases.protagonist).like(f"%{term}%"),
            func.lower(ReportedCases.antagonist).like(f"%{term}%")
        ])
    
    cases = db.query(ReportedCases).filter(
        or_(*conditions)
    ).limit(limit).all()
    
    # Format cases for API response
    def format_case_for_api(case):
        return {
            "id": case.id,
            "title": case.title or "N/A",
            "suit_reference_number": case.suit_reference_number or "N/A",
            "court_type": case.court_type or "N/A",
            "date": case.date.strftime("%Y-%m-%d") if case.date else "N/A",
            "area_of_law": case.area_of_law or "N/A",
            "ai_case_outcome": case.ai_case_outcome or "N/A",
            "case_summary": case.case_summary or "N/A",
            "protagonist": case.protagonist or "N/A",
            "antagonist": case.antagonist or "N/A",
            "presiding_judge": case.presiding_judge or "N/A",
            "lawyers": case.lawyers or "N/A",
            "year": case.year or "N/A",
            "region": case.region or "N/A",
            "town": case.town or "N/A"
        }
    
    return {
        "company_id": company_id,
        "company_name": company.name,
        "total_cases": len(cases),
        "cases": [format_case_for_api(case) for case in cases]
    }
