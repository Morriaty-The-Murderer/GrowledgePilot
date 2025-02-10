from sqlalchemy.orm import Session
from models.user import UserModel
from utils.database import get_db
from fastapi import Depends


# def create_user(db: Session, name: str, age: int, occupation: str, objectives: list = None):
def create_user(db: Session, name: str, age: int, occupation: str):
    """
    创建新用户。
    """
    db_user = UserModel(name=name, age=age, occupation=occupation)
    # db_user = UserModel(name=name, age=age, occupation=occupation, objectives=objectives)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    """
    根据用户ID获取用户。
    """
    return db.query(UserModel).filter(UserModel.id == user_id).first()

# def get_user_by_name(db: Session, name: str): # 暂时移除
#     return db.query(UserModel).filter(UserModel.name == name).first()
