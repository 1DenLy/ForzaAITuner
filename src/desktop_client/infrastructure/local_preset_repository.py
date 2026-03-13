from desktop_client.presentation.interfaces.protocols import IPresetRepository
from desktop_client.validation import PathValidator, FileSizeValidator


class LocalPresetRepository(IPresetRepository):
    """
    Concrete implementation of IPresetRepository for local file system.
    Responsible for secure file reading of JSON presets.
    """
    def __init__(self, path_validator: PathValidator, size_validator: FileSizeValidator):
        self._path_validator = path_validator
        self._size_validator = size_validator

    def load_preset(self, filepath: str) -> str:
        # 1. Path Validation
        path_res = self._path_validator.validate(filepath)
        if not path_res.is_valid:
            raise PermissionError(f"Security Error: {path_res.errors[0].message}")
        
        safe_path = path_res.data

        # 2. File Size Validation
        size_res = self._size_validator.validate(safe_path)
        if not size_res.is_valid:
            raise ValueError(f"Security Error: {size_res.errors[0].message}")

        # 3. Reading
        return safe_path.read_text(encoding="utf-8")
