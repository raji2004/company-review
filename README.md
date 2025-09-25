# Company Review Monitor API

A FastAPI-based REST API for monitoring company reviews from Trustpilot with automatic background job processing.

## Features

- **JWT Authentication**: Secure endpoints with token-based authentication
- **Company Search**: Search for companies using Trustpilot API
- **Review Tracking**: Add companies to tracking list and get their reviews
- **Automatic Updates**: Background jobs fetch new reviews every 5 minutes
- **JSON Storage**: All data stored in JSON files for simplicity
- **Job Logging**: Comprehensive logging of background job execution
- **Loguru Integration**: Advanced logging with file rotation, colorful console output, and detailed tracking

## Setup

### Quick Start (Recommended)

Use the provided bash scripts for easy setup:

1. **Setup virtual environment and dependencies:**

   ```bash
   ./setupVirtualEnv.sh
   ```

   _This script creates a virtual environment, activates it, and installs all dependencies from requirements.txt_

2. **Configure environment (optional):**
  Create a `.env` file with:

  ```bash
  RAPIDAPI_KEY=f087850b41mshb3c7794a5fe78b0p1006edjsn8cc54b6de0ef
  SECRET_KEY=your-super-secret-jwt-key
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  ```

3. **Start the application:**
   ```bash
   ./start.sh
   ```
   _This script installs dependencies (if needed) and runs the FastAPI application_

### Manual Setup (Alternative)

0. **Setup virtual environment:**

   ```bash
   python -m venv venv
   ```

1. **Activate virtual environment:**

   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional):**
   Create a `.env` file with:

   ```bash
   RAPIDAPI_KEY=f087850b41mshb3c7794a5fe78b0p1006edjsn8cc54b6de0ef
   SECRET_KEY=your-super-secret-jwt-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

> **Note:** Make sure to make the bash scripts executable before running them:
>
> ```bash
> chmod +x setupVirtualEnv.sh start.sh
> ```

## Default User

A default user is created automatically:

- Username: `admin`
- Password: `admin123`

## API Endpoints

### Authentication

- `POST /auth/login` - Get JWT token
  ```bash
  curl -X POST "http://localhost:8000/auth/login" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       -d "username=admin&password=admin123"
  ```

### Company Search

- `GET /companies/search?query=bestbuy` - Search companies
  ```bash
  curl -X GET "http://localhost:8000/companies/search?query=bestbuy" \
       -H "Authorization: Bearer <your_token>"
  ```

### Company Tracking

- `POST /companies/track` - Add company to tracking

  ```bash
  curl -X POST "http://localhost:8000/companies/track" \
       -H "Authorization: Bearer <your_token>" \
       -H "Content-Type: application/json" \
       -d '{"domain": "gossby.com", "name": "Gossby", "website": "https://gossby.com"}'
  ```

- `GET /companies/tracked` - Get tracked companies
  ```bash
  curl -X GET "http://localhost:8000/companies/tracked" \
       -H "Authorization: Bearer <your_token>"
  ```

### Reviews

- `GET /reviews/{domain}` - Get reviews for a company
  ```bash
  curl -X GET "http://localhost:8000/reviews/gossby.com" \
       -H "Authorization: Bearer <your_token>"
  ```

## Data Storage

All data is stored in JSON files in the `data/` directory:

- `users.json` - User accounts and credentials
- `tracked_companies.json` - Companies being tracked by users
- `reviews.json` - All fetched reviews
- `job_logs.json` - Background job execution logs

## Background Jobs

The system automatically runs background jobs every 5 minutes to:

1. **Prioritized Processing**: Fetch new reviews for recently tracked companies first
2. Update the reviews storage
3. Log job execution details

### **Company Processing Priority**

- 🥇 **Newest First**: Recently added companies get their reviews fetched first
- 📅 **Sorted by Date**: Companies are sorted by `added_at` timestamp in descending order
- ⚡ **Faster Updates**: New company tracking requests get reviews sooner

## Logging System

The application uses **Loguru** for comprehensive logging with the following features:

### **Log Files**

- **Location**: `logs/app.log`
- **Rotation**: 10MB file size
- **Retention**: 7 days
- **Format**: `{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}`

### **Console Output**

- **Colorful formatting** with emojis for better readability
- **Real-time logging** of all system activities
- **Different colors** for different log levels (INFO, SUCCESS, WARNING, ERROR)

### **What Gets Logged**

- 🔐 **Authentication**: Login attempts and results
- 🔍 **API Requests**: Company searches, tracking requests, review requests
- 📊 **Background Jobs**: Detailed progress with company processing order
- 🎯 **Processing Priority**: Shows which companies are processed first (newest)
- ✅ **Success Operations**: Successful operations and results
- ❌ **Errors**: API failures, validation errors, and exceptions
- 🚀 **System Events**: Startup, shutdown, and system status

### **Log Levels Used**

- `logger.info()` - General information and progress
- `logger.success()` - Successful operations
- `logger.warning()` - Warnings and recoverable issues
- `logger.error()` - Errors and failures

## Error Handling

- Comprehensive error handling for API calls
- JWT token validation and expiration
- Company tracking validation
- Background job error logging

## Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- python-jose - JWT tokens
- passlib - Password hashing
- bcrypt - Password hashing backend
- requests - HTTP client
- apscheduler - Background jobs
- python-dotenv - Environment variables
- loguru - Advanced logging system
- email-validator - Email validation for Pydantic
