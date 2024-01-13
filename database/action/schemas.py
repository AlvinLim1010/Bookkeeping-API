from pydantic import BaseModel
import datetime

from typing import Dict, Optional

class ActionBase(BaseModel):
    username: str

class ActionID(BaseModel):
    action_id: int

class ActionCreate(ActionBase):
    date: datetime.date
    main_category: str
    sub_category: str
    amount: float
    remarks: Dict 

class ActionUpdate(ActionID):
    date: Optional[datetime.date] = None
    amount: Optional[float] = None
    remarks: Optional[Dict] = None

class ActionReturn(ActionCreate):
      id: int
      user_id: int
    