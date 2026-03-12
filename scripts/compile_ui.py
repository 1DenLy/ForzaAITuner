"""
AOT compilation script for .ui -> .py using pyside6-uic.
Run as part of CI/CD setup or initial project bootstrapping:

    python scripts/compile_ui.py

Generated .py files are placed in:
    src/desktop_client/presentation/ui/generated/

The generated files should be committed to version control so that
at runtime no QUiLoader is needed (faster startup, strict typing).
"""
import subprocess
import sys
from pathlib import Path

# Project root is two levels up from this script
ROOT = Path(__file__).resolve().parent.parent

# Source directory with .ui files
ASSETS_DIR = ROOT / "src" / "desktop_client" / "presentation" / "ui" / "forms"

# Output directory for generated .py files
OUTPUT_DIR = ROOT / "src" / "desktop_client" / "presentation" / "ui" / "generated"

# Maps .ui filename -> generated .py filename
UI_FILES = {
    "api_v1.1.ui": "ui_main_window.py",
    "config_dialog.ui": "ui_config_dialog.py",
    "settings_dialog.ui": "ui_settings_dialog.py",
    "config_library.ui": "ui_config_library.py",
    "list widget.ui": "ui_list_widget.py",
}


def compile_ui():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create __init__.py so the folder is a proper package
    init_file = OUTPUT_DIR / "__init__.py"
    if not init_file.exists():
        init_file.write_text(
            "# Auto-generated UI package. Do not edit manually.\n"
        )

    errors = []

    for ui_name, py_name in UI_FILES.items():
        ui_path = ASSETS_DIR / ui_name
        out_path = OUTPUT_DIR / py_name

        if not ui_path.exists():
            print(f"[SKIP]  {ui_name} not found at {ui_path}")
            continue

        print(f"[COMPILE] {ui_name} -> {py_name}")
        result = subprocess.run(
            ["pyside6-uic", str(ui_path), "-o", str(out_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"[ERROR] Failed to compile {ui_name}:\n{result.stderr}")
            errors.append(ui_name)
        else:
            print(f"[OK]    Written to {out_path.relative_to(ROOT)}")

    if errors:
        print(f"\nCompilation finished with {len(errors)} error(s): {errors}")
        sys.exit(1)
    else:
        print("\nAll .ui files compiled successfully.")


if __name__ == "__main__":
    compile_ui()
