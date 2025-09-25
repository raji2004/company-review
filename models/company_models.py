from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Company(BaseModel):
    domain: str
    name: str
    website: str
    trustscore: Optional[float] = None
    trustscore_category: Optional[float] = None  # Actually a float, not string
    number_of_reviews: Optional[int] = None

class TrackedCompany(BaseModel):
    domain: str
    name: str
    added_at: datetime
    user: str
