# -*- coding: utf-8 -*-
import sys
from loguru import logger
from settings import LOG_LEVEL, LOGS_DIR

# 日志格式
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# 日志配置
logger.remove()  # 移除默认的 handler
logger.add(sys.stderr, format=LOG_FORMAT, level=LOG_LEVEL)  # 添加到标准错误输出
logger.add(f"{LOGS_DIR}/app_{{time}}.log", format=LOG_FORMAT, level=LOG_LEVEL, rotation="500 MB")  # 添加到文件
