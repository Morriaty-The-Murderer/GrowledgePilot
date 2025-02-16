# -*- coding: utf-8 -*-
from typing import Dict, Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.meta_prompt_session import MetaPromptSession, MetaPromptStatus
from models.user import UserModel
from settings import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database and create all tables."""
    # Import all models to ensure they're registered with metadata
    Base.metadata.create_all(bind=engine)


def migrate_user_preferences():
    """Migrate existing users to include new preference fields."""
    db = SessionLocal()
    try:
        users = db.query(UserModel).all()
        for user in users:
            if not hasattr(user, 'learning_goals'):
                user.learning_goals = {}
            if not hasattr(user, 'meta_prompt_complete'):
                user.meta_prompt_complete = False
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()


def store_user_preferences(user_id: int, preferences: Dict) -> bool:
    """Store or update user preferences."""
    db = SessionLocal()
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return False

        if 'learning_style' in preferences:
            user.preferred_learning_style = preferences['learning_style']
        if 'language' in preferences:
            user.language_preference = preferences['language']
        if 'goals' in preferences:
            user.learning_goals = preferences['goals']

        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
    finally:
        db.close()


def create_meta_prompt_session(user_id: int) -> Optional[MetaPromptSession]:
    """Create a new meta prompt session for a user."""
    db = SessionLocal()
    try:
        session = MetaPromptSession(user_id=user_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    except SQLAlchemyError:
        db.rollback()
        return None
    finally:
        db.close()


def update_prompt_session(session_id: int, preferences: Dict) -> bool:
    """Update meta prompt session with collected preferences."""
    db = SessionLocal()
    try:
        session = db.query(MetaPromptSession).filter(
            MetaPromptSession.id == session_id
        ).first()
        if not session:
            return False

        for key, value in preferences.items():
            session.add_preference(key, value)

        session.update_status(MetaPromptStatus.COLLECTING)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
    finally:
        db.close()


def complete_prompt_session(session_id: int, generated_prompt: str) -> bool:
    """Mark meta prompt session as complete with generated prompt."""
    db = SessionLocal()
    try:
        session = db.query(MetaPromptSession).filter(
            MetaPromptSession.id == session_id
        ).first()
        if not session:
            return False

        session.set_generated_prompt(generated_prompt)
        session.user.set_personalized_prompt(generated_prompt)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
    finally:
        db.close()


def get_user_prompt_data(user_id: int) -> Optional[Dict]:
    """Retrieve user's prompt and preference data."""
    db = SessionLocal()
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None

        return {
            'personalized_prompt': user.personalized_prompt,
            'learning_style': user.preferred_learning_style,
            'language': user.language_preference,
            'goals': user.learning_goals,
            'is_complete': user.meta_prompt_complete
        }
    finally:
        db.close()
