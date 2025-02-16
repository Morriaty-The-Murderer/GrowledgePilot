# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict, Optional, List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.user import UserModel
from models.meta_prompt_session import MetaPromptSession, MetaPromptStatus
from controllers.meta_prompt_controller import MetaPromptController
from utils.database import get_db


class UserController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.meta_prompt_controller = MetaPromptController(db)

    def create_user(
        self,
        name: str,
        age: int,
        occupation: str,
        language_preference: Optional[str] = None
    ) -> UserModel:
        """Create a new user with initial preferences."""
        db_user = UserModel(
            name=name,
            age=age,
            occupation=occupation,
            language_preference=language_preference,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int) -> Optional[UserModel]:
        """Retrieve user by ID."""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_name(self, name: str) -> Optional[UserModel]:
        """Retrieve user by name."""
        return self.db.query(UserModel).filter(UserModel.name == name).first()

    def update_user_profile(
        self,
        user_id: int,
        name: Optional[str] = None,
        age: Optional[int] = None,
        occupation: Optional[str] = None,
        language_preference: Optional[str] = None
    ) -> UserModel:
        """Update user profile information."""
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if name:
            user.name = name
        if age:
            user.age = age
        if occupation:
            user.occupation = occupation
        if language_preference:
            user.language_preference = language_preference

        self.db.commit()
        self.db.refresh(user)
        return user

    def update_learning_preferences(
        self,
        user_id: int,
        learning_style: Optional[str] = None,
        goals: Optional[Dict] = None,
        interests: Optional[List[str]] = None
    ) -> UserModel:
        """Update user's learning preferences."""
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        updated_goals = user.learning_goals.copy() if user.learning_goals else {}
        
        if learning_style:
            user.preferred_learning_style = learning_style
        if goals:
            updated_goals.update(goals)
            user.learning_goals = updated_goals
        if interests:
            updated_goals['interests'] = interests
            user.learning_goals = updated_goals

        self.db.commit()
        self.db.refresh(user)
        return user

    def start_meta_prompt_flow(self, user_id: int) -> MetaPromptSession:
        """Initialize meta prompt collection flow for a user."""
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.meta_prompt_complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Meta prompt flow already completed"
            )
            
        return self.meta_prompt_controller.create_session(user_id)

    def set_personalized_prompt(self, user_id: int, prompt: str) -> UserModel:
        """Set user's personalized learning prompt."""
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        user.set_personalized_prompt(prompt)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_progress(self, user_id: int) -> Dict:
        """Get user's onboarding and learning progress."""
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        active_session = self.db.query(MetaPromptSession).filter(
            MetaPromptSession.user_id == user_id,
            MetaPromptSession.status != MetaPromptStatus.COMPLETED
        ).first()

        return {
            "onboarding_complete": user.meta_prompt_complete,
            "has_learning_style": bool(user.preferred_learning_style),
            "has_learning_goals": bool(user.learning_goals),
            "has_personalized_prompt": bool(user.personalized_prompt),
            "active_session_id": active_session.id if active_session else None
        }

    def reset_user_preferences(self, user_id: int) -> UserModel:
        """Reset user's learning preferences and prompt."""
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.preferred_learning_style = None
        user.learning_goals = {}
        user.personalized_prompt = None
        user.meta_prompt_complete = False

        self.db.commit()
        self.db.refresh(user)
        return user