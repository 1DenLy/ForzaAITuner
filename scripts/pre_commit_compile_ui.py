"""
pre-commit hook: проверяет, что .ui -> .py файлы актуальны.

Логика:
  1. Если среди staged-файлов есть изменённый .ui — запускает compile_ui.py.
  2. После компиляции добавляет сгенерированные .py в индекс (git add).
  3. Если compile_ui.py завершился с ошибкой — коммит блокируется.

Использование (через .pre-commit-config.yaml):
  hooks:
    - id: compile-ui
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Пути к .ui и сгенерированным .py — должны совпадать с compile_ui.py
ASSETS_DIR = ROOT / "src" / "desktop_client" / "presentation" / "assets"
OUTPUT_DIR = ROOT / "src" / "desktop_client" / "presentation" / "ui_gen"

UI_FILES = {
    "api_v1.1.ui":       "ui_main_window.py",
    "config_dialog.ui":  "ui_config_dialog.py",
    "settings_dialog.ui":"ui_settings_dialog.py",
}


def get_staged_files() -> list[str]:
    """Возвращает список файлов в индексе (staged)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True, cwd=ROOT,
    )
    return result.stdout.splitlines()


def main() -> int:
    staged = get_staged_files()
    staged_ui = [f for f in staged if f.endswith(".ui")]

    if not staged_ui:
        # Нет изменённых .ui — хук не нужен
        return 0

    print(f"[pre-commit] Обнаружены изменённые .ui файлы: {staged_ui}")
    print("[pre-commit] Запускаю компиляцию .ui -> .py ...")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "compile_ui.py")],
        cwd=ROOT,
    )

    if result.returncode != 0:
        print("[pre-commit] [ERROR] Компиляция завершилась с ошибкой. Коммит заблокирован.")
        return 1

    # Добавляем сгенерированные файлы в индекс автоматически
    generated = [
        str((OUTPUT_DIR / py_name).relative_to(ROOT))
        for ui_name, py_name in UI_FILES.items()
        if (ASSETS_DIR / ui_name).exists() and (OUTPUT_DIR / py_name).exists()
    ]
    if generated:
        subprocess.run(["git", "add"] + generated, cwd=ROOT)
        print(f"[pre-commit] [OK] Добавлены в индекс: {generated}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
