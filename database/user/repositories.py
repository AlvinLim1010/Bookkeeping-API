from sqlalchemy.orm import Session
from database.user.models import User
from database.user import schemas

import bcrypt
from typing import Optional, ByteString, Tuple


class UserRepo:
    def add_user(db: Session, input_item: schemas.UserCreate) -> Optional[User]:
        user = User(username=input_item.name, passowrd=input_item.password, email=input_item.email, created_at=input_item.created_at)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def fetch_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    def fetch_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
    
    def fetch_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def hash_password(plaintext_password:str)-> Tuple[str,str]:
        # Adding the salt to password
        salt: ByteString = bcrypt.gensalt()
        byte_plaintext_password: ByteString = plaintext_password.encode()

        # Hashing the password
        hashed_password = bcrypt.hashpw(byte_plaintext_password, salt)
        return hashed_password.decode() , salt.decode()
    
    def check_password(hashed_password:str, salt:str, plaintext_password:str) -> bool:

        if hashed_password.encode() == bcrypt.hashpw(plaintext_password.encode(), salt.encode()):
            return True
    
    # def get_hashed_pw_from_mixed_hashed(hashed_pw_with_salt:str)-> str:
    #     hashed_password,_ = hashed_pw_with_salt.split()
    #     return hashed_password   


    # def get_salt_from_mixed_hashed(hashed_pw_with_salt:str)-> str:
    #     _,salt = hashed_pw_with_salt.split()
    #     return salt
    
    # def check_password(self,user_keyin_password:str):
    #     valid:bool = check_password(hashed_pw= get_hashed_pw_from_mixed_hashed(self.password), salt = get_salt_from_mixed_hashed(self.password), plaintext_password= user_keyin_password)
    #     return valid
        
    # async def delete_user(db: Session, input_item: schemas.UserDelete) -> Optional[User]:
    #     user = User(username=input_item.name, passowrd=input_item.password, email=input_item.email)
    #     db.add(user)
    #     db.commit()
    #     db.refresh(user)
    #     return user

    # async def update_user(db: Session, input_item: schemas.UserDelete) -> Optional[User]: