from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from apis import create_app
from database import get_db, engine
from database.user import models, schemas
from database.action import models 
from database.user.repositories import UserRepo


global app
app = create_app()

models.Base.metadata.create_all(bind=engine)


@app.post('/login')
def user_login():
    return {'login', 200}


@app.post('/register', tags=["User"],response_model=schemas.UserCreate,status_code=201)
def user_register(user_request: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create an User and store it in the database
    """

    db_user = UserRepo.fetch_user_by_username(db, username=user_request.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!")
    
    print(user_request.password)

    return UserRepo.add_user(db=db, user=user_request)


@app.get('/actions/get')
def get_actions():
    return {'get actions', 200}


@app.post('/actions/post')
def post_actions():
    return {'post actions', 200}


@app.patch('/actions/update')
def update_actions():
    return {'update actions', 200}


@app.delete('/actions/delete')
def delete_actions():
    return {'delete actions', 200}
    