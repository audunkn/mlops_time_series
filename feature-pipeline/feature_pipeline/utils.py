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


    def save_json(data: dict, file_name: str, save_dir: str = settings.OUTPUT_DIR): # settings.OUTPUT_DIR is default value for save_dir
    """
    Save a dictionary as a JSON file.

    Args:
        data: data to save.
        file_name: Name of the JSON file.
        save_dir: Directory to save the JSON file.

    Returns: None
    """

    data_path = Path(save_dir) / file_name # creates the complete file path by combining the directory and filename
    with open(data_path, "w") as f: # context manager (with statement) ensures the file is properly closed even if an error occurs
        json.dump(data, f)


    def load_json(file_name: str, save_dir: str = settings.OUTPUT_DIR) -> dict: 
    """
    Load a JSON file.

    Args:
        file_name: Name of the JSON file.
        save_dir: Directory of the JSON file.

    Returns: Dictionary with the data.
    """

    data_path = Path(save_dir) / file_name
    if not data_path.exists():
        raise FileNotFoundError(f"Cached JSON from {data_path} does not exist.")

    with open(data_path, "r") as f:
        return json.load(f) 