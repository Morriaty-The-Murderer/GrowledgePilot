# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL  # 导入 settings.py 中的数据库配置

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    获取数据库会话的依赖项。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库（创建表）。
    """
    from models.base import Base  # 导入所有模型，以确保它们被注册到元数据中
    from models.user import UserModel  # 导入所有模型，以确保它们被注册到元数据中
    from models.objective import ObjectiveModel
    from models.learning_session import LearningSessionModel

    Base.metadata.create_all(bind=engine)
