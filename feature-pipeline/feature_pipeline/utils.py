import json
import logging
from pathlib import Path

from feature_pipeline import settings

def get_logger(name: str) -> logging.Logger:
    """
    Template for getting a logger.

    Args:
        name: Name of the logger.

    Returns: Logger.
    """

    logging.basicConfig(level=logging.INFO) # sensitivity level - captures all informational messages, warnings, and errors, but not debug messages
    logger = logging.getLogger(name) # creates a new logger instance with the given name

    return logger