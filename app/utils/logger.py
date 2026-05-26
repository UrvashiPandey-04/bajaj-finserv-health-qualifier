import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Setup logs directory in the project root
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

# Define log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"

def setup_logger(name: str = "bajaj_qualifier") -> logging.Logger:
    """
    Configures and returns a logging instance.
    Logs will output to both stdout (console) and a local log file.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if setup_logger is called multiple times
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)

    # 1. Console Handler (Standard Output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "\033[1;36m[App]\033[0m %(asctime)s - \033[1;33m%(levelname)s\033[0m - %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 2. Rotating File Handler (Production Logs)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

# Globally available logger instance
logger = setup_logger()
