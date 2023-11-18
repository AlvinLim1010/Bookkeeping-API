from sqlalchemy.orm import Session
from database.action.models import Action
from database.action import schemas
from database.action.baserepo import ActionBaseRepo

from typing import Optional

class ActionRepo:    
    base = ActionBaseRepo

    def fetch_single_action_by_id(cls, db: Session, action_id: int) -> Optional[Action]:
        return cls.base.fetch_single_action_by_id(db, action_id)
    
    def fetch_by_user_id(cls, db: Session, user_id: int, offset: int) -> Optional[Action]:
        return cls.base.fetch_by_user_id(db, user_id, offset)
    
    def add_action(db: Session, input: schemas.ActionCreate) -> Optional[Action]:
        action = Action(
            date=input['date'], 
            main_category=input['main_category'], 
            sub_category=input['sub_category'], 
            amount=input['amount'], 
            remarks=input['remarks'], 
            user_id=input['user_id']
        )

        db.add(action)
        db.commit()
        db.refresh(action)
        return action
    
    async def delete_action(cls, db: Session, action_id: int) -> Optional[Action]:
        action = cls.fetch_single_action_by_id(db, action_id)
        db.delete(action)
        db.commit()
        return action
