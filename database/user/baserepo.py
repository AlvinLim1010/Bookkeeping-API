from sqlalchemy.orm import Session
from database.user.models import User
from database.user import schemas

from typing import Optional


class UserBaseRepo:
    
    def fetch_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    def fetch_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
    
    def fetch_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()