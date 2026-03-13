from pathlib import Path

# Hard upper limit for external files (presets, assets etc.).
# Protects against DoS / OOM attacks when reading unknown files.
MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MiB


class SecurityUtils:
    """
    Utility class for security-related checks in the Presentation Layer.
    Single Responsibility: only validates path safety and file constraints.
    """

    @staticmethod
    def validate_safe_path(target_path: str | Path, base_dir: Path) -> Path:
        """
        Resolves *target_path* and ensures it is located within *base_dir*,
        preventing path-traversal attacks.

        The check uses ``Path.is_relative_to()`` (Python ≥ 3.9), which compares
        path *components*, not raw strings.  This closes the classic
        ``startswith`` vulnerability where "/app/ui_fake" would falsely match
        the prefix "/app/ui".

        Args:
            target_path: The path to verify (absolute or relative).
            base_dir:    The project root / allowed base directory.

        Returns:
            The resolved, safe ``Path`` object.

        Raises:
            PermissionError: If the resolved path is outside *base_dir*.
        """
        resolved = Path(target_path).resolve()
        base_resolved = Path(base_dir).resolve()

        if not resolved.is_relative_to(base_resolved):
            raise PermissionError(
                f"Security Error: Path traversal attempt blocked for '{target_path}'"
            )

        return resolved

    @staticmethod
    def validate_file_size(path: Path, max_bytes: int = MAX_FILE_SIZE_BYTES) -> None:
        """
        Ensures *path* does not exceed *max_bytes* before it is opened by any
        parser / loader, guarding against XML-bomb / OOM denial-of-service.

        Args:
            path:      Resolved ``Path`` object to check.
            max_bytes: Maximum allowed file size in bytes (default: 5 MiB).

        Raises:
            ValueError: If the file exceeds *max_bytes*.
        """
        size = path.stat().st_size
        if size > max_bytes:
            max_mb = max_bytes / (1024 * 1024)
            actual_mb = size / (1024 * 1024)
            raise ValueError(
                f"Security Error: File '{path.name}' is {actual_mb:.1f} MiB, "
                f"which exceeds the maximum allowed size of {max_mb:.0f} MiB."
            )
