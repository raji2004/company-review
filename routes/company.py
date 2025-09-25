from fastapi import APIRouter, Depends, HTTPException
from typing import List
from loguru import logger

from services.company_service import search_companies, track_company, get_tracked_companies
from services.auth_service import get_current_active_user
from models.company_models import Company, TrackedCompany
from models.auth_models import User

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("/search", response_model=List[Company])
async def search_companies_endpoint(query: str, current_user: User = Depends(get_current_active_user)):
    """Search for companies by query"""
    logger.info(f"🔍 Company search request from user '{current_user.username}': '{query}'")
    companies = search_companies(query)
    logger.info(f"📊 Found {len(companies)} companies for query: '{query}'")
    return companies

@router.post("/track", response_model=TrackedCompany)
async def track_company_endpoint(company: Company, current_user: User = Depends(get_current_active_user)):
    """Add a company to tracking list"""
    logger.info(f"➕ Tracking request from user '{current_user.username}' for company: {company.name} ({company.domain})")
    tracked_company = track_company(company, current_user.username)
    logger.success(f"✅ Successfully added company '{tracked_company.name}' to tracking for user '{current_user.username}'")
    return tracked_company

@router.get("/tracked", response_model=List[TrackedCompany])
async def get_tracked_companies_endpoint(current_user: User = Depends(get_current_active_user)):
    """Get all tracked companies for the current user"""
    logger.info(f"📋 Request for tracked companies from user: '{current_user.username}'")
    tracked_companies = get_tracked_companies(current_user.username)
    logger.info(f"📊 User '{current_user.username}' has {len(tracked_companies)} tracked companies")
    return tracked_companies
