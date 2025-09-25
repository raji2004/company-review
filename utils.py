import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import requests
from loguru import logger
from config import settings
from models.auth_models import UserInDB
from models.company_models import Company
from models.review_models import Review
from models.job_models import JobLog

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT token functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# Data storage functions
def ensure_data_dir():
    if not os.path.exists(settings.DATA_DIR):
        os.makedirs(settings.DATA_DIR)

def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    ensure_data_dir()
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_json_file(file_path: str, data: List[Dict[str, Any]]):
    ensure_data_dir()
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

# API call functions
def search_companies(query: str) -> List[Company]:
    headers = {
        "x-rapidapi-host": "trustpilot-company-and-reviews-data.p.rapidapi.com",
        "x-rapidapi-key": settings.RAPIDAPI_KEY
    }
    
    params = {"query": query}
    
    try:
        response = requests.get(settings.COMPANY_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        companies = []
        for company_data in data.get("data", {}).get("companies", []):
            company = Company(
                domain=company_data.get("domain", ""),
                name=company_data.get("name", ""),
                website=company_data.get("website", ""),
                trustscore=company_data.get("trust_score"),
                trustscore_category=company_data.get("trust_score"),
                number_of_reviews=company_data.get("review_count")
            )
            companies.append(company)
        
        return companies
    except requests.RequestException as e:
        logger.error(f"❌ Error searching companies: {e}")
        return []

def get_company_reviews(domain: str) -> List[Review]:
    headers = {
        "x-rapidapi-host": "trustpilot-company-and-reviews-data.p.rapidapi.com",
        "x-rapidapi-key": settings.RAPIDAPI_KEY
    }
    
    params = {"company_domain": domain}
    
    try:
        response = requests.get(settings.COMPANY_REVIEWS_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        reviews = []
        for review_data in data.get("data", {}).get("reviews", []):
            review = Review(
                id=review_data.get("review_id", ""),
                company_domain=domain,
                title=review_data.get("review_title", ""),
                content=review_data.get("review_text", ""),
                rating=review_data.get("review_rating", 0),
                date=datetime.fromisoformat(review_data.get("review_time", "1970-01-01T00:00:00").replace('Z', '+00:00')),
                author=review_data.get("consumer_name", "")
            )
            reviews.append(review)
        
        return reviews
    except requests.RequestException as e:
        logger.error(f"❌ Error fetching reviews for {domain}: {e}")
        return []
    except (ValueError, KeyError) as e:
        logger.error(f"❌ Error parsing reviews for {domain}: {e}")
        return []
