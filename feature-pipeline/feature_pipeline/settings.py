import os
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

def load_env_vars(root_dir: Union[str, Path]) -> dict:
    """
    Load environemnt variables from .env file.
    
    Args:
        root_dir: Root directory of the .env file. Can be a string or a Path object
        
    Returns:
        Dictionary with the environnment variables loaded from the env file.
    """

    if isinstance (root_dir, str): 
        root_dir = Path (root_dir) 
        
    
    load_dotenv(dotenv_path=root_dir / ".env")
    
    
    return dict(os.environ)
    
    def get_root_dir(default_value: ".") -> Path:
        """
        Get the root directory of the project.
        Args:
            default_value: Default value to use if the environment variable is not set.
        Returns: 
            Path to the root directory of the project
        """

        return Path(os.getenv("ML_PIPELINE_ROOT_DIR", default_value))

        ML_PIPELINE_ROOT_DIR = get_root_dir() 
        
        OUTPUTS_DIR = ML_PIPELINE_ROOT_DIR / "output" 

        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True) 

        SETTINGS = load_env_vars(root_dir=ML_PIPELINE_ROOT_DIR) 