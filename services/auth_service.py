from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from loguru import logger

from utils import verify_password, get_password_hash, create_access_token, decode_token, read_json_file, write_json_file
from config import settings
from models.auth_models import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_user(username: str) -> Optional[UserInDB]:
    users_data = read_json_file(settings.USERS_FILE)
    for user_data in users_data:
        if user_data["username"] == username:
            return UserInDB(**user_data)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_default_user():
    users_data = read_json_file(settings.USERS_FILE)
    if not any(user["username"] == "admin" for user in users_data):
        default_user = UserInDB(
            username="admin",
            email="admin@example.com",
            password="admin123",
            hashed_password=get_password_hash("admin123"),
            disabled=False
        )
        users_data.append(default_user.dict())
        write_json_file(settings.USERS_FILE, users_data)
        logger.success("✅ Default user created: admin/admin123")
