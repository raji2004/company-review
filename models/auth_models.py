from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr  # Using EmailStr now that email-validator is installed
    password: str
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: Optional[str] = None
    email: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None
