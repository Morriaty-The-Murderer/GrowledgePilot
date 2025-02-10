# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, BaseMixin


class ObjectiveModel(Base, BaseMixin):
    __tablename__ = "objectives"

    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String)
    priority = Column(Integer)
    current_level = Column(String)
    target_level = Column(String)
    user = relationship("UserModel", back_populates="objectives")
