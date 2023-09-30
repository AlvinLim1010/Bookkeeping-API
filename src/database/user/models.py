from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship

from src.database import Base
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True)
    password = Column(Text)
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow())

    def __str__(self):
        return f'{self.id}-{self.username}'

    def get_user_id(self):
        return self.id
    