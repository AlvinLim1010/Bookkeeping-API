from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import json

from database import Base


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    created_at = Column(DateTime(timezone=True), default=func.clock_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.clock_timestamp())

    main_category = Column(String(40))

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User')

    def __str__(self):
        return f'{self.id}-{self.date}'

    def get_action_id(self):
        return self.id
    
    def as_dict(self):
        return {
            'id': self.id,
            'date': json.dumps(self.date.strftime("%Y-%m-%d")),
            'main_category': self.main_category,
            'user_id': self.user_id,
        }


class Income(Base):
    __tablename__ = "income"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40))
    amount = Column(Float)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_income_id(self):
        return self.id
    
    def as_dict(self):
        return {
            'id': self.id,
            'sub_category': self.sub_category,
            'amount': self.amount,
            'remarks': self.remarks,
        }
    

class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40))
    amount = Column(Float)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_food_id(self):
        return self.id
    
    def as_dict(self):
        return {
            'id': self.id,
            'sub_category': self.sub_category,
            'amount': self.amount,
            'remarks': self.remarks,
        }


class Travel(Base):
    __tablename__ = "travel"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40))
    amount = Column(Float)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_travel_id(self):
        return self.id
    
    def as_dict(self):
        return {
            'id': self.id,
            'sub_category': self.sub_category,
            'amount': self.amount,
            'remarks': self.remarks,
        }
    

class HouseHold(Base):
    __tablename__ = "household"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40))
    amount = Column(Float)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_household_id(self):
        return self.id
    
    def as_dict(self):
        return {
            'id': self.id,
            'sub_category': self.sub_category,
            'amount': self.amount,
            'remarks': self.remarks,
        }


class Misc(Base):
    __tablename__ = "misc"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40))
    amount = Column(Float)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_misc_id(self):
        return self.id
    
    def as_dict(self):
        return {
            'id': self.id,
            'sub_category': self.sub_category,
            'amount': self.amount,
            'remarks': self.remarks,
        }
