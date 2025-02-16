# -*- coding: utf-8 -*-
from abc import ABC
from typing import Dict, List, Optional

from openai import OpenAI

from settings import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME


class BaseAIAgent(ABC):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化 BaseAIAgent。

        Args:
            api_key: OpenAI API 密钥。如果为 None，则从 settings.py 中读取。
            base_url: OpenAI API 的 base URL。如果为 None，则从 settings.py 中读取。
        """
        api_key = api_key or OPENAI_API_KEY
        base_url = base_url or OPENAI_BASE_URL

        if not api_key:
            raise ValueError("OpenAI API key is required. "
                             "Please set it in settings.py or pass it as an argument.")
        if not base_url:
            print("UserWarning: OpenAI Base URL is not set. Using it may cause some error")

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        使用 OpenAI 的 Chat Completions API 生成回复。

        Args:
            messages: 一个消息列表，每个消息是一个字典，包含 "role" (system, user, assistant) 和 "content"。

        Returns:
            LLM 的回复内容。
        """
        response = self.client.chat.completions.create(
            model=MODEL_NAME,  # 你可以根据需要更改模型
            messages=messages
        )
        return response.choices[0].message.content.strip()
