from loguru import logger

logger.add("logs/critical.log", level="CRITICAL", rotation="10MB")
logger.add("logs/error.log", level="ERROR", rotation="10MB")
logger.add("logs/warning.log", level="WARNING", rotation="10MB")
logger.add("logs/info.log", level="INFO", rotation="10MB")
logger.add("logs/debug.log", level="DEBUG", rotation="10MB")

