from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
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


@app.post('/user/login', tags=["User"], response_model=user_schemas.UserLogin, status_code=HTTPStatus.OK)
def user_login(user_request: user_schemas.UserLogin, db: Session = Depends(get_db)):
    if user := UserRepo.fetch_user_by_email(db=db, email=user_request.email):
        if UserRepo.check_password(user_keyin_password=user_request.password, user_db_password=user.password):
            if user.is_verified:
                return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())
            
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Please Verified your email first!")
        
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect Email/Password!")


@app.post('/user/register', tags=["User"], response_model=user_schemas.UserCreate, status_code=HTTPStatus.CREATED)
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


@app.post('/user/reset', tags=["User"], response_model=user_schemas.UserUpdate, status_code=HTTPStatus.OK)
def user_reset_password(user_request: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = UserRepo.fetch_user_by_email(db=db, email=user_request.email)
    if UserRepo.check_password(user_keyin_password=user_request.old_password, user_db_password=db_user.password):

        if UserRepo.check_password(user_keyin_password=user_request.new_password, user_db_password=db_user.password):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Same Password Entered!")

        user = UserRepo.update_password(db=db, input=user_request)
        return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())
    
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Old Password Incorrect!")

@app.post('/user/info', tags=["User"], response_model=user_schemas.UserBase, status_code=HTTPStatus.OK)
def user_info(user_request: user_schemas.UserBase, db: Session = Depends(get_db)):
    if db_user := UserRepo.fetch_user_by_username(db=db, username=user_request.username.upper()):
        return JSONResponse(status_code=HTTPStatus.OK, content=db_user.as_dict())
    
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="User not found!")


@app.post('/user/forget', tags=["User"], response_model=user_schemas.UserUpdate, status_code=HTTPStatus.OK)
def user_forgot_password(user_request: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    if UserRepo.fetch_user_by_email(db=db, email=user_request.email):

        # Generate random password
        user_request.new_password = 'abc123'

        user = UserRepo.update_password(db=db, input=user_request)

        return JSONResponse(status_code=HTTPStatus.OK, content=user.as_dict())
        
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email does not exists!")



@app.get('/actions/overview', tags=["Action"], status_code=HTTPStatus.OK)
def get_actions(username: str, db: Session = Depends(get_db)):
    if db_user:= UserRepo.fetch_user_by_username(db, username=username.upper()):
        all_actions = ActionRepo.fetch_actions_by_user_id(db, db_user.id)
        content = [action.as_dict() for action in all_actions]
        return JSONResponse(status_code=HTTPStatus.OK, content=content)
    
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="User not found!")


@app.post('/actions/create', tags=["Action"], response_model=action_schemas.ActionCreate, status_code=HTTPStatus.CREATED)
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
    
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="User not found!")


@app.patch('/actions/update', tags=["Action"], response_model=action_schemas.ActionCreate, status_code=HTTPStatus.OK)
def update_actions(action_request: action_schemas.ActionUpdate, db: Session = Depends(get_db)):
    action = ActionRepo.update_action(db=db, action_input=action_request)

    return JSONResponse(status_code=HTTPStatus.OK, content=action.as_dict())


@app.delete('/actions/delete', tags=["Action"], response_model=action_schemas.ActionCreate, status_code=HTTPStatus.OK)
def delete_actions(action_request: action_schemas.ActionID, db: Session = Depends(get_db)):
    
    action = ActionRepo.delete_action(db=db, action_id=action_request.action_id)

    return JSONResponse(status_code=HTTPStatus.OK, content=action.as_dict())
    