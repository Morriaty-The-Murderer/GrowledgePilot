# -*- coding: utf-8 -*-
# built-in packages

# third-party packages
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship

# self-defined packages
from .base import Base, BaseMixin


class UserModel(Base, BaseMixin):
    __tablename__ = "users"

    name = Column(String, index=True)
    age = Column(Integer)
    occupation = Column(String)
    
    # Learning preferences and personalization fields
    preferred_learning_style = Column(String, nullable=True)
    language_preference = Column(String, nullable=True)
    learning_goals = Column(JSON, default={})
    personalized_prompt = Column(Text, nullable=True)
    meta_prompt_complete = Column(Boolean, default=False)
    
    # Relationships
    objectives = relationship("ObjectiveModel", back_populates="user")
    meta_prompt_sessions = relationship("MetaPromptSession", back_populates="user")
    created_at = Column(DateTime)
    last_login = Column(DateTime)

    def update_learning_preferences(self, 
                                  learning_style: str = None,
                                  language: str = None,
                                  goals: dict = None) -> None:
        """Update user's learning preferences"""
        if learning_style:
            self.preferred_learning_style = learning_style
        if language:
            self.language_preference = language
        if goals:
            self.learning_goals = goals

    def set_personalized_prompt(self, prompt: str) -> None:
        """Set the user's personalized learning prompt"""
        self.personalized_prompt = prompt
        self.meta_prompt_complete = True

    def get_learning_goals(self) -> dict:
        """Retrieve user's learning goals"""
        return self.learning_goals or {}

    def is_onboarding_complete(self) -> bool:
        """Check if user has completed the meta prompt onboarding"""
        return self.meta_prompt_complete