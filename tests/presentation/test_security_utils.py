import pytest
import os
from pathlib import Path
from desktop_client.presentation.helpers.security_utils import SecurityUtils, MAX_FILE_SIZE_BYTES

def test_validate_safe_path_detects_path_traversal(tmp_path):
    # Arrange
    base_dir = tmp_path / "app" / "ui"
    base_dir.mkdir(parents=True)
    
    # Act & Assert
    # Path Traversal - Relative
    attack_path = "../../windows/system32/cmd.exe"
    
    with pytest.raises(PermissionError) as exc_info:
        SecurityUtils.validate_safe_path(attack_path, base_dir)
        
    assert "Path traversal attempt blocked" in str(exc_info.value)

def test_validate_safe_path_detects_prefix_spoofing(tmp_path):
    # Arrange
    base_dir = tmp_path / "app" / "ui"
    base_dir.mkdir(parents=True)
    
    # Prefix Spoofing folder
    spoofed_dir = tmp_path / "app" / "ui_hacked"
    spoofed_dir.mkdir(parents=True)
    bomb_path = spoofed_dir / "bomb.ui"
    
    # Act & Assert
    with pytest.raises(PermissionError) as exc_info:
        SecurityUtils.validate_safe_path(bomb_path, base_dir)
        
    assert "Path traversal attempt blocked" in str(exc_info.value)

def test_validate_file_size_detects_xml_bomb(tmp_path):
    # Arrange
    bomb_file = tmp_path / "huge_bomb.ui"
    
    # Создать временный файл размером 5.1 МБ (забить нулями)
    with open(bomb_file, "wb") as f:
        f.seek(5 * 1024 * 1024 + 100 * 1024) # 5.1 MB
        f.write(b"0")
        
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        SecurityUtils.validate_file_size(bomb_file)
        
    assert "Security Error: File" in str(exc_info.value)
    assert "exceeds the maximum allowed size" in str(exc_info.value)

def test_validate_safe_path_success(tmp_path):
    # Arrange
    base_dir = tmp_path / "app" / "ui"
    base_dir.mkdir(parents=True)
    valid_file = base_dir / "valid.ui"
    valid_file.touch()
    
    # Act
    result = SecurityUtils.validate_safe_path(str(valid_file), base_dir)
    
    # Assert
    assert result == valid_file.resolve()
