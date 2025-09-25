from fastapi import HTTPException
from typing import List

from utils import get_company_reviews as get_company_reviews_api, read_json_file, write_json_file
from config import settings
from models.review_models import Review
from services.company_service import get_tracked_companies

def get_reviews(domain: str, username: str) -> List[Review]:
    """Get reviews for a specific company domain"""
    # Check if user is tracking this company
    tracked_companies = get_tracked_companies(username)
    if not any(tc.domain == domain for tc in tracked_companies):
        raise HTTPException(status_code=403, detail="Company not tracked by user")
    
    # Get reviews from storage first
    all_reviews = read_json_file(settings.REVIEWS_FILE)
    company_reviews = [Review(**r) for r in all_reviews if r["company_domain"] == domain]
    
    # If no reviews in storage, fetch from API
    if not company_reviews:
        company_reviews = get_company_reviews_api(domain)
        if company_reviews:
            # Save fetched reviews
            all_reviews.extend([r.dict() for r in company_reviews])
            write_json_file(settings.REVIEWS_FILE, all_reviews)
    
    return company_reviews
