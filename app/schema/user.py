import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    role: str
    password_hash: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RefreshToken(BaseModel):
    refresh_token: str