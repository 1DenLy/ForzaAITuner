from typing import Protocol, TypeVar, Any
from .models import ValidationResult

T = TypeVar("T_contra", contravariant=True)
R = TypeVar("R_co", covariant=True)

class ValidatorProtocol(Protocol[T, R]):
    def validate(self, data: T) -> ValidationResult[R]:
        """Unified method for all validators"""
        ...