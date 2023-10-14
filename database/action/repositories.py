from sqlalchemy.orm import Session
from database.action.models import Action, Travel, Income, HouseHold, Misc, Food
from database.action import schemas

from typing import Optional

class ActionRepo:    
    def fetch_single_action_by_id(db: Session, action_id: int) -> Optional[Action]:
        return db.query(Action).filter(Action.id == action_id).first()
    
    def fetch_by_user_id(db: Session, user_id: int, offset: int) -> Optional[Action]:
        number_of_rows:int = db.query(Action).filter(Action.user_id == user_id).all().count()
        skip:int = number_of_rows - offset
        return db.query(Action).filter(Action.user_id == user_id).offset(skip).all()
    
    def add_action(db: Session, input: schemas.ActionCreate) -> Optional[Action]:
        action = Action(date=input['date'], main_category=input['main_category'], user_id=input['user_id'])
        db.add(action)
        db.commit()
        db.refresh(action)
        return action

class TravelRepo: 
    def fetch_by_user_id(db: Session, user_id: int, offset: int) -> Optional[Travel]:
        number_of_rows:int = db.query(Travel).filter(Travel.user_id == user_id).all().count()
        skip:int = number_of_rows - offset
        return db.query(Travel).filter(Travel.user_id == user_id).offset(skip).all()
    
    def add_travel(db: Session, input: schemas.ActionCreate) -> Optional[Travel]:
        travel = Travel(sub_category=input['sub_category'], amount=input['amount'], remarks=input['remarks'], action_id=input['action_id'])
        db.add(travel)
        db.commit()
        db.refresh(travel)
        return travel


class IncomeRepo: 
    def fetch_by_user_id(db: Session, user_id: int, offset: int) -> Optional[Income]:
        number_of_rows:int = db.query(Income).filter(Income.user_id == user_id).all().count()
        skip:int = number_of_rows - offset
        return db.query(Income).filter(Income.user_id == user_id).offset(skip).all()
    
    def add_income(db: Session, input: schemas.ActionCreate) -> Optional[Income]:
        income = Income(sub_category=input['sub_category'], amount=input['amount'], remarks=input['remarks'], action_id=input['action_id'])
        db.add(income)
        db.commit()
        db.refresh(income)
        return income


class HouseHoldRepo: 
    def fetch_by_user_id(db: Session, user_id: int, offset: int) -> Optional[HouseHold]:
        number_of_rows:int = db.query(HouseHold).filter(HouseHold.user_id == user_id).all().count()
        skip:int = number_of_rows - offset
        return db.query(HouseHold).filter(HouseHold.user_id == user_id).offset(skip).all()
    
    def add_household(db: Session, input: schemas.ActionCreate) -> Optional[HouseHold]:
        household = HouseHold(sub_category=input['sub_category'], amount=input['amount'], remarks=input['remarks'], action_id=input['action_id'])
        db.add(household)
        db.commit()
        db.refresh(household)
        return household


class FoodRepo: 
    def fetch_by_user_id(db: Session, user_id: int, offset: int) -> Optional[Food]:
        number_of_rows:int = db.query(Food).filter(Food.user_id == user_id).all().count()
        skip:int = number_of_rows - offset
        return db.query(Food).filter(Food.user_id == user_id).offset(skip).all()
    
    def add_food(db: Session, input: schemas.ActionCreate) -> Optional[Food]:
        food = Food(sub_category=input['sub_category'], amount=input['amount'], remarks=input['remarks'], action_id=input['action_id'])
        db.add(food)
        db.commit()
        db.refresh(food)
        return food


class MiscRepo: 
    def fetch_by_user_id(db: Session, user_id: int, offset: int) -> Optional[Misc]:
        number_of_rows:int = db.query(Misc).filter(Misc.user_id == user_id).all().count()
        skip:int = number_of_rows - offset
        return db.query(Misc).filter(Misc.user_id == user_id).offset(skip).all()
    
    def add_misc(db: Session, input: schemas.ActionCreate) -> Optional[Misc]:
        misc = Misc(sub_category=input['sub_category'], amount=input['amount'], remarks=input['remarks'], action_id=input['action_id'])
        db.add(misc)
        db.commit()
        db.refresh(misc)
        return misc
    