"""
@ coding : utf-8 
@Time    : 2025/10/25 14:48
@Author  : admin
@Project : fastapi_wms
@File    : logger.py
@Software: PyCharm
@Notes   : 日志工具配置
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = r"D:\sync\PythonProject\fastapi_wms\logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 日志文件路径
LOG_FILE = os.path.join(LOG_DIR, "app.log")
# 创建logger
logger = logging.getLogger("fastapi_wms")
logger.setLevel(logging.DEBUG)
# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# 文件输出
file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=7, encoding="utf-8")
file_handler.suffix = "%Y-%m-%d"
# 统一格式
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
# 绑定handler
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)