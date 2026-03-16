from dataclasses import dataclass, field
from typing import Generic, TypeVar
from enum import Enum

T = TypeVar("T")

class ValidationErrorCode(str, Enum):
    """Standardized validation error codes."""
    PATH_TRAVERSAL = "path_traversal"
    PATH_ERROR = "path_error"
    NOT_FOUND = "not_found"
    FILE_TOO_LARGE = "file_too_large"
    OS_ERROR = "os_error"
    INVALID_TYPE = "invalid_type"
    INVALID_LENGTH = "invalid_length"
    INVALID_FLOAT = "invalid_float"
    NOT_A_DATACLASS = "not_a_dataclass"
    SCHEMA_ERROR = "schema_error"

@dataclass(frozen=True)
class ValidationError:
    code: ValidationErrorCode | str
    message: str
    location: str | None = None

@dataclass(frozen=True)
class ValidationResult(Generic[T]):
    is_valid: bool
    data: T | None = None
    errors: tuple[ValidationError, ...] = field(default_factory=tuple)
    warnings: tuple[ValidationError, ...] = field(default_factory=tuple)