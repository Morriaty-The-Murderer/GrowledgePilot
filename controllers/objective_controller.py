# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from models.objective import ObjectiveModel


def create_objective(db: Session, user_id: int, name: str, description: str, priority: int, current_level: str,
                     target_level: str):
    db_obj = ObjectiveModel(user_id=user_id, name=name, description=description, priority=priority,
                            current_level=current_level, target_level=target_level)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_objective(db: Session, objective_id: int):
    return db.query(ObjectiveModel).filter(ObjectiveModel.id == objective_id).first()


def get_objectives_by_user(db: Session, user_id: int):
    return db.query(ObjectiveModel).filter(ObjectiveModel.user_id == user_id).all()


def update_objective(db: Session, objective_id: int, name: str = None, description: str = None, priority: int = None,
                     current_level: str = None, target_level: str = None):
    objective = get_objective(db, objective_id)
    if objective:
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
        db.commit()
        db.refresh(objective)
    return objective
