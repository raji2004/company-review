from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobLog(BaseModel):
    job_id: str
    job_type: str
    status: str  # success, error, running
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    companies_processed: Optional[int] = 0
    reviews_fetched: Optional[int] = 0
