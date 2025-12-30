from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: Optional[  str] = None
    email: EmailStr
    password_hash: str
    is_active: bool = True
    is_logged_in: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    key: str

class SignUp(BaseModel):
    email: EmailStr
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str