"""
Logger configuration for the automation framework.
"""

import logging
import os
from datetime import datetime
import colorlog


def get_logger(name):
    """
    Get a configured logger instance.
    
    Args:
        name (str): Logger name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler
    log_filename = f"test_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    
    file_handler = logging.FileHandler(log_filepath, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def log_test_start(test_name):
    """Log test start with separator."""
    logger = get_logger("TEST")
    logger.info("=" * 80)
    logger.info(f"STARTING TEST: {test_name}")
    logger.info("=" * 80)


def log_test_end(test_name, status="COMPLETED"):
    """Log test end with separator."""
    logger = get_logger("TEST")
    logger.info("=" * 80)
    logger.info(f"TEST {status}: {test_name}")
    logger.info("=" * 80)