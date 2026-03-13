import os
from pathlib import Path
from desktop_client.presentation.interfaces.protocols import IPresetRepository
from desktop_client.presentation.helpers.security_utils import SecurityUtils


class LocalPresetRepository(IPresetRepository):
    """
    Concrete implementation of IPresetRepository for local file system.
    Responsible for secure file reading of JSON presets.
    """
    def __init__(self, base_dir: Path):
        self._base_dir = base_dir

    def load_preset(self, filepath: str) -> str:
        # 1. Security Validation: Path Traversal & DoS (File size)
        safe_path = SecurityUtils.validate_safe_path(filepath, self._base_dir)
        SecurityUtils.validate_file_size(safe_path)

        # 2. Reading
        text = safe_path.read_text(encoding="utf-8")
        return text
