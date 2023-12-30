from sqlalchemy import or_, and_, func
from sqlalchemy.orm import Session
from database.action.models import Action

from datetime import datetime, timedelta
from typing import Optional


class ActionBaseRepo:
    def fetch_single_action_by_id(db: Session, action_id: int) -> Optional[Action]:
        return db.query(Action).filter(Action.id == action_id).first()
    
    def fetch_actions_by_user_id(db: Session, user_id: int) -> Optional[Action]:
        return db.query(Action).filter(Action.user_id == user_id).all()
    
    def fetch_all_actions(db: Session) -> Optional[Action]:
        return db.query(Action).all()
    
    def fetch_updated_actions_from_days(db: Session, days: int) -> Optional[Action]:
        days_ago = (datetime.utcnow() - timedelta(days=days)).date()
        return (
            db.query(Action)
            .filter(
                or_(
                    func.date(Action.updated_at) == days_ago,
                    and_(func.date(Action.updated_at) == None, func.date(Action.created_at) == days_ago),
                )
            )
            .all()
        )
    