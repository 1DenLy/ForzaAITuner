import structlog
import logging
import sys
from typing import Any, MutableMapping

def _security_filter(logger: Any, method_name: str, event_dict: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
    """
    Filter sensitive keys from logs.
    """
    SENSITIVE_KEYS = {"password", "dsn", "token", "secret"}
    for key in event_dict:
        if key.lower() in SENSITIVE_KEYS:
            event_dict[key] = "***"
    return event_dict

def setup_logging(env: str) -> None:
    """
    Configure structlog based on environment.
    """
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        _security_filter,
    ]

    if env in ("local", "development"):
        # Development: Colored Console
        processors.extend([
            structlog.dev.ConsoleRenderer()
        ])
    else:
        # Production: JSON
        processors.extend([
            structlog.processors.JSONRenderer()
        ])

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to redirect to structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
