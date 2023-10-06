from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), default=func.clock_timestamp())
    created_at = Column(DateTime(timezone=True), default=func.clock_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.clock_timestamp())

    # Income / Outgoing
    action_type = Column(String(40))
    main_category = Column(String(40), unique=True)

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User')

    def __str__(self):
        return f'{self.id}-{self.date}'

    def get_action_id(self):
        return self.id


class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40), unique=True)
    amount = Column(Integer)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_food_id(self):
        return self.id


class Travel(Base):
    __tablename__ = "travel"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40), unique=True)
    amount = Column(Integer)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_travel_id(self):
        return self.id


class Misc(Base):
    __tablename__ = "misc"
    id = Column(Integer, primary_key=True)

    sub_category = Column(String(40), unique=True)
    amount = Column(Integer)
    remarks = Column(JSON(), default={})

    action_id = Column(Integer, ForeignKey('action.id', ondelete='CASCADE'))
    action = relationship('Action')

    def __str__(self):
        return f'{self.id}-{self.sub_category}'

    def get_misc_id(self):
        return self.id
