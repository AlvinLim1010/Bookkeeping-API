from pydantic import BaseModel
import datetime

from typing import Dict

class ActionBase(BaseModel):
    username: str

class ActionDelete(BaseModel):
    action_id: int

class ActionCreate(ActionBase):
    date: datetime.date
    main_category: str
    sub_category: str
    amount: float
    remarks: Dict 
    