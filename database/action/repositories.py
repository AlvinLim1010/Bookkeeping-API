from sqlalchemy.orm import Session
from database.action.models import Action

from typing import Optional

class ActionRepo:    
    def fetch_action_by_id(db: Session, action_id: int) -> Optional[Action]:
        return db.query(Action).filter(Action.id == action_id).first()
    
    def fetch_action_by_user_id(db: Session, user_id: int) -> Optional[Action]:
        return db.query(Action).filter(Action.user_id == user_id).first()