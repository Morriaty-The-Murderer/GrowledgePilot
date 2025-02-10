# -*- coding: utf-8 -*-
# built-in packages

# third-party packages
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

# self-defined packages
from .base import Base, BaseMixin  # 导入上一步创建的 base.py


class UserModel(Base, BaseMixin):
    __tablename__ = "users"

    name = Column(String, index=True)
    age = Column(Integer)
    occupation = Column(String)
    objectives = relationship("ObjectiveModel", back_populates="user")
    # objectives = Column(MutableList.as_mutable(JSON), default=[]) # 使用JSON存储，更灵活
    created_at = Column(DateTime)
    last_login = Column(DateTime)
