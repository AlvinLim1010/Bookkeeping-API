from sqlalchemy.orm import Session
from database.user.models import User
from database.user import schemas
from database.user.baserepo import UserBaseRepo

import bcrypt
from typing import Optional, ByteString, Tuple


class UserRepo:
    base = UserBaseRepo

    def add_user(db: Session, input: schemas.UserCreate) -> Optional[User]:
        user = User(username=input["username"], password=input["password"], email=input["email"])
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @classmethod
    def fetch_user_by_id(cls, db: Session, user_id: int) -> Optional[User]:
        return cls.base.fetch_user_by_id(db, user_id)
    
    @classmethod
    def fetch_user_by_username(cls, db: Session, username: str):
        return cls.base.fetch_user_by_username(db, username)
    
    @classmethod
    def fetch_user_by_email(cls, db: Session, email: str) -> Optional[User]:
        return cls.base.fetch_user_by_email(db, email)
    
    def hash_password(plaintext_password:str)-> Tuple[str,str]:
        # Adding the salt to password
        salt: ByteString = bcrypt.gensalt()
        byte_plaintext_password: ByteString = plaintext_password.encode()

        # Hashing the password
        hashed_password = bcrypt.hashpw(byte_plaintext_password, salt)
        return hashed_password.decode(), salt.decode()
    
    def check_password(user_keyin_password:str, user_db_password:str) -> bool:
        hashed_password, salt = user_db_password.split()

        if hashed_password.encode() == bcrypt.hashpw(user_keyin_password.encode(), salt.encode()):
            return True
        
    async def delete_user(cls, db: Session, input: schemas.UserBase) -> Optional[User]:
        user = cls.base.fetch_user_by_username(db, input.username)
        db.delete(user)
        db.commit()
        return user

    @classmethod
    def update_password(cls, db: Session, input: schemas.UserUpdate) -> Optional[User]:
        user = cls.base.fetch_user_by_email(db, input.email)
        
        hash_password, salt = UserRepo.hash_password(input.new_password)
        new_password = f"{hash_password} {salt}"

        user.password = new_password

        db.commit()
        db.refresh(user)
        return user

        