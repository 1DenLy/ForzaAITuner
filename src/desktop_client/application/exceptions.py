"""
Exceptions related to the application layer.
"""

class SecurityViolationError(Exception):
    """Exception raised for security violations like Path Traversal or DoS attempts."""
    pass

class ConfigLockedError(Exception):
    """Exception raised when attempting to modify configuration while it is locked."""
    pass
