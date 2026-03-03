import json
import os
import tempfile
from pathlib import Path

from desktop_client.presentation.interfaces.protocols import IConfigRepository
from config import BASE_DIR

class ConfigRepository(IConfigRepository):
    """
    Service responsible for loading and saving the configuration files.
    """
    def __init__(self, last_config_filename: str = "last_config.json"):
        # Put the last valid configuration in a standard place.
        self._last_config_path = BASE_DIR / last_config_filename

    def get_last_config_path(self) -> str:
        return str(self._last_config_path)

    def save_config(self, config_data: dict) -> str:
        """
        Saves the config data as JSON to the last config file path using an atomic write.
        Protects against data corruption from crashes/power outages during write operations.
        """
        try:
            # Create a temporary file in the same directory to ensure it's on the same filesystem
            fd, tmp_path = tempfile.mkstemp(dir=self._last_config_path.parent, prefix=".config_", suffix=".tmp", text=True)
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
            # Atomically replace the target file with the new temporary file
            os.replace(tmp_path, self._last_config_path)
            return str(self._last_config_path)
        except (OSError, IOError) as e:
            raise IOError(f"Filesystem error while saving config: {str(e)}") from e
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid configuration data. Cannot serialize to JSON: {str(e)}") from e
