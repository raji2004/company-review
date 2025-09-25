from fastapi import HTTPException
from typing import List

from utils import search_companies as search_companies_api, read_json_file, write_json_file
from config import settings
from models.company_models import Company, TrackedCompany
from datetime import datetime

def search_companies(query: str) -> List[Company]:
    """Search for companies using the Trustpilot API"""
    return search_companies_api(query)

def track_company(company: Company, username: str) -> TrackedCompany:
    """Add a company to tracking list"""
    tracked_companies = read_json_file(settings.TRACKED_COMPANIES_FILE)
    
    # Check if company is already tracked by this user
    if any(tc["domain"] == company.domain and tc["user"] == username for tc in tracked_companies):
        raise HTTPException(status_code=400, detail="Company already tracked")
    
    tracked_company = TrackedCompany(
        domain=company.domain,
        name=company.name,
        added_at=datetime.now(),
        user=username
    )
    
    tracked_companies.append(tracked_company.dict())
    write_json_file(settings.TRACKED_COMPANIES_FILE, tracked_companies)
    
    return tracked_company

def get_tracked_companies(username: str) -> List[TrackedCompany]:
    """Get all tracked companies for a specific user"""
    tracked_companies = read_json_file(settings.TRACKED_COMPANIES_FILE)
    user_tracked = [TrackedCompany(**tc) for tc in tracked_companies if tc["user"] == username]
    return user_tracked
