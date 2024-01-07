from collections import Counter
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from http import HTTPStatus

from apis import create_app
from apis.common import enums
from database import get_db, engine

from database.user import models
from database.user import schemas as user_schemas
from database.user.repositories import UserRepo

from database.action import models
from database.action import schemas as action_schemas
from database.action.repositories import ActionRepo


global app
app = create_app()

models.Base.metadata.create_all(bind=engine)


@app.post('/user/login', tags=["User"], response_model=user_schemas.UserReturn, status_code=HTTPStatus.OK)
def user_login(user_request: user_schemas.UserLogin, db: Session = Depends(get_db)):
    if user := UserRepo.fetch_user_by_email(db=db, email=user_request.email):
        if UserRepo.check_password(user_keyin_password=user_request.password, user_db_password=user.password):
            if user.is_verified:
                return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())
            
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Please Verified your email first!")
        
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect Email/Password!")


@app.post('/user/register', tags=["User"], response_model=user_schemas.UserReturn, status_code=HTTPStatus.CREATED)
def user_register(user_request: user_schemas.UserCreate, db: Session = Depends(get_db)):
    if UserRepo.fetch_user_by_username(db=db, username=user_request.username.upper()):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="User already exists!")
    
    hash_password, salt = UserRepo.hash_password(user_request.password)
    user_create = {
        "username": user_request.username.upper(),
        "password": f"{hash_password} {salt}",
        "email": user_request.email
    }

    user = UserRepo.add_user(db=db, input=user_create)

    return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())


@app.patch('/user/reset', tags=["User"], response_model=user_schemas.UserReturn, status_code=HTTPStatus.OK)
def user_reset_password(user_request: user_schemas.UserUpdate, db: Session = Depends(get_db)):

    if db_user := UserRepo.fetch_user_by_email(db=db, email=user_request.email):
        if UserRepo.check_password(user_keyin_password=user_request.old_password, user_db_password=db_user.password):

            if UserRepo.check_password(user_keyin_password=user_request.new_password, user_db_password=db_user.password):
                raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Same Password Entered!")

            user = UserRepo.update_password(db=db, input=user_request)
            return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())
        
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Old Password Incorrect!")
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")

@app.patch('/user/update', tags=["User"], response_model=user_schemas.UserReturn, status_code=HTTPStatus.OK)
def user_update_info(user_request: user_schemas.UserUpdateInfo, db: Session = Depends(get_db)):

    if UserRepo.fetch_user_by_email(db=db, email=user_request.email):
        user = UserRepo.update_info(db=db, input=user_request)

        return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")

@app.post('/user/info', tags=["User"], response_model=user_schemas.UserReturn, status_code=HTTPStatus.OK)
def user_info(user_request: user_schemas.UserBase, db: Session = Depends(get_db)):
    if db_user := UserRepo.fetch_user_by_username(db=db, username=user_request.username.upper()):
        return JSONResponse(status_code=HTTPStatus.OK, content=db_user.as_dict())
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")


@app.post('/user/forget', tags=["User"], response_model=user_schemas.UserReturn, status_code=HTTPStatus.OK)
def user_forgot_password(user_request: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    if UserRepo.fetch_user_by_email(db=db, email=user_request.email):

        # Generate random password
        user_request.new_password = 'abc123'

        user = UserRepo.update_password(db=db, input=user_request)

        return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())
        
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email does not exists!")



@app.post('/actions', tags=["Action"], status_code=HTTPStatus.OK)
def get_actions(action_request: action_schemas.ActionBase, db: Session = Depends(get_db)):
    if db_user:= UserRepo.fetch_user_by_username(db, username=action_request.username.upper()):
        all_actions = ActionRepo.fetch_actions_by_user_id(db, db_user.id)
        content = [action.as_dict() for action in all_actions]
        return JSONResponse(status_code=HTTPStatus.OK, content=content)
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")

@app.post('/actions/overview', tags=["Action"], status_code=HTTPStatus.OK)
def get_actions_overview(action_request: action_schemas.ActionBase, db: Session = Depends(get_db)):
    all_actions = ActionRepo.fetch_all_actions(db)

    sorted_actions: List[models.Action] = sorted(all_actions, key=lambda x: x.date)
    start_date = sorted_actions[0].date
    final_date = sorted_actions[-1].date
    
    valid_categories = {category.value for category in enums.ActionTypes}

    main_categories = [action.main_category for action in all_actions]
    category_counts = Counter(main_categories)

    all_category = {category: category_counts.get(category, 0) for category in valid_categories}

    content = { 
        "all_category": {
            **all_category, 
            "Total": len(all_actions),
            "Start_date": start_date.strftime("%Y-%m-%d"),
            "Final_date": final_date.strftime("%Y-%m-%d"),
        },
    }
    
    if action_request.username:
        if db_user:= UserRepo.fetch_user_by_username(db, username=action_request.username.upper()):
            all_actions = ActionRepo.fetch_actions_by_user_id(db, db_user.id)
            sorted_actions: List[models.Action] = sorted(all_actions, key=lambda x: x.date)
            start_date = sorted_actions[0].date
            final_date = sorted_actions[-1].date
            
            main_categories = [action.main_category for action in all_actions]
            category_counts = Counter(main_categories)

            user_category = {category: category_counts.get(category, 0) for category in valid_categories}

            previous_category = {}
            for day in range(0,7):
                previous_actions = ActionRepo.fetch_updated_actions_from_days(db, day, db_user.id)
                main_categories = [action.main_category for action in previous_actions]
                category_counts = Counter(main_categories)

                total_count = len(previous_actions)
                date = (datetime.utcnow() - timedelta(days=day)).date()

                previous_category[day] = {
                    'date': date.strftime("%Y-%m-%d"),
                    'count': total_count,
                    'categories': {category: category_counts.get(category, 0) for category in valid_categories}
                }

            content = {
                **content, 
                "user_category": {
                    **user_category, 
                    "Total": len(all_actions),
                    "Start_date": start_date.strftime("%Y-%m-%d"),
                    "Final_date": final_date.strftime("%Y-%m-%d"),
                },
                "previous_category": previous_category,
            }

        else:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")

    return JSONResponse(status_code=HTTPStatus.OK, content=content)

@app.post('/actions/create', tags=["Action"], response_model=action_schemas.ActionReturn, status_code=HTTPStatus.CREATED)
def create_actions(action_request: action_schemas.ActionCreate, db: Session = Depends(get_db)):
    if db_user:= UserRepo.fetch_user_by_username(db, username=action_request.username.upper()):

        if any(action_request.main_category == item.value for item in enums.ActionTypes):
            action_create = {
                "date": action_request.date,
                "main_category": action_request.main_category,
                "sub_category": action_request.sub_category,
                "amount": action_request.amount,
                "remarks": action_request.remarks,
                "user_id": db_user.id,
            }

            action = ActionRepo.add_action(db=db, action_input=action_create)

            return JSONResponse(status_code=HTTPStatus.OK, content=action.as_dict())
        
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Action is not allowed!")
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")


@app.patch('/actions/update', tags=["Action"], response_model=action_schemas.ActionReturn, status_code=HTTPStatus.OK)
def update_actions(action_request: action_schemas.ActionUpdate, db: Session = Depends(get_db)):
    if action := ActionRepo.fetch_single_action_by_id(db, action_request.action_id):
        action = ActionRepo.update_action(db=db, action_input=action_request)

        return JSONResponse(status_code=HTTPStatus.OK, content=action.as_dict())
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Action not found!")


@app.delete('/actions/delete', tags=["Action"], response_model=action_schemas.ActionReturn, status_code=HTTPStatus.OK)
def delete_actions(action_request: action_schemas.ActionID, db: Session = Depends(get_db)):
    
    if action := ActionRepo.fetch_single_action_by_id(db=db, action_id=action_request.action_id):
        deleted_action = ActionRepo.delete_action(db=db, action=action)

        return JSONResponse(status_code=HTTPStatus.OK, content=deleted_action.as_dict())
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Action not found!")
    