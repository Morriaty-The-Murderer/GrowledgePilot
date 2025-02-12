# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 数据库配置
DATABASE_URL = "sqlite:///./data/learning_assistant.db"

# OpenAI API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# 其他 API 密钥 (根据需要添加)
# NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# YAHOO_FINANCE_API_KEY = os.getenv("YAHOO_FINANCE_API_KEY")

# 日志配置
LOG_LEVEL = "DEBUG"  # 可以根据需要调整日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Gradio 配置
GRADIO_HOST = os.getenv("GRADIO_HOST", "127.0.0.1")  # 默认值为 "127.0.0.1"
GRADIO_PORT = int(os.getenv("GRADIO_PORT", "7865"))  # 默认值为 7860，并转换为整数
