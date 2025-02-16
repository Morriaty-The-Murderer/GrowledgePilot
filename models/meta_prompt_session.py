# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship

from .base import Base, BaseMixin
from .user import UserModel


class MetaPromptStatus(str, Enum):
    STARTED = "started"
    COLLECTING = "collecting" 
    COMPLETED = "completed"


class MetaPromptSession(Base, BaseMixin):
    __tablename__ = "meta_prompt_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(MetaPromptStatus), default=MetaPromptStatus.STARTED, nullable=False)
    collected_preferences = Column(JSON, default={})
    generated_prompt = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("UserModel", back_populates="meta_prompt_sessions")

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.status = MetaPromptStatus.STARTED
        self.collected_preferences = {}

    def update_status(self, new_status: MetaPromptStatus) -> None:
        self.status = new_status
        if new_status == MetaPromptStatus.COMPLETED:
            self.completed_at = datetime.utcnow()

    def add_preference(self, key: str, value: any) -> None:
        """Add or update a user preference"""
        if self.collected_preferences is None:
            self.collected_preferences = {}
        self.collected_preferences[key] = value

    def set_generated_prompt(self, prompt: str) -> None:
        """Set the generated personalized prompt"""
        self.generated_prompt = prompt
        self.update_status(MetaPromptStatus.COMPLETED)

    def get_preference(self, key: str) -> Optional[any]:
        """Retrieve a specific preference value"""
        return self.collected_preferences.get(key) if self.collected_preferences else None

    def is_complete(self) -> bool:
        """Check if the meta prompt session is complete"""
        return self.status == MetaPromptStatus.COMPLETED

    def to_dict(self) -> Dict:
        """Convert session to dictionary format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status.value,
            'collected_preferences': self.collected_preferences,
            'generated_prompt': self.generated_prompt,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

# Add Meta Prompt Session relationship to UserModel
UserModel.meta_prompt_sessions = relationship("MetaPromptSession", back_populates="user")