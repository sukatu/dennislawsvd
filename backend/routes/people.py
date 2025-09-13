from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from database import get_db
from models.people import People
from models.user import User
from models.person_case_statistics import PersonCaseStatistics
from schemas.people import (
    PeopleCreate, 
    PeopleUpdate, 
    PeopleResponse, 
    PeopleSearchRequest, 
    PeopleSearchResponse,
    PeopleStats
)
from auth import get_current_user
from typing import List, Optional
import logging
import math

router = APIRouter()

@router.get("/search", response_model=PeopleSearchResponse)
async def search_people(
    query: Optional[str] = Query(None, description="General search query"),
    first_name: Optional[str] = Query(None, description="First name filter"),
    last_name: Optional[str] = Query(None, description="Last name filter"),
    id_number: Optional[str] = Query(None, description="ID number filter"),
    phone_number: Optional[str] = Query(None, description="Phone number filter"),
    email: Optional[str] = Query(None, description="Email filter"),
    city: Optional[str] = Query(None, description="City filter"),
    region: Optional[str] = Query(None, description="Region filter"),
    risk_level: Optional[str] = Query(None, description="Risk level filter"),
    occupation: Optional[str] = Query(None, description="Occupation filter"),
    employer: Optional[str] = Query(None, description="Employer filter"),
    organization: Optional[str] = Query(None, description="Organization filter"),
    gender: Optional[str] = Query(None, description="Gender filter"),
    nationality: Optional[str] = Query(None, description="Nationality filter"),
    is_verified: Optional[bool] = Query(None, description="Verification status filter"),
    status: Optional[str] = Query(None, description="Status filter"),
    min_risk_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum risk score"),
    max_risk_score: Optional[float] = Query(None, ge=0, le=100, description="Maximum risk score"),
    min_case_count: Optional[int] = Query(None, ge=0, description="Minimum case count"),
    max_case_count: Optional[int] = Query(None, ge=0, description="Maximum case count"),
    sort_by: str = Query("full_name", description="Sort field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    # current_user: User = Depends(get_current_user),  # Temporarily disabled for testing
    db: Session = Depends(get_db)
):
    """Search for people with various filters"""
    try:
        # Build query with case statistics join
        query_obj = db.query(People).outerjoin(
            PersonCaseStatistics, 
            People.id == PersonCaseStatistics.person_id
        )
        
        # Apply filters
        filters = []
        
        if query:
            # General search across multiple fields
            search_term = f"%{query.lower()}%"
            filters.append(
                or_(
                    func.lower(People.full_name).like(search_term),
                    func.lower(People.first_name).like(search_term),
                    func.lower(People.last_name).like(search_term),
                    func.lower(People.id_number).like(search_term),
                    func.lower(People.phone_number).like(search_term),
                    func.lower(People.email).like(search_term),
                    func.lower(People.address).like(search_term),
                    func.lower(People.city).like(search_term),
                    func.lower(People.region).like(search_term),
                    func.lower(People.occupation).like(search_term),
                    func.lower(People.employer).like(search_term),
                    func.lower(People.organization).like(search_term)
                )
            )
        
        if first_name:
            filters.append(func.lower(People.first_name).like(f"%{first_name.lower()}%"))
        if last_name:
            filters.append(func.lower(People.last_name).like(f"%{last_name.lower()}%"))
        if id_number:
            filters.append(People.id_number.ilike(f"%{id_number}%"))
        if phone_number:
            filters.append(People.phone_number.ilike(f"%{phone_number}%"))
        if email:
            filters.append(func.lower(People.email).like(f"%{email.lower()}%"))
        if city:
            filters.append(func.lower(People.city).like(f"%{city.lower()}%"))
        if region:
            filters.append(func.lower(People.region).like(f"%{region.lower()}%"))
        if risk_level:
            filters.append(People.risk_level == risk_level)
        if occupation:
            filters.append(func.lower(People.occupation).like(f"%{occupation.lower()}%"))
        if employer:
            filters.append(func.lower(People.employer).like(f"%{employer.lower()}%"))
        if organization:
            filters.append(func.lower(People.organization).like(f"%{organization.lower()}%"))
        if gender:
            filters.append(People.gender == gender)
        if nationality:
            filters.append(func.lower(People.nationality).like(f"%{nationality.lower()}%"))
        if is_verified is not None:
            filters.append(People.is_verified == is_verified)
        if status:
            filters.append(People.status == status)
        if min_risk_score is not None:
            filters.append(People.risk_score >= min_risk_score)
        if max_risk_score is not None:
            filters.append(People.risk_score <= max_risk_score)
        if min_case_count is not None:
            filters.append(People.case_count >= min_case_count)
        if max_case_count is not None:
            filters.append(People.case_count <= max_case_count)
        
        # Apply all filters
        if filters:
            query_obj = query_obj.filter(and_(*filters))
        
        # Apply sorting
        sort_column = getattr(People, sort_by, People.full_name)
        if sort_order == "desc":
            query_obj = query_obj.order_by(desc(sort_column))
        else:
            query_obj = query_obj.order_by(asc(sort_column))
        
        # Get total count
        total = query_obj.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        people = query_obj.offset(offset).limit(limit).all()
        
        # Calculate pagination info
        total_pages = math.ceil(total / limit)
        has_next = page < total_pages
        has_prev = page > 1
        
        # Update search count for each person and add case statistics
        for person in people:
            if person.search_count is None:
                person.search_count = 0
            person.search_count += 1
            person.last_searched = func.now()
            
            # Add case statistics if available
            if hasattr(person, 'case_statistics') and person.case_statistics:
                stats = person.case_statistics
                person.total_cases = stats.total_cases
                person.resolved_cases = stats.resolved_cases
                person.unresolved_cases = stats.unresolved_cases
                person.favorable_cases = stats.favorable_cases
                person.unfavorable_cases = stats.unfavorable_cases
                person.mixed_cases = stats.mixed_cases
                person.case_outcome = stats.case_outcome
            else:
                # Default values if no statistics available
                person.total_cases = 0
                person.resolved_cases = 0
                person.unresolved_cases = 0
                person.favorable_cases = 0
                person.unfavorable_cases = 0
                person.mixed_cases = 0
                person.case_outcome = "N/A"
        
        db.commit()
        
        return PeopleSearchResponse(
            people=people,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        logging.error(f"Error searching people: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search people"
        )

@router.get("/{people_id}", response_model=PeopleResponse)
async def get_person(
    people_id: int,
    # current_user: User = Depends(get_current_user),  # Temporarily disabled for testing
    db: Session = Depends(get_db)
):
    """Get a specific person by ID"""
    try:
        person = db.query(People).filter(People.id == people_id).first()
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
        # Update search count
        person.search_count += 1
        person.last_searched = func.now()
        db.commit()
        
        return person
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting person: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve person"
        )

@router.post("/", response_model=PeopleResponse)
async def create_person(
    person_data: PeopleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new person record"""
    try:
        # Create full name if not provided
        if not person_data.full_name:
            person_data.full_name = f"{person_data.first_name} {person_data.last_name}"
        
        person = People(
            **person_data.dict(),
            created_by=current_user.id
        )
        
        db.add(person)
        db.commit()
        db.refresh(person)
        
        return person
        
    except Exception as e:
        logging.error(f"Error creating person: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create person"
        )

@router.put("/{people_id}", response_model=PeopleResponse)
async def update_person(
    people_id: int,
    person_data: PeopleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a person record"""
    try:
        person = db.query(People).filter(People.id == people_id).first()
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
        # Update only provided fields
        update_data = person_data.dict(exclude_unset=True)
        
        # Update full name if first_name or last_name changed
        if "first_name" in update_data or "last_name" in update_data:
            first_name = update_data.get("first_name", person.first_name)
            last_name = update_data.get("last_name", person.last_name)
            update_data["full_name"] = f"{first_name} {last_name}"
        
        for field, value in update_data.items():
            if hasattr(person, field):
                setattr(person, field, value)
        
        person.updated_by = current_user.id
        db.commit()
        db.refresh(person)
        
        return person
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating person: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update person"
        )

@router.delete("/{people_id}")
async def delete_person(
    people_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a person record (soft delete)"""
    try:
        person = db.query(People).filter(People.id == people_id).first()
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
        # Soft delete by changing status
        person.status = "archived"
        person.updated_by = current_user.id
        db.commit()
        
        return {"message": "Person deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting person: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete person"
        )

@router.get("/stats/overview", response_model=PeopleStats)
async def get_people_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get people statistics overview"""
    try:
        # Total people
        total_people = db.query(People).filter(People.status == "active").count()
        
        # Verified people
        verified_people = db.query(People).filter(
            and_(People.status == "active", People.is_verified == True)
        ).count()
        
        # Risk level breakdown
        high_risk = db.query(People).filter(
            and_(People.status == "active", People.risk_level == "High")
        ).count()
        
        medium_risk = db.query(People).filter(
            and_(People.status == "active", People.risk_level == "Medium")
        ).count()
        
        low_risk = db.query(People).filter(
            and_(People.status == "active", People.risk_level == "Low")
        ).count()
        
        # People with cases
        people_with_cases = db.query(People).filter(
            and_(People.status == "active", People.case_count > 0)
        ).count()
        
        # People by region
        region_stats = db.query(
            People.region, func.count(People.id)
        ).filter(People.status == "active").group_by(People.region).all()
        people_by_region = {region or "Unknown": count for region, count in region_stats}
        
        # People by occupation
        occupation_stats = db.query(
            People.occupation, func.count(People.id)
        ).filter(
            and_(People.status == "active", People.occupation.isnot(None))
        ).group_by(People.occupation).all()
        people_by_occupation = {occupation: count for occupation, count in occupation_stats}
        
        # Recent searches (last 24 hours)
        recent_searches = db.query(People).filter(
            and_(
                People.status == "active",
                People.last_searched.isnot(None),
                People.last_searched >= func.now() - func.interval(1, 'day')
            )
        ).count()
        
        # Top searched people
        top_searched = db.query(
            People.full_name, People.search_count
        ).filter(People.status == "active").order_by(
            desc(People.search_count)
        ).limit(10).all()
        top_searched_list = [
            {"name": name, "search_count": count} 
            for name, count in top_searched
        ]
        
        return PeopleStats(
            total_people=total_people,
            verified_people=verified_people,
            high_risk_people=high_risk,
            medium_risk_people=medium_risk,
            low_risk_people=low_risk,
            people_with_cases=people_with_cases,
            people_by_region=people_by_region,
            people_by_occupation=people_by_occupation,
            recent_searches=recent_searches,
            top_searched=top_searched_list
        )
        
    except Exception as e:
        logging.error(f"Error getting people stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve people statistics"
        )
