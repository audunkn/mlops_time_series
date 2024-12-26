import os
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

def load_env_vars(root_dir: Union[str, Path]) -> dict: # argument can be either string or a Path object
    """
    Load environemnt variables from .env file.
    
    Args:
        root_dir: Root directory of the .env file. Can be a string or a Path object
        
    Returns:
        Dictionary with the environnment variables loaded from the env file.
    """

    if isinstance (root_dir, str): # Checks if the root_dir argument is of type str
        root_dir = Path (root_dir) # If root_dir is a string, it converts it into a Path object
        
    
    load_dotenv(dotenv_path=root_dir / ".env")
    # Constructs the full path to the .env file by appending ".env" to the root_dir
    # Calls load_dotenv with the path to the .env file. 
    # Reads the .env file and loads its key-value pairs into the process's environment variables

    
    return dict(os.environ)
    # Converts the os.environ object (a mapping object containing all environment variables) into a dictionary and returns it. 
    # This dictionary includes both existing system environment variables and those loaded from the .env file

    def get_root_dir(default_value: ".") -> Path:
        """
        Get the root directory of the project.
        Args:
            default_value: Default value to use if the environment variable is not set.
        Returns: 
            Path to the root directory of the project
        """

        return Path(os.getenv("ML_PIPELINE_ROOT_DIR", default_value))

        ML_PIPELINE_ROOT_DIR = get_root_dir() # Calls the get_root_dir function to determine the root directory of the project. 
        # If the environment variable ML_PIPELINE_ROOT_DIR is set, its value is used. If not, the default value "." is used, pointing to the current directory.
        
        OUTPUTS_DIR = ML_PIPELINE_ROOT_DIR / "output" # Appends "output" to the ML_PIPELINE_ROOT_DIR path using the / operator, which is a feature of the Path object.

        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True) # Creates the directory represented by OUTPUT_DIR on the filesystem.
        # parents=True: Ensures that any missing parent directories are created automatically.
        # exist_ok=True: Prevents errors if the directory already exists.

        SETTINGS = load_env_vars(root_dir=ML_PIPELINE_ROOT_DIR) # Calls the load_env_vars function with the root directory as an argument