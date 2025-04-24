import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Get the log level from the environment variable, default to 'INFO'
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Validate log level
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        log_level = 'INFO'

    # Control log level for file handler
    log_info_to_file = os.getenv("LOG_INFO_TO_LOGS_FILE", "False").lower() in ("true", "1", "yes")
    log_file = os.getenv("LOG_FILE", "app_logs.log")

    # Remove existing handlers to avoid duplicates
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up the main logger
    logger = logging.getLogger()

    # Set up rotating file handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )

    # Set log level for file handler
    if log_info_to_file:
        file_handler.setLevel(logging.WARNING)  # includes WARNING, ERROR, CRITICAL
    else:
        file_handler.setLevel(logging.ERROR)    # includes only ERROR, CRITICAL

    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
        if log_info_to_file else
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (show everything from log_level and up)
    console_handler = logging.StreamHandler()
    if log_level == "DEBUG":
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
    else:
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Set root logger level
    logger.setLevel(log_level)

    # One-time message
    logger.info("Logging setup complete with level '%s'.", log_level)

    return logger

logger = setup_logging()