import uuid
from datetime import datetime
from typing import List
from loguru import logger

from utils import get_company_reviews, read_json_file, write_json_file
from config import settings
from models.job_models import JobLog
from models.review_models import Review

def fetch_reviews_for_tracked_companies():
    """Background job to fetch reviews for all tracked companies"""
    job_id = str(uuid.uuid4())
    job_log = JobLog(
        job_id=job_id,
        job_type="review_fetch",
        status="running",
        start_time=datetime.now(),
        companies_processed=0,
        reviews_fetched=0
    )

    logger.info(f"🚀 Starting background job {job_id} - Review fetching")
    logger.info("📊 Background job will fetch reviews for all tracked companies")

    # Read current logs and add new job
    logs = read_json_file(settings.LOGS_FILE)
    logs.append(job_log.dict())
    write_json_file(settings.LOGS_FILE, logs)

    try:
        tracked_companies = read_json_file(settings.TRACKED_COMPANIES_FILE)
        all_reviews = read_json_file(settings.REVIEWS_FILE)

        # Sort companies by added_at in descending order (newest first)
        tracked_companies.sort(key=lambda x: datetime.fromisoformat(x["added_at"]), reverse=True)

        logger.info(f"📈 Found {len(tracked_companies)} tracked companies")
        logger.info(f"📚 Found {len(all_reviews)} existing reviews in storage")
        logger.info("🔄 Processing companies in order of newest first (prioritizing recently added)")

        new_reviews_count = 0
        companies_processed = 0

        for i, company_data in enumerate(tracked_companies, 1):
            company_domain = company_data["domain"]
            company_name = company_data["name"]
            added_at = datetime.fromisoformat(company_data["added_at"]).strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"🔄 [{i}/{len(tracked_companies)}] Processing company: {company_name} ({company_domain}) - Added: {added_at}")

            # Fetch new reviews
            new_reviews = get_company_reviews(company_domain)
            if new_reviews:
                # Filter out reviews we already have
                existing_review_ids = {r["id"] for r in all_reviews if r["company_domain"] == company_domain}
                new_reviews = [r for r in new_reviews if r.id not in existing_review_ids]

                if new_reviews:
                    logger.info(f"✨ Found {len(new_reviews)} new reviews for {company_domain}")
                    # Add new reviews to storage
                    all_reviews.extend([r.dict() for r in new_reviews])
                    new_reviews_count += len(new_reviews)
                else:
                    logger.info(f"📭 No new reviews found for {company_domain}")
            else:
                logger.warning(f"⚠️ Failed to fetch reviews for {company_domain}")

            companies_processed += 1

        # Save updated reviews
        write_json_file(settings.REVIEWS_FILE, all_reviews)
        logger.info(f"💾 Saved {len(all_reviews)} total reviews to storage")

        # Update job log with success
        job_log.status = "success"
        job_log.end_time = datetime.now()
        job_log.reviews_fetched = new_reviews_count
        job_log.companies_processed = companies_processed

        logger.success(f"✅ Background job {job_id} completed successfully!")
        logger.success(f"📊 Processed {companies_processed} companies in priority order (newest first), fetched {new_reviews_count} new reviews")
        logger.info("🎯 Company processing priority: Recently tracked companies get reviews fetched first")

    except Exception as e:
        # Update job log with error
        job_log.status = "error"
        job_log.end_time = datetime.now()
        job_log.error_message = str(e)

        logger.error(f"❌ Background job {job_id} failed with error: {e}")
        logger.error("🚨 Background job execution stopped due to error")

    finally:
        # Update the job log in storage
        logs = read_json_file(settings.LOGS_FILE)
        for i, log in enumerate(logs):
            if log["job_id"] == job_id:
                logs[i] = job_log.dict()
                break
        write_json_file(settings.LOGS_FILE, logs)

        if job_log.status == "success":
            logger.info(f"📋 Job log updated in storage - Status: {job_log.status}")
        else:
            logger.warning(f"📋 Job log updated in storage - Status: {job_log.status} - Error: {job_log.error_message}")
