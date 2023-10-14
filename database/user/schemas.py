import datetime
from pydantic import BaseModel
from sqlalchemy.sql import func

# from typing import 

class UserBase(BaseModel):
    username: str

class UserEmail(BaseModel):
    email: str

class UserLogin(UserEmail):
    password: str

class UserUpdate(UserEmail):
    old_password: str
    new_password: str

class UserCreate(UserLogin):
    username: str

class UserVerified(UserBase):
    is_verified: bool
    verified_at: datetime.time
    