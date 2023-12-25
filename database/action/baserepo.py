from sqlalchemy.orm import Session
from database.action.models import Action

from typing import Optional


class ActionBaseRepo:
    def fetch_single_action_by_id(db: Session, action_id: int) -> Optional[Action]:
        return db.query(Action).filter(Action.id == action_id).first()
    
    def fetch_actions_by_user_id(db: Session, user_id: int) -> Optional[Action]:
        return db.query(Action).filter(Action.user_id == user_id).all()
    
    def fetch_all_actions(db: Session) -> Optional[Action]:
        return db.query(Action).all()
    