from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
import datetime

from apis import create_app
from database import get_db, engine

from database.user import models
from database.user import schemas as user_schemas
from database.user.repositories import UserRepo

from database.action import models
from database.action import schemas as action_schemas
from database.action.repositories import ActionRepo, FoodRepo, TravelRepo, HouseHoldRepo, IncomeRepo, MiscRepo


global app
app = create_app()

models.Base.metadata.create_all(bind=engine)

ActionType = ['Action', 'Food', 'Household', 'Income', 'Travel', 'Misc']


@app.post('/user/login', tags=["User"], response_model=user_schemas.UserLogin, status_code=200)
def user_login(user_request: user_schemas.UserLogin, db: Session = Depends(get_db)):
    if user := UserRepo.fetch_user_by_email(db=db, email=user_request.email):
        if UserRepo.check_password(user_keyin_password=user_request.password, user_db_password=user.password):
            if user.is_verified:
                return JSONResponse(status_code=200, content=user.as_dict())
            
            raise HTTPException(status_code=401, detail="Please Verified your email first!")
        
    raise HTTPException(status_code=401, detail="Incorrect Email/Password!")


@app.post('/user/register', tags=["User"], response_model=user_schemas.UserCreate, status_code=201)
def user_register(user_request: user_schemas.UserCreate, db: Session = Depends(get_db)):
    if UserRepo.fetch_user_by_username(db=db, username=user_request.username.upper()):
        raise HTTPException(status_code=400, detail="User already exists!")
    
    hash_password, salt = UserRepo.hash_password(user_request.password)
    user_create = {
        "username": user_request.username.upper(),
        "password": f"{hash_password} {salt}",
        "email": user_request.email
    }

    user = UserRepo.add_user(db=db, input=user_create)

    return JSONResponse(status_code=200, content=user.as_dict())


@app.post('/user/reset', tags=["User"], response_model=user_schemas.UserUpdate, status_code=201)
def user_reset_password(user_request: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = UserRepo.fetch_user_by_email(db=db, email=user_request.email)
    if UserRepo.check_password(user_keyin_password=user_request.old_password, user_db_password=db_user.password):

        if UserRepo.check_password(user_keyin_password=user_request.new_password, user_db_password=db_user.password):
            raise HTTPException(status_code=400, detail="Same Password Entered!")

        user = UserRepo.update_password(db=db, input=user_request)
        return JSONResponse(status_code=200, content=user.as_dict())
    
    raise HTTPException(status_code=400, detail="Old Password Incorrect!")

@app.post('/user/info', tags=["User"], response_model=user_schemas.UserBase, status_code=200)
def user_info(user_request: user_schemas.UserBase, db: Session = Depends(get_db)):
    if db_user := UserRepo.fetch_user_by_username(db=db, username=user_request.username.upper()):
        return JSONResponse(status_code=200, content=db_user.as_dict())
    
    raise HTTPException(status_code=401, detail="User not found!")


@app.post('/user/forget', tags=["User"], response_model=user_schemas.UserUpdate, status_code=201)
def user_forgot_password(user_request: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    if UserRepo.fetch_user_by_email(db=db, email=user_request.email):

        # Generate random password
        user_request.new_password = 'abc123'

        user = UserRepo.update_password(db=db, input=user_request)

        return JSONResponse(status_code=200, content=user.as_dict())
        
    raise HTTPException(status_code=401, detail="Email does not exists!")



@app.get('/actions/get')
def get_actions():
    return {'get actions', 200}


@app.post('/actions/create', tags=["Action"], response_model=action_schemas.ActionCreate, status_code=201)
def create_actions(action_request: action_schemas.ActionCreate, db: Session = Depends(get_db)):
    if db_user:= UserRepo.fetch_user_by_username(db, username=action_request.username.upper()):

        if action_request.main_category in ActionType:
            action_create = {
                "date": action_request.date,
                "main_category": action_request.main_category,
                "user_id": db_user.id,
            }

            action = ActionRepo.add_action(db=db, input=action_create)

            sub_category_create = {
                "sub_category": action_request.sub_category,
                "amount": action_request.amount,
                "remarks": action_request.remarks,
                "action_id": action.id,
            }

            if action.main_category == 'Food':
                sub_action = FoodRepo.add_food(db=db, input=sub_category_create)

            elif action.main_category == 'Travel':
                sub_action = TravelRepo.add_travel(db=db, input=sub_category_create)

            elif action.main_category == 'Household':
                sub_action = HouseHoldRepo.add_household(db=db, input=sub_category_create)

            elif action.main_category == 'Income':
                sub_action = IncomeRepo.add_income(db=db, input=sub_category_create)
                
            else:
                sub_action = MiscRepo.add_misc(db=db, input=sub_category_create)

            results = {'main_category': action.as_dict(), 'sub_category': sub_action.as_dict()}

            return JSONResponse(status_code=200, content=results)
        
        raise HTTPException(status_code=404, detail="Action is not allowed!")
    
    raise HTTPException(status_code=401, detail="User not found!")


@app.patch('/actions/update')
def update_actions():
    return {'update actions', 200}


@app.delete('/actions/delete')
def delete_actions():
    return {'delete actions', 200}
    