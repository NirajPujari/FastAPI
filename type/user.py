from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: str
    email: EmailStr
    password_hash: str

    is_active: bool = True

    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

class SignUp(BaseModel):
    email: EmailStr
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str