from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from services.auth_service import create_default_user
from services.job_service import fetch_reviews_for_tracked_companies
from routes.auth import router as auth_router
from routes.company import router as company_router
from routes.review import router as review_router
from config import settings

# Create logs directory if it doesn't exist
import os
os.makedirs("logs", exist_ok=True)

# Configure loguru logging
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    backtrace=True,
    diagnose=True
)

# Add console logger with emoji formatting
logger.add(
    lambda msg: print(msg, end=""),
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    colorize=True
)

# Background scheduler for automatic review fetching
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Company Review Monitor API")
    logger.info("📁 Data will be stored in JSON files in the 'data/' directory")

    create_default_user()
    logger.info("✅ Default user created: admin/admin123")

    scheduler.start()
    logger.info("⏰ Background scheduler started")

    # Schedule review fetching job every 5 minutes
    scheduler.add_job(
        fetch_reviews_for_tracked_companies,
        trigger=IntervalTrigger(minutes=5),
        id="review_fetcher",
        name="Fetch reviews for tracked companies every 5 minutes",
        replace_existing=True
    )
    logger.info("📊 Scheduled review fetching job to run every 5 minutes")

    yield

    # Shutdown
    logger.info("🛑 Shutting down Company Review Monitor API")
    scheduler.shutdown()
    logger.info("✅ Background scheduler stopped")

app = FastAPI(
    title="Company Review Monitor API",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth_router)
app.include_router(company_router)
app.include_router(review_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
