from .models import ValidationResult


def format_errors_for_ui(result: ValidationResult) -> tuple[dict[str, str], list[str]]:
    """
    Transforms ValidationResult errors into a format suitable for the UI.
    
    Returns:
    - field_errors: dict[dot_notation_path, message]
    - global_errors: list[message]
    """
    field_errors = {}
    global_errors = []

    for error in result.errors:
        if error.location is None or error.location in ("__root__", ""):
            global_errors.append(error.message)
        else:
            # Ensure dot notation for UI mapping
            cleaned_loc = error.location.replace(" -> ", ".")
            field_errors[cleaned_loc] = error.message

    return field_errors, global_errors
