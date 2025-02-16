# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from controllers.objective_controller import ObjectiveController
from controllers.user_controller import UserController
from .base import BaseAIAgent


class LearningAgent(BaseAIAgent):
    def __init__(self, user_id: int, objective_id: int, db: Session):
        super().__init__()
        self.user_id = user_id
        self.objective_id = objective_id
        self.db = db
        self.user_controller = UserController(db)
        self.objective_controller = ObjectiveController(db)

    def generate_learning_response(self, user_input: str, prompt_template: str) -> str:
        user = self.user_controller.get_user(self.user_id)
        objective = self.objective_controller.get_objective(self.objective_id)

        if not user or not objective:
            return "User or objective not found."

            # 构建 messages 列表
        messages = [
            {
                "role": "system",
                "content": prompt_template.format(
                    user_name=user.name,
                    objective_name=objective.name,  # type: ignore
                    current_level=objective.current_level,  # type: ignore
                    target_level=objective.target_level,  # type: ignore
                    objective_description=objective.description,  # type: ignore
                    user_occupation=user.occupation,
                    user_age=user.age
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = self.generate_response(messages)

        # 在这里添加后处理逻辑，例如：
        # - 提取关键信息
        # - 格式化输出
        # - 更新学习进度 (调用 learning_controller 中的方法)
        # - 调用第三方 API (如果需要)

        return response
