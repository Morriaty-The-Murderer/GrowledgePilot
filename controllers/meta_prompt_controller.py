# -*- coding: utf-8 -*-
from enum import Enum
from typing import Dict, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ai_agents.meta_prompt_agent import MetaPromptAgent
from models.meta_prompt_session import MetaPromptSession, MetaPromptStatus
from models.user import UserModel
from utils.database import get_db


class PromptCollectionStep(str, Enum):
    INIT = "init"
    LEARNING_STYLE = "learning_style"
    GOALS = "goals"
    INTERESTS = "interests"
    REVIEW = "review"
    COMPLETE = "complete"


class MetaPromptController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.agent = MetaPromptAgent()
        self.collection_steps = [
            PromptCollectionStep.INIT,
            PromptCollectionStep.LEARNING_STYLE,
            PromptCollectionStep.GOALS,
            PromptCollectionStep.INTERESTS,
            PromptCollectionStep.REVIEW,
            PromptCollectionStep.COMPLETE
        ]

    def create_session(self, user_id: int) -> MetaPromptSession:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        session = MetaPromptSession(user_id=user_id)
        session.update_status(MetaPromptStatus.STARTED)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: int) -> MetaPromptSession:
        session = self.db.query(MetaPromptSession).filter(
            MetaPromptSession.id == session_id
        ).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        return session

    def get_current_step(self, session: MetaPromptSession) -> PromptCollectionStep:
        if session.status == MetaPromptStatus.COMPLETED:
            return PromptCollectionStep.COMPLETE

        preferences = session.collected_preferences
        if not preferences:
            return PromptCollectionStep.INIT

        if "learning_style" not in preferences:
            return PromptCollectionStep.LEARNING_STYLE
        elif "goals" not in preferences:
            return PromptCollectionStep.GOALS
        elif "interests" not in preferences:
            return PromptCollectionStep.INTERESTS
        else:
            return PromptCollectionStep.REVIEW

    def process_step(
            self,
            session_id: int,
            step: PromptCollectionStep,
            input_data: Optional[Dict] = None
    ) -> Dict:
        session = self.get_session(session_id)
        current_step = self.get_current_step(session)

        if step != current_step:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid step. Expected {current_step}, got {step}"
            )

        if step == PromptCollectionStep.INIT:
            session.update_status(MetaPromptStatus.COLLECTING)
            next_step = PromptCollectionStep.LEARNING_STYLE
        else:
            next_step = self._get_next_step(step)

        self.db.commit()

        return {
            "current_step": step,
            "next_step": next_step,
            "session_id": session_id,
            "status": session.status
        }

    def _collect_step_data(
            self,
            session: MetaPromptSession,
            step: PromptCollectionStep,
            input_data: Dict
    ) -> Dict:
        if step == PromptCollectionStep.LEARNING_STYLE:
            preference = self.agent.collect_preferences(session.user, "learning_style")
            session.add_preference("learning_style", preference)

        elif step == PromptCollectionStep.GOALS:
            goals = self.agent.collect_preferences(session.user, "goals")
            session.add_preference("goals", goals)

        elif step == PromptCollectionStep.INTERESTS:
            interests = self.agent.collect_preferences(session.user, "interests")
            session.add_preference("interests", interests)

        elif step == PromptCollectionStep.REVIEW:
            personalized_prompt = self.agent.generate_personalized_prompt(session)
            session.set_generated_prompt(personalized_prompt)
            session.user.set_personalized_prompt(personalized_prompt)

        return session.collected_preferences

    def _get_next_step(self, current_step: PromptCollectionStep) -> PromptCollectionStep:
        current_index = self.collection_steps.index(current_step)
        if current_index + 1 < len(self.collection_steps):
            return self.collection_steps[current_index + 1]
        return PromptCollectionStep.COMPLETE

    def generate_final_prompt(self, session_id: int) -> str:
        session = self.get_session(session_id)
        if session.status != MetaPromptStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot generate final prompt before completing all steps"
            )
        return session.generated_prompt

    def get_session_progress(self, session_id: int) -> Dict:
        session = self.get_session(session_id)
        current_step = self.get_current_step(session)
        total_steps = len(self.collection_steps) - 2  # Excluding INIT and COMPLETE
        completed_steps = self.collection_steps.index(current_step)

        return {
            "current_step": current_step,
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "progress_percentage": (completed_steps / total_steps) * 100 if total_steps > 0 else 0
        }

    def reset_session(self, session_id: int) -> MetaPromptSession:
        session = self.get_session(session_id)
        session.collected_preferences = {}
        session.generated_prompt = None
        session.update_status(MetaPromptStatus.STARTED)
        self.db.commit()
        return session
