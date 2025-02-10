# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base, BaseMixin


class LearningSessionModel(Base, BaseMixin):
    __tablename__ = "learning_sessions"
    user_id = Column(Integer, ForeignKey("users.id"))
    objective_id = Column(Integer, ForeignKey("objectives.id"))
    # sub_objective_id = Column(Integer, ForeignKey("subobjectives.id"), nullable=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    content = Column(String)
    notes = Column(String, nullable=True)
    ai_prompt = Column(String, nullable=True)

    # Relationships (optional, for easier navigation)
    user = relationship("UserModel")
    objective = relationship("ObjectiveModel")
