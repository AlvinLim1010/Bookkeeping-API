import datetime
from pydantic import BaseModel

# from typing import 

class UserBase(BaseModel):
    username: str
    email : str
    password: str


class UserCreate(UserBase):
    created_at: datetime.time 
    