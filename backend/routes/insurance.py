from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from database import get_db
from models.insurance import Insurance
from models.user import User
from schemas.insurance import (
    InsuranceCreate, 
    InsuranceUpdate, 
    InsuranceResponse, 
    InsuranceSearchRequest, 
    InsuranceSearchResponse,
    InsuranceStats
)
from auth import get_current_user
from typing import List, Optional
import logging
import math

router = APIRouter()

@router.get("/search", response_model=InsuranceSearchResponse)
async def search_insurance(
    query: Optional[str] = Query(None, description="General search query"),
    name: Optional[str] = Query(None, description="Insurance name filter"),
    city: Optional[str] = Query(None, description="City filter"),
    region: Optional[str] = Query(None, description="Region filter"),
    insurance_type: Optional[str] = Query(None, description="Insurance type filter"),
    ownership_type: Optional[str] = Query(None, description="Ownership type filter"),
    has_mobile_app: Optional[bool] = Query(None, description="Has mobile app filter"),
    has_online_portal: Optional[bool] = Query(None, description="Has online portal filter"),
    has_online_claims: Optional[bool] = Query(None, description="Has online claims filter"),
    has_24_7_support: Optional[bool] = Query(None, description="Has 24/7 support filter"),
    rating: Optional[str] = Query(None, description="Rating filter"),
    target_market: Optional[str] = Query(None, description="Target market filter"),
    min_assets: Optional[float] = Query(None, description="Minimum assets filter"),
    max_assets: Optional[float] = Query(None, description="Maximum assets filter"),
    sort_by: str = Query("name", description="Sort by field"),
    sort_order: str = Query("asc", description="Sort order (asc/desc)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
    # Temporarily disabled authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """Search insurance companies with various filters"""
    
    # Build query
    db_query = db.query(Insurance).filter(Insurance.is_active == True)
    
    # Apply filters
    if query:
        search_term = f"%{query.lower()}%"
        db_query = db_query.filter(
            or_(
                func.lower(Insurance.name).like(search_term),
                func.lower(Insurance.short_name).like(search_term),
                func.lower(Insurance.license_number).like(search_term),
                func.lower(Insurance.city).like(search_term),
                func.lower(Insurance.region).like(search_term),
                func.lower(Insurance.description).like(search_term)
            )
        )
    
    if name:
        db_query = db_query.filter(func.lower(Insurance.name).like(f"%{name.lower()}%"))
    
    if city:
        db_query = db_query.filter(func.lower(Insurance.city).like(f"%{city.lower()}%"))
    
    if region:
        db_query = db_query.filter(func.lower(Insurance.region).like(f"%{region.lower()}%"))
    
    if insurance_type:
        db_query = db_query.filter(Insurance.insurance_type == insurance_type)
    
    if ownership_type:
        db_query = db_query.filter(Insurance.ownership_type == ownership_type)
    
    if has_mobile_app is not None:
        db_query = db_query.filter(Insurance.has_mobile_app == has_mobile_app)
    
    if has_online_portal is not None:
        db_query = db_query.filter(Insurance.has_online_portal == has_online_portal)
    
    if has_online_claims is not None:
        db_query = db_query.filter(Insurance.has_online_claims == has_online_claims)
    
    if has_24_7_support is not None:
        db_query = db_query.filter(Insurance.has_24_7_support == has_24_7_support)
    
    if rating:
        db_query = db_query.filter(Insurance.rating == rating)
    
    if target_market:
        db_query = db_query.filter(Insurance.target_market == target_market)
    
    if min_assets is not None:
        db_query = db_query.filter(Insurance.total_assets >= min_assets)
    
    if max_assets is not None:
        db_query = db_query.filter(Insurance.total_assets <= max_assets)
    
    # Get total count
    total = db_query.count()
    
    # Apply sorting
    if sort_order.lower() == "desc":
        if sort_by == "name":
            db_query = db_query.order_by(desc(Insurance.name))
        elif sort_by == "city":
            db_query = db_query.order_by(desc(Insurance.city))
        elif sort_by == "rating":
            db_query = db_query.order_by(desc(Insurance.rating))
        elif sort_by == "total_assets":
            db_query = db_query.order_by(desc(Insurance.total_assets))
        elif sort_by == "branches_count":
            db_query = db_query.order_by(desc(Insurance.branches_count))
        else:
            db_query = db_query.order_by(desc(Insurance.name))
    else:
        if sort_by == "name":
            db_query = db_query.order_by(asc(Insurance.name))
        elif sort_by == "city":
            db_query = db_query.order_by(asc(Insurance.city))
        elif sort_by == "rating":
            db_query = db_query.order_by(asc(Insurance.rating))
        elif sort_by == "total_assets":
            db_query = db_query.order_by(asc(Insurance.total_assets))
        elif sort_by == "branches_count":
            db_query = db_query.order_by(asc(Insurance.branches_count))
        else:
            db_query = db_query.order_by(asc(Insurance.name))
    
    # Apply pagination
    offset = (page - 1) * limit
    insurance_companies = db_query.offset(offset).limit(limit).all()
    
    # Update search count for each insurance company
    for insurance in insurance_companies:
        insurance.search_count += 1
        insurance.last_searched = func.now()
    
    db.commit()
    
    # Calculate pagination info
    total_pages = math.ceil(total / limit)
    has_next = page < total_pages
    has_prev = page > 1
    
    return InsuranceSearchResponse(
        insurance=insurance_companies,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        has_next=has_next,
        has_prev=has_prev
    )

@router.get("/", response_model=List[InsuranceResponse])
async def get_insurance(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all insurance companies"""
    insurance = db.query(Insurance).filter(Insurance.is_active == True).offset(skip).limit(limit).all()
    return insurance

@router.get("/{insurance_id}", response_model=InsuranceResponse)
async def get_insurance_company(
    insurance_id: int,
    db: Session = Depends(get_db)
    # Temporarily disabled authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """Get a specific insurance company by ID"""
    insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance company not found")
    return insurance

@router.post("/", response_model=InsuranceResponse)
async def create_insurance(
    insurance: InsuranceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new insurance company"""
    db_insurance = Insurance(**insurance.dict())
    db.add(db_insurance)
    db.commit()
    db.refresh(db_insurance)
    return db_insurance

@router.put("/{insurance_id}", response_model=InsuranceResponse)
async def update_insurance(
    insurance_id: int,
    insurance: InsuranceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an insurance company"""
    db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not db_insurance:
        raise HTTPException(status_code=404, detail="Insurance company not found")
    
    update_data = insurance.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_insurance, field, value)
    
    db.commit()
    db.refresh(db_insurance)
    return db_insurance

@router.delete("/{insurance_id}")
async def delete_insurance(
    insurance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an insurance company (soft delete)"""
    db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not db_insurance:
        raise HTTPException(status_code=404, detail="Insurance company not found")
    
    db_insurance.is_active = False
    db.commit()
    return {"message": "Insurance company deleted successfully"}

@router.get("/stats/overview", response_model=InsuranceStats)
async def get_insurance_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get insurance statistics"""
    
    total_insurance = db.query(Insurance).count()
    active_insurance = db.query(Insurance).filter(Insurance.is_active == True).count()
    
    # Insurance by type
    insurance_by_type = db.query(
        Insurance.insurance_type, 
        func.count(Insurance.id).label('count')
    ).filter(Insurance.is_active == True).group_by(Insurance.insurance_type).all()
    insurance_by_type_dict = {item.insurance_type or 'Unknown': item.count for item in insurance_by_type}
    
    # Insurance by region
    insurance_by_region = db.query(
        Insurance.region, 
        func.count(Insurance.id).label('count')
    ).filter(Insurance.is_active == True).group_by(Insurance.region).all()
    insurance_by_region_dict = {item.region or 'Unknown': item.count for item in insurance_by_region}
    
    # Insurance with mobile app
    insurance_with_mobile_app = db.query(Insurance).filter(
        Insurance.is_active == True,
        Insurance.has_mobile_app == True
    ).count()
    
    # Insurance with online portal
    insurance_with_online_portal = db.query(Insurance).filter(
        Insurance.is_active == True,
        Insurance.has_online_portal == True
    ).count()
    
    return InsuranceStats(
        total_insurance=total_insurance,
        active_insurance=active_insurance,
        insurance_by_type=insurance_by_type_dict,
        insurance_by_region=insurance_by_region_dict,
        insurance_with_mobile_app=insurance_with_mobile_app,
        insurance_with_online_portal=insurance_with_online_portal
    )
