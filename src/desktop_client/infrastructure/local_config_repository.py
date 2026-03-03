"""
Infrastructure layer implementation for configuration management.
"""
import json
import logging
from pathlib import Path
from typing import Any

from desktop_client.application.exceptions import SecurityViolationError

logger = logging.getLogger(__name__)

class LocalConfigRepository:
    """
    Repository for safely storing and loading configuration data from a local JSON file.
    """
    
    def __init__(self, base_dir: Path | str, filename: str = "last_session_config.json") -> None:
        """
        Initializes the repository with a base directory and filename.
        
        Args:
            base_dir (Path | str): The base directory for storing the configuration.
            filename (str): The name of the configuration file.
        """
        self.base_dir = Path(base_dir).resolve()
        self.filename = filename

    def _get_safe_path(self) -> Path:
        """
        Calculates and validates the target configuration file path.
        
        Raises:
            SecurityViolationError: If a Path Traversal attempt is detected.
            
        Returns:
            Path: The resolved and validated file path.
        """
        target_path = (self.base_dir / self.filename).resolve()
        
        # Path Traversal Protection
        if not target_path.is_relative_to(self.base_dir):
            raise SecurityViolationError(
                f"Path Traversal detected: File path '{target_path}' "
                f"must be within base_dir '{self.base_dir}'."
            )
            
        return target_path

    def load_raw_data(self) -> dict[str, Any]:
        """
        Reads and returns the JSON configuration data.
        If the file does not exist, returns an empty dictionary.
        
        Raises:
            SecurityViolationError: If the file is larger than 1MB (DoS protection).
            
        Returns:
            dict[str, Any]: The configuration data as a dictionary.
        """
        file_path = self._get_safe_path()
        
        if not file_path.exists():
            return {}
            
        # DoS Protection: Limit file size to 1MB (1 * 1024 * 1024 bytes)
        max_size_bytes = 1048576
        if file_path.stat().st_size > max_size_bytes:
            logger.warning(
                f"DoS Protection: Configuration file '{self.filename}' "
                f"exceeds the maximum allowed size of 1MB."
            )
            raise SecurityViolationError(
                "DoS Protection: Configuration file exceeds the maximum allowed size of 1MB."
            )
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return {}
                return data
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to read or decode configuration file '{self.filename}': {e}")
            return {}

    def save_raw_data(self, data: dict[str, Any]) -> None:
        """
        Safely saves the data dictionary to the JSON file.
        
        Args:
            data (dict[str, Any]): The configuration data to save.
            
        Raises:
            SecurityViolationError: If a Path Traversal attempt is detected.
        """
        file_path = self._get_safe_path()
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
