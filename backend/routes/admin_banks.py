from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.banks import Banks
from models.bank_analytics import BankAnalytics
from models.bank_case_statistics import BankCaseStatistics
from typing import List, Optional
import math

router = APIRouter()

@router.get("/stats")
async def get_banks_stats(db: Session = Depends(get_db)):
    """Get comprehensive bank statistics for admin dashboard"""
    try:
        # Basic counts
        total_banks = db.query(Banks).count()
        
        # Financial analysis
        total_assets = db.query(Banks.total_assets).filter(Banks.total_assets.isnot(None)).all()
        total_assets = sum([assets[0] for assets in total_assets]) if total_assets else 0
        
        total_branches = db.query(Banks.branches_count).filter(Banks.branches_count.isnot(None)).all()
        total_branches = sum([branches[0] for branches in total_branches]) if total_branches else 0
        
        # Average rating
        avg_rating = db.query(Banks.rating).filter(Banks.rating.isnot(None)).all()
        avg_rating = sum([rating[0] for rating in avg_rating]) / len(avg_rating) if avg_rating else 0
        
        # Active banks
        active_banks = db.query(Banks).filter(Banks.is_active == True).count()
        
        return {
            "total_banks": total_banks,
            "total_assets": total_assets,
            "total_branches": total_branches,
            "avg_rating": avg_rating,
            "active_banks": active_banks,
            "last_updated": db.query(Banks.updated_at).order_by(Banks.updated_at.desc()).first()[0].isoformat() if db.query(Banks.updated_at).first() else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching banks stats: {str(e)}")

@router.get("/")
async def get_banks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    bank_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get paginated list of banks with optional filtering"""
    try:
        query = db.query(Banks)
        
        # Apply search filter
        if search:
            query = query.filter(
                Banks.name.ilike(f"%{search}%") |
                Banks.short_name.ilike(f"%{search}%") |
                Banks.email.ilike(f"%{search}%")
            )
        
        # Apply bank type filter
        if bank_type:
            query = query.filter(Banks.bank_type == bank_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        banks = query.offset(offset).limit(limit).all()
        
        # Calculate total pages
        total_pages = math.ceil(total / limit)
        
        return {
            "banks": banks,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching banks: {str(e)}")

@router.get("/{bank_id}")
async def get_bank(bank_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific bank"""
    try:
        bank = db.query(Banks).filter(Banks.id == bank_id).first()
        if not bank:
            raise HTTPException(status_code=404, detail="Bank not found")
        
        # Get analytics if available
        analytics = db.query(BankAnalytics).filter(BankAnalytics.bank_id == bank_id).first()
        case_stats = db.query(BankCaseStatistics).filter(BankCaseStatistics.bank_id == bank_id).first()
        
        return {
            "bank": bank,
            "analytics": analytics,
            "case_statistics": case_stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bank: {str(e)}")

@router.delete("/{bank_id}")
async def delete_bank(bank_id: int, db: Session = Depends(get_db)):
    """Delete a bank and all associated data"""
    try:
        bank = db.query(Banks).filter(Banks.id == bank_id).first()
        if not bank:
            raise HTTPException(status_code=404, detail="Bank not found")
        
        # Delete associated analytics and statistics
        db.query(BankAnalytics).filter(BankAnalytics.bank_id == bank_id).delete()
        db.query(BankCaseStatistics).filter(BankCaseStatistics.bank_id == bank_id).delete()
        
        # Delete the bank
        db.delete(bank)
        db.commit()
        
        return {"message": "Bank deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting bank: {str(e)}")
