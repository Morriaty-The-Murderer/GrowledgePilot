# -*- coding: utf-8 -*-
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.objective import ObjectiveModel
from utils.database import get_db


class ObjectiveController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_objective(self,
                         user_id: int,
                         name: str,
                         description: str,
                         priority: int,
                         current_level: str,
                         target_level: str) -> ObjectiveModel:
        db_obj = ObjectiveModel(
            user_id=user_id,
            name=name,
            description=description,
            priority=priority,
            current_level=current_level,
            target_level=target_level
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_objective(self, objective_id: int) -> Optional[ObjectiveModel]:
        return self.db.query(ObjectiveModel).filter(ObjectiveModel.id == objective_id).first()

    def get_objectives_by_user(self, user_id: int) -> List[ObjectiveModel]:
        return self.db.query(ObjectiveModel).filter(ObjectiveModel.user_id == user_id).all()

    def update_objective(self,
                         objective_id: int,
                         name: Optional[str] = None,
                         description: Optional[str] = None,
                         priority: Optional[int] = None,
                         current_level: Optional[str] = None,
                         target_level: Optional[str] = None) -> Optional[ObjectiveModel]:
        objective = self.get_objective(objective_id)
        if not objective:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Objective not found"
            )

        if name:
            objective.name = name
        if description:
            objective.description = description
        if priority:
            objective.priority = priority
        if current_level:
            objective.current_level = current_level
        if target_level:
            objective.target_level = target_level

        self.db.commit()
        self.db.refresh(objective)
        return objective
