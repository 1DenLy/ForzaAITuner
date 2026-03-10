import dataclasses

@dataclasses.dataclass(frozen=True, slots=True)
class BackendErrorEvent:
    """
    Event triggered when the backend API encounters an error (network or HTTP status).
    """
    code: int           # HTTP Status or internal code
    message: str        # Human-readable, SANITIZED error message
    is_transient: bool  # Whether it's a retryable network issue
