from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.companies import Companies
from models.company_analytics import CompanyAnalytics
from models.company_case_statistics import CompanyCaseStatistics
from schemas.admin import CompanyCreateRequest, CompanyUpdateRequest
from typing import List, Optional
import math
import json

router = APIRouter()

@router.get("/stats")
async def get_companies_stats(db: Session = Depends(get_db)):
    """Get comprehensive company statistics for admin dashboard"""
    try:
        # Basic counts
        total_companies = db.query(Companies).count()
        
        # Financial analysis
        total_revenue = 0
        revenue_data = db.query(Companies.annual_revenue).filter(Companies.annual_revenue.isnot(None)).all()
        for revenue in revenue_data:
            try:
                if revenue[0]:
                    # Convert to string, remove commas and other characters, then convert to float
                    clean_revenue = str(revenue[0]).replace(',', '').replace('$', '').replace(' ', '')
                    if clean_revenue.replace('.', '').replace('-', '').isdigit():
                        total_revenue += float(clean_revenue)
            except (ValueError, TypeError):
                continue
        
        total_employees = 0
        employee_data = db.query(Companies.employee_count).filter(Companies.employee_count.isnot(None)).all()
        for employees in employee_data:
            try:
                if employees[0]:
                    # Convert to string, remove commas, then convert to int
                    clean_employees = str(employees[0]).replace(',', '').replace(' ', '')
                    if clean_employees.isdigit():
                        total_employees += int(clean_employees)
            except (ValueError, TypeError):
                continue
        
        # Average rating
        avg_rating = 0
        rating_data = db.query(Companies.rating).filter(Companies.rating.isnot(None)).all()
        if rating_data:
            valid_ratings = []
            for rating in rating_data:
                try:
                    if rating[0] is not None:
                        clean_rating = str(rating[0]).replace(',', '').replace(' ', '')
                        if clean_rating.replace('.', '').isdigit():
                            valid_ratings.append(float(clean_rating))
                except (ValueError, TypeError):
                    continue
            avg_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0
        
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
        # Get total count first
        total = db.query(Companies).count()
        print(f"Debug: Total companies in database: {total}")
        
        # Simple query to test - get first few companies
        companies = db.query(Companies).limit(10).all()
        print(f"Debug: Query returned {len(companies)} companies")
        
        if companies:
            print(f"Debug: First company: {companies[0].name if hasattr(companies[0], 'name') else 'No name'}")
            print(f"Debug: First company type: {type(companies[0])}")
            if hasattr(companies[0], '__dict__'):
                print(f"Debug: First company dict keys: {list(companies[0].__dict__.keys())[:10]}")
        else:
            print("Debug: No companies returned from query")
            
        # Apply pagination manually
        offset = (page - 1) * limit
        companies = companies[offset:offset + limit]
        print(f"Debug: After pagination: {len(companies)} companies")
        
        # Convert SQLAlchemy objects to dictionaries and handle data conversion
        formatted_companies = []
        for company in companies:
            try:
                # Convert SQLAlchemy object to dict
                company_dict = {}
                for column in company.__table__.columns:
                    value = getattr(company, column.name)
                    company_dict[column.name] = value
                
                # Convert JSON arrays to comma-separated strings
                if company_dict.get('business_activities'):
                    if isinstance(company_dict['business_activities'], list):
                        company_dict['business_activities'] = ', '.join(str(item) for item in company_dict['business_activities'])
                    elif isinstance(company_dict['business_activities'], str):
                        try:
                            data = json.loads(company_dict['business_activities'])
                            if isinstance(data, list):
                                company_dict['business_activities'] = ', '.join(str(item) for item in data)
                        except:
                            pass
                else:
                    company_dict['business_activities'] = ''
                    
                if company_dict.get('directors') and company_dict['directors'] is not None:
                    if isinstance(company_dict['directors'], list):
                        # Convert list of dicts to comma-separated names
                        director_names = []
                        for director in company_dict['directors']:
                            if isinstance(director, dict) and 'name' in director:
                                director_names.append(director['name'])
                            elif isinstance(director, str):
                                director_names.append(director)
                        company_dict['directors'] = ', '.join(director_names) if director_names else ''
                    elif isinstance(company_dict['directors'], str):
                        try:
                            data = json.loads(company_dict['directors'])
                            if isinstance(data, list):
                                director_names = []
                                for director in data:
                                    if isinstance(director, dict) and 'name' in director:
                                        director_names.append(director['name'])
                                    elif isinstance(director, str):
                                        director_names.append(director)
                                company_dict['directors'] = ', '.join(director_names) if director_names else ''
                        except:
                            pass
                else:
                    company_dict['directors'] = ''
                    
                if company_dict.get('secretary'):
                    if isinstance(company_dict['secretary'], dict):
                        company_dict['secretary'] = company_dict['secretary'].get('name', '')
                    elif isinstance(company_dict['secretary'], str):
                        try:
                            import json
                            data = json.loads(company_dict['secretary'])
                            if isinstance(data, dict) and 'name' in data:
                                company_dict['secretary'] = data['name']
                        except:
                            pass
                else:
                    company_dict['secretary'] = ''
                    
                if company_dict.get('auditor'):
                    if isinstance(company_dict['auditor'], dict):
                        company_dict['auditor'] = company_dict['auditor'].get('name', '')
                    elif isinstance(company_dict['auditor'], str):
                        try:
                            import json
                            data = json.loads(company_dict['auditor'])
                            if isinstance(data, dict) and 'name' in data:
                                company_dict['auditor'] = data['name']
                        except:
                            pass
                else:
                    company_dict['auditor'] = ''
                    
                # Convert rating from string to number if possible
                if company_dict.get('rating'):
                    try:
                        # Try to convert rating to float
                        rating_str = str(company_dict['rating'])
                        if rating_str.replace('.', '').replace('-', '').isdigit():
                            company_dict['rating'] = float(rating_str)
                        else:
                            # Handle letter grades like 'A+', 'A', etc.
                            rating_map = {'A+': 4.3, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}
                            company_dict['rating'] = rating_map.get(rating_str, 0.0)
                    except (ValueError, TypeError):
                        company_dict['rating'] = 0.0
                else:
                    company_dict['rating'] = 0.0
                
                formatted_companies.append(company_dict)
                print(f"Processed company: {company_dict.get('name', 'No name')} - business_activities: {company_dict.get('business_activities', 'None')}")
                
            except Exception as e:
                print(f"Error processing company: {e}")
                continue
        
        # Calculate total pages
        total_pages = math.ceil(total / limit)
        
        return {
            "companies": formatted_companies,
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
        
        # Convert company data for API response
        company_dict = company.__dict__.copy()
        
        # Convert JSON arrays to comma-separated strings
        if company_dict.get('business_activities') and isinstance(company_dict['business_activities'], list):
            company_dict['business_activities'] = ', '.join(company_dict['business_activities']) if company_dict['business_activities'] else ''
        elif company_dict.get('business_activities') is None or company_dict.get('business_activities') == []:
            company_dict['business_activities'] = ''
            
        if company_dict.get('directors') and isinstance(company_dict['directors'], list):
            # Convert list of dicts to comma-separated names
            director_names = []
            for director in company_dict['directors']:
                if isinstance(director, dict) and 'name' in director:
                    director_names.append(director['name'])
            company_dict['directors'] = ', '.join(director_names) if director_names else ''
        elif company_dict.get('directors') is None or company_dict.get('directors') == []:
            company_dict['directors'] = ''
            
        if company_dict.get('secretary') and isinstance(company_dict['secretary'], dict):
            company_dict['secretary'] = company_dict['secretary'].get('name', '') if company_dict['secretary'] else ''
        elif company_dict.get('secretary') is None:
            company_dict['secretary'] = ''
            
        if company_dict.get('auditor') and isinstance(company_dict['auditor'], dict):
            company_dict['auditor'] = company_dict['auditor'].get('name', '') if company_dict['auditor'] else ''
        elif company_dict.get('auditor') is None:
            company_dict['auditor'] = ''
            
        # Convert rating from string to number if possible
        if company_dict.get('rating'):
            try:
                # Try to convert rating to float
                rating_str = str(company_dict['rating'])
                if rating_str.replace('.', '').replace('-', '').isdigit():
                    company_dict['rating'] = float(rating_str)
                else:
                    # Handle letter grades like 'A+', 'A', etc.
                    rating_map = {'A+': 4.3, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}
                    company_dict['rating'] = rating_map.get(rating_str, 0.0)
            except (ValueError, TypeError):
                company_dict['rating'] = 0.0
        else:
            company_dict['rating'] = 0.0
        
        # Remove SQLAlchemy internal attributes
        company_dict.pop('_sa_instance_state', None)
        
        return {
            "company": company_dict,
            "analytics": analytics,
            "case_statistics": case_stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company: {str(e)}")

@router.post("/")
async def create_company(company_data: CompanyCreateRequest, db: Session = Depends(get_db)):
    """Create a new company"""
    try:
        # Convert comma-separated strings to JSON arrays for storage
        company_dict = company_data.dict()
        
        # Convert string fields to JSON arrays/objects
        if company_dict.get('business_activities'):
            company_dict['business_activities'] = [activity.strip() for activity in company_dict['business_activities'].split(',') if activity.strip()]
        else:
            company_dict['business_activities'] = []
            
        if company_dict.get('directors'):
            # Convert comma-separated names to list of dicts
            director_names = [name.strip() for name in company_dict['directors'].split(',') if name.strip()]
            company_dict['directors'] = [{'name': name, 'id_number': f'P{str(i).zfill(9)}'} for i, name in enumerate(director_names, 1)]
        else:
            company_dict['directors'] = []
            
        if company_dict.get('secretary'):
            company_dict['secretary'] = {'name': company_dict['secretary'], 'id_number': f'P{str(1).zfill(9)}'}
        else:
            company_dict['secretary'] = {}
            
        if company_dict.get('auditor'):
            company_dict['auditor'] = {'name': company_dict['auditor'], 'id_number': f'C{str(1).zfill(9)}'}
        else:
            company_dict['auditor'] = {}
        
        # Create the company
        company = Companies(**company_dict)
        db.add(company)
        db.commit()
        db.refresh(company)
        
        return {"message": "Company created successfully", "company_id": company.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating company: {str(e)}")

@router.put("/{company_id}")
async def update_company(company_id: int, company_data: CompanyUpdateRequest, db: Session = Depends(get_db)):
    """Update an existing company"""
    try:
        company = db.query(Companies).filter(Companies.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Convert comma-separated strings to JSON arrays for storage
        update_data = company_data.dict(exclude_unset=True)
        
        # Convert string fields to JSON arrays/objects
        if 'business_activities' in update_data and update_data['business_activities']:
            update_data['business_activities'] = [activity.strip() for activity in update_data['business_activities'].split(',') if activity.strip()]
        elif 'business_activities' in update_data and not update_data['business_activities']:
            update_data['business_activities'] = []
            
        if 'directors' in update_data and update_data['directors']:
            # Convert comma-separated names to list of dicts
            director_names = [name.strip() for name in update_data['directors'].split(',') if name.strip()]
            update_data['directors'] = [{'name': name, 'id_number': f'P{str(i).zfill(9)}'} for i, name in enumerate(director_names, 1)]
        elif 'directors' in update_data and not update_data['directors']:
            update_data['directors'] = []
            
        if 'secretary' in update_data and update_data['secretary']:
            update_data['secretary'] = {'name': update_data['secretary'], 'id_number': f'P{str(1).zfill(9)}'}
        elif 'secretary' in update_data and not update_data['secretary']:
            update_data['secretary'] = {}
            
        if 'auditor' in update_data and update_data['auditor']:
            update_data['auditor'] = {'name': update_data['auditor'], 'id_number': f'C{str(1).zfill(9)}'}
        elif 'auditor' in update_data and not update_data['auditor']:
            update_data['auditor'] = {}
        
        # Update the company
        for field, value in update_data.items():
            setattr(company, field, value)
        
        db.commit()
        db.refresh(company)
        
        return {"message": "Company updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating company: {str(e)}")

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
