from sqlalchemy.orm import Session
from database.action.models import Action
from database.action import schemas
from database.action.baserepo import ActionBaseRepo

from typing import Optional

class ActionRepo:    
    base = ActionBaseRepo

    @classmethod
    def fetch_single_action_by_id(cls, db: Session, action_id: int) -> Optional[Action]:
        return cls.base.fetch_single_action_by_id(db, action_id)
    
    @classmethod
    def fetch_actions_by_user_id(cls, db: Session, user_id: int) -> Optional[Action]:
        return cls.base.fetch_actions_by_user_id(db, user_id)
    
    @classmethod
    def fetch_all_actions(cls, db: Session) -> Optional[Action]:
        return cls.base.fetch_all_actions(db)
    
    @classmethod
    def fetch_updated_actions_from_days(cls, db: Session, days: int) -> Optional[Action]:
        return cls.base.fetch_updated_actions_from_days(db, days)
    
    def add_action(db: Session, action_input: schemas.ActionCreate) -> Optional[Action]:
        action = Action(
            date=action_input['date'], 
            main_category=action_input['main_category'], 
            sub_category=action_input['sub_category'], 
            amount=action_input['amount'], 
            remarks=action_input['remarks'], 
            user_id=action_input['user_id']
        )

        db.add(action)
        db.commit()
        db.refresh(action)
        return action
    
    @classmethod
    def update_action(cls, db: Session, action_input: schemas.ActionUpdate) -> Optional[Action]:
        action: Action = cls.fetch_single_action_by_id(db, action_input.action_id)

        # db.delete(action)
        db.commit()
        return action
    
    @classmethod
    def delete_action(cls, db: Session, action_id: int) -> Optional[Action]:
        action: Action = cls.fetch_single_action_by_id(db, action_id)
        db.delete(action)
        db.commit()
        return action
