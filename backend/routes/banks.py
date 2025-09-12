from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from database import get_db
from models.banks import Banks
from models.user import User
from schemas.banks import (
    BanksCreate, 
    BanksUpdate, 
    BanksResponse, 
    BanksSearchRequest, 
    BanksSearchResponse,
    BanksStats
)
from auth import get_current_user
from typing import List, Optional
import logging
import math

router = APIRouter()

@router.get("/search", response_model=BanksSearchResponse)
async def search_banks(
    query: Optional[str] = Query(None, description="General search query"),
    name: Optional[str] = Query(None, description="Bank name filter"),
    city: Optional[str] = Query(None, description="City filter"),
    region: Optional[str] = Query(None, description="Region filter"),
    bank_type: Optional[str] = Query(None, description="Bank type filter"),
    ownership_type: Optional[str] = Query(None, description="Ownership type filter"),
    has_mobile_app: Optional[bool] = Query(None, description="Has mobile app filter"),
    has_online_banking: Optional[bool] = Query(None, description="Has online banking filter"),
    has_atm_services: Optional[bool] = Query(None, description="Has ATM services filter"),
    has_foreign_exchange: Optional[bool] = Query(None, description="Has foreign exchange filter"),
    rating: Optional[str] = Query(None, description="Rating filter"),
    min_assets: Optional[float] = Query(None, description="Minimum assets filter"),
    max_assets: Optional[float] = Query(None, description="Maximum assets filter"),
    sort_by: str = Query("name", description="Sort by field"),
    sort_order: str = Query("asc", description="Sort order (asc/desc)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search banks with various filters"""
    
    # Build query
    db_query = db.query(Banks).filter(Banks.is_active == True)
    
    # Apply filters
    if query:
        search_term = f"%{query.lower()}%"
        db_query = db_query.filter(
            or_(
                func.lower(Banks.name).like(search_term),
                func.lower(Banks.short_name).like(search_term),
                func.lower(Banks.bank_code).like(search_term),
                func.lower(Banks.city).like(search_term),
                func.lower(Banks.region).like(search_term),
                func.lower(Banks.description).like(search_term)
            )
        )
    
    if name:
        db_query = db_query.filter(func.lower(Banks.name).like(f"%{name.lower()}%"))
    
    if city:
        db_query = db_query.filter(func.lower(Banks.city).like(f"%{city.lower()}%"))
    
    if region:
        db_query = db_query.filter(func.lower(Banks.region).like(f"%{region.lower()}%"))
    
    if bank_type:
        db_query = db_query.filter(Banks.bank_type == bank_type)
    
    if ownership_type:
        db_query = db_query.filter(Banks.ownership_type == ownership_type)
    
    if has_mobile_app is not None:
        db_query = db_query.filter(Banks.has_mobile_app == has_mobile_app)
    
    if has_online_banking is not None:
        db_query = db_query.filter(Banks.has_online_banking == has_online_banking)
    
    if has_atm_services is not None:
        db_query = db_query.filter(Banks.has_atm_services == has_atm_services)
    
    if has_foreign_exchange is not None:
        db_query = db_query.filter(Banks.has_foreign_exchange == has_foreign_exchange)
    
    if rating:
        db_query = db_query.filter(Banks.rating == rating)
    
    if min_assets is not None:
        db_query = db_query.filter(Banks.total_assets >= min_assets)
    
    if max_assets is not None:
        db_query = db_query.filter(Banks.total_assets <= max_assets)
    
    # Get total count
    total = db_query.count()
    
    # Apply sorting
    if sort_order.lower() == "desc":
        if sort_by == "name":
            db_query = db_query.order_by(desc(Banks.name))
        elif sort_by == "city":
            db_query = db_query.order_by(desc(Banks.city))
        elif sort_by == "rating":
            db_query = db_query.order_by(desc(Banks.rating))
        elif sort_by == "total_assets":
            db_query = db_query.order_by(desc(Banks.total_assets))
        elif sort_by == "branches_count":
            db_query = db_query.order_by(desc(Banks.branches_count))
        else:
            db_query = db_query.order_by(desc(Banks.name))
    else:
        if sort_by == "name":
            db_query = db_query.order_by(asc(Banks.name))
        elif sort_by == "city":
            db_query = db_query.order_by(asc(Banks.city))
        elif sort_by == "rating":
            db_query = db_query.order_by(asc(Banks.rating))
        elif sort_by == "total_assets":
            db_query = db_query.order_by(asc(Banks.total_assets))
        elif sort_by == "branches_count":
            db_query = db_query.order_by(asc(Banks.branches_count))
        else:
            db_query = db_query.order_by(asc(Banks.name))
    
    # Apply pagination
    offset = (page - 1) * limit
    banks = db_query.offset(offset).limit(limit).all()
    
    # Update search count for each bank
    for bank in banks:
        bank.search_count += 1
        bank.last_searched = func.now()
    
    db.commit()
    
    # Calculate pagination info
    total_pages = math.ceil(total / limit)
    has_next = page < total_pages
    has_prev = page > 1
    
    return BanksSearchResponse(
        banks=banks,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        has_next=has_next,
        has_prev=has_prev
    )

@router.get("/", response_model=List[BanksResponse])
async def get_banks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all banks"""
    banks = db.query(Banks).filter(Banks.is_active == True).offset(skip).limit(limit).all()
    return banks

@router.get("/{bank_id}", response_model=BanksResponse)
async def get_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific bank by ID"""
    bank = db.query(Banks).filter(Banks.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank

@router.post("/", response_model=BanksResponse)
async def create_bank(
    bank: BanksCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new bank"""
    db_bank = Banks(**bank.dict())
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

@router.put("/{bank_id}", response_model=BanksResponse)
async def update_bank(
    bank_id: int,
    bank: BanksUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a bank"""
    db_bank = db.query(Banks).filter(Banks.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    update_data = bank.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bank, field, value)
    
    db.commit()
    db.refresh(db_bank)
    return db_bank

@router.delete("/{bank_id}")
async def delete_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a bank (soft delete)"""
    db_bank = db.query(Banks).filter(Banks.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    db_bank.is_active = False
    db.commit()
    return {"message": "Bank deleted successfully"}

@router.get("/stats/overview", response_model=BanksStats)
async def get_banks_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get banks statistics"""
    
    total_banks = db.query(Banks).count()
    active_banks = db.query(Banks).filter(Banks.is_active == True).count()
    
    # Banks by type
    banks_by_type = db.query(
        Banks.bank_type, 
        func.count(Banks.id).label('count')
    ).filter(Banks.is_active == True).group_by(Banks.bank_type).all()
    banks_by_type_dict = {item.bank_type or 'Unknown': item.count for item in banks_by_type}
    
    # Banks by region
    banks_by_region = db.query(
        Banks.region, 
        func.count(Banks.id).label('count')
    ).filter(Banks.is_active == True).group_by(Banks.region).all()
    banks_by_region_dict = {item.region or 'Unknown': item.count for item in banks_by_region}
    
    # Banks with mobile app
    banks_with_mobile_app = db.query(Banks).filter(
        Banks.is_active == True,
        Banks.has_mobile_app == True
    ).count()
    
    # Banks with online banking
    banks_with_online_banking = db.query(Banks).filter(
        Banks.is_active == True,
        Banks.has_online_banking == True
    ).count()
    
    return BanksStats(
        total_banks=total_banks,
        active_banks=active_banks,
        banks_by_type=banks_by_type_dict,
        banks_by_region=banks_by_region_dict,
        banks_with_mobile_app=banks_with_mobile_app,
        banks_with_online_banking=banks_with_online_banking
    )
