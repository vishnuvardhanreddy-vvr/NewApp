import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Get the log level from the environment variable, default to 'INFO'
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Ensure the log level is valid
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        log_level = 'INFO'  # Default to INFO if invalid level

    # Flag to write INFO logs to the file (from env var or default)
    log_info_to_file = os.getenv("LOG_INFO_TO_LOGS_FILE", False)

    # Set up log file rotation
    log_file = os.getenv("LOG_FILE", "app_logs.log")

    # Remove existing handlers if any (to avoid duplication)
    logging.root.handlers = []

    # Set up log file rotation (write only ERROR and above by default)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )  # 10 MB per log file, keep 5 backups

    # If INFO logs should be written to file, set the level accordingly
    if log_info_to_file:
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'))
    else:
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Get the logger instance
    logger = logging.getLogger()

    # Always log to the file handler
    logger.addHandler(file_handler)

    # Set up console logging (for both DEBUG and higher)
    console_handler = logging.StreamHandler()
    if log_level == "DEBUG":
        # For DEBUG, log to console with full details (file, line number)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'))
    else:
        # For INFO or higher, log to console without file name/line number
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Add the console handler, but make sure it's not duplicating
    logger.addHandler(console_handler)

    # Set the logger's level (to decide console logging)
    logger.setLevel(log_level)

    # Log that setup is complete (this message should only appear once)
    logger.info("Logging setup complete with level '%s'.", log_level)

    return logger