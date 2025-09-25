import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "f087850b41mshb3c7794a5fe78b0p1006edjsn8cc54b6de0ef")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-here-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # API key loaded successfully
    
    # API endpoints
    COMPANY_SEARCH_URL = "https://trustpilot-company-and-reviews-data.p.rapidapi.com/company-search"
    COMPANY_REVIEWS_URL = "https://trustpilot-company-and-reviews-data.p.rapidapi.com/company-reviews"
    
    # Data storage paths
    DATA_DIR = "data"
    USERS_FILE = os.path.join(DATA_DIR, "users.json")
    TRACKED_COMPANIES_FILE = os.path.join(DATA_DIR, "tracked_companies.json")
    REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")
    LOGS_FILE = os.path.join(DATA_DIR, "job_logs.json")

    # Server settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")

settings = Settings()
