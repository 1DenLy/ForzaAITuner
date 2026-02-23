import pytest
from unittest.mock import patch
from desktop_client.presentation.services.ui_loader_service import UiLoaderService

def test_load_ui_invalid_extension(tmp_path, qapp):
    # Левое расширение файла
    test_file = tmp_path / "config.json"
    test_file.touch()

    with patch('desktop_client.presentation.services.ui_loader_service.SecurityUtils.validate_safe_path', return_value=test_file):
        with pytest.raises(ValueError, match="Invalid file extension"):
            UiLoaderService.load_ui(str(test_file))

def test_load_ui_invalid_xml(tmp_path, qapp):
    # Битый XML / Ошибка Qt
    empty_ui = tmp_path / "empty.ui"
    empty_ui.write_text("Hello")

    with patch('desktop_client.presentation.services.ui_loader_service.SecurityUtils.validate_safe_path', return_value=empty_ui):
        with patch('desktop_client.presentation.services.ui_loader_service.SecurityUtils.validate_file_size'):
            with pytest.raises(RuntimeError, match="(Loader failed to load|Unable to open/read ui device)"):
                UiLoaderService.load_ui(str(empty_ui))

def test_load_ui_file_not_found(tmp_path, qapp):
    missing_file = tmp_path / "missing.ui"
    
    with patch('desktop_client.presentation.services.ui_loader_service.SecurityUtils.validate_safe_path', return_value=missing_file):
        with pytest.raises(FileNotFoundError, match="UI file not found"):
            UiLoaderService.load_ui(str(missing_file))
