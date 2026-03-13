from pathlib import Path
from .models import ValidationResult, ValidationError, ValidationErrorCode

class PathValidator:
    """Validator for path security (protection against path-traversal)."""
    def __init__(self, base_dir: str | Path):
        self._base_dir = Path(base_dir).resolve()

    def validate(self, data: str | Path) -> ValidationResult[Path]:
        try:
            target = Path(data).resolve()
            if not target.is_relative_to(self._base_dir):
                return ValidationResult(
                    is_valid=False, 
                    errors=(ValidationError(ValidationErrorCode.PATH_TRAVERSAL, "Access denied: Path is outside of allowed directory!"),)
                )
            return ValidationResult(is_valid=True, data=target)
        except Exception as e:
            return ValidationResult(
                is_valid=False, 
                errors=(ValidationError(ValidationErrorCode.PATH_ERROR, f"Path processing error: {str(e)}"),)
            )

class FileSizeValidator:
    """
    Validator for limiting upload file sizes.
    
    NOTE: There is a TOCTOU (Time-of-Check to Time-of-Use) risk. 
    For critical operations, it is recommended to check the size 
    of an already opened file descriptor via os.fstat(fd).st_size.
    """
    def __init__(self, max_bytes: int = 5 * 1024 * 1024):
        self._max_bytes = max_bytes

    def validate(self, data: Path) -> ValidationResult[Path]:
        try:
            if not data.exists() or not data.is_file():
                return ValidationResult(
                    is_valid=False, 
                    errors=(ValidationError(ValidationErrorCode.NOT_FOUND, "File not found or it is a directory."),)
                )
            
            # NOTE: data.stat() might return data for a file 
            # that changes before the open() call in the application.
            if data.stat().st_size > self._max_bytes:
                return ValidationResult(
                    is_valid=False, 
                    errors=(ValidationError(ValidationErrorCode.FILE_TOO_LARGE, f"File size exceeds {self._max_bytes} bytes."),)
                )
            return ValidationResult(is_valid=True, data=data)
        except OSError as e:
            return ValidationResult(
                is_valid=False, 
                errors=(ValidationError(ValidationErrorCode.OS_ERROR, f"File access error: {str(e)}"),)
            )