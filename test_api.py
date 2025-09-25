#!/usr/bin/env python3
"""
Test script to verify the Trustpilot API calls are working correctly.
"""
import requests
from loguru import logger

# Test the API endpoints
RAPIDAPI_KEY = "f087850b41mshb3c7794a5fe78b0p1006edjsn8cc54b6de0ef"
COMPANY_SEARCH_URL = "https://trustpilot-company-and-reviews-data.p.rapidapi.com/company-search"
COMPANY_REVIEWS_URL = "https://trustpilot-company-and-reviews-data.p.rapidapi.com/company-reviews"

headers = {
    "x-rapidapi-host": "trustpilot-company-and-reviews-data.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}

def test_company_search():
    """Test the company search API"""
    logger.info("🔍 Testing company search API...")

    params = {"query": "bestbuy"}

    try:
        response = requests.get(COMPANY_SEARCH_URL, headers=headers, params=params)
        logger.info(f"📊 Response status: {response.status_code}")
        logger.info(f"📊 Response headers: {response.headers}")

        if response.status_code == 200:
            data = response.json()
            logger.success(f"✅ API call successful! Found {len(data.get('companies', []))} companies")
            logger.info(f"📄 Full response: {data}")
            return data
        else:
            logger.error(f"❌ API call failed with status {response.status_code}")
            logger.error(f"❌ Response: {response.text}")
            return None

    except Exception as e:
        logger.error(f"❌ Error testing company search: {e}")
        return None

def test_company_reviews():
    """Test the company reviews API"""
    logger.info("📖 Testing company reviews API...")

    params = {"company_domain": "gossby.com"}

    try:
        response = requests.get(COMPANY_REVIEWS_URL, headers=headers, params=params)
        logger.info(f"📊 Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.success(f"✅ API call successful! Found {len(data.get('reviews', []))} reviews")
            logger.info(f"📄 Full response: {data}")
            return data
        else:
            logger.error(f"❌ API call failed with status {response.status_code}")
            logger.error(f"❌ Response: {response.text}")
            return None

    except Exception as e:
        logger.error(f"❌ Error testing company reviews: {e}")
        return None

if __name__ == "__main__":
    logger.info("🚀 Starting API tests...")

    # Test company search
    search_result = test_company_search()

    # Test company reviews
    reviews_result = test_company_reviews()

    logger.info("🏁 API tests completed!")
