from fastapi import APIRouter, Depends, HTTPException
from typing import List
from loguru import logger

from services.review_service import get_reviews
from services.auth_service import get_current_active_user
from models.review_models import Review
from models.auth_models import User

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/{domain}", response_model=List[Review])
async def get_reviews_endpoint(domain: str, current_user: User = Depends(get_current_active_user)):
    """Get reviews for a specific company domain"""
    logger.info(f"📖 Reviews request from user '{current_user.username}' for domain: {domain}")
    reviews = get_reviews(domain, current_user.username)
    logger.info(f"📊 Returned {len(reviews)} reviews for domain '{domain}' to user '{current_user.username}'")
    return reviews
