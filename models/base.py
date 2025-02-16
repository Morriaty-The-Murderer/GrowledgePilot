# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建声明基类
Base = declarative_base()


class BaseMixin(object):
    """
    包含所有数据模型都共享的列
    """

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def save(self, db):
        """
        将当前对象保存到数据库
        """
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db):
        """从数据库中删除当前对象。"""
        db.delete(self)
        db.commit()
