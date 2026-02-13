from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.EMPLOYEE

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True



class UserListResponse(BaseModel):
    users: list[UserResponse]

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: int
    role: Optional[str] = None