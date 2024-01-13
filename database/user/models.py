from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from database import Base
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True)
    password = Column(Text)
    email = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=func.clock_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.clock_timestamp())
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime(timezone=True))

    def __str__(self):
        return f'{self.id}-{self.username}'

    def get_user_id(self):
        return self.id
    
    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
    