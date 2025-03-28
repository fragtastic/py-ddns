import logging
import sys
import os

# Get log level from env (default to INFO)
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
if log_level_str not in logging.getLevelNamesMapping():
    print(f'Invalid log level "{log_level_str}", defaulting to INFO')
log_level = getattr(logging, log_level_str, logging.INFO)

base_logger = logging.getLogger("ddns")
base_logger.setLevel(log_level)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(provider)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

base_logger.addHandler(handler)
base_logger.propagate = False

def getLoggerAdapter(loggerName: str):
    return logging.LoggerAdapter(base_logger, {"provider": loggerName})
