from pydantic import BaseModel
from datetime import datetime

class Review(BaseModel):
    id: str
    company_domain: str
    title: str
    content: str
    rating: int
    date: datetime
    author: str
