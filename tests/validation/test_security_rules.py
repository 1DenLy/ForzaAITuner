import pytest
from pathlib import Path
from desktop_client.validation import PathValidator, FileSizeValidator, ValidationResult

def test_path_validator_detects_path_traversal(tmp_path):
    # Arrange
    base_dir = tmp_path / "app" / "ui"
    base_dir.mkdir(parents=True)
    validator = PathValidator(base_dir)
    
    # Act
    # Path Traversal - Relative
    attack_path = "../../windows/system32/cmd.exe"
    result = validator.validate(attack_path)
    
    # Assert
    assert result.is_valid is False
    assert result.errors[0].code == "path_traversal"
    assert "outside of allowed directory" in result.errors[0].message

def test_path_validator_detects_prefix_spoofing(tmp_path):
    # Arrange
    base_dir = tmp_path / "app" / "ui"
    base_dir.mkdir(parents=True)
    validator = PathValidator(base_dir)
    
    # Prefix Spoofing folder
    spoofed_dir = tmp_path / "app" / "ui_hacked"
    spoofed_dir.mkdir(parents=True)
    bomb_path = spoofed_dir / "bomb.ui"
    
    # Act
    result = validator.validate(bomb_path)
    
    # Assert
    assert result.is_valid is False
    assert result.errors[0].code == "path_traversal"

def test_file_size_validator_detects_huge_file(tmp_path):
    # Arrange
    bomb_file = tmp_path / "huge_bomb.ui"
    # Create 1.1 MB file, max set to 1 MB
    with open(bomb_file, "wb") as f:
        f.seek(1 * 1024 * 1024 + 100) 
        f.write(b"0")
    
    validator = FileSizeValidator(max_bytes=1 * 1024 * 1024)
        
    # Act
    result = validator.validate(bomb_file)
    
    # Assert
    assert result.is_valid is False
    assert result.errors[0].code == "file_too_large"

def test_file_size_validator_fails_on_missing_file(tmp_path):
    # Arrange
    missing_file = tmp_path / "ghost.json"
    validator = FileSizeValidator()

    # Act
    result = validator.validate(missing_file)

    # Assert
    assert result.is_valid is False
    assert result.errors[0].code == "not_found"

def test_path_validator_success(tmp_path):
    # Arrange
    base_dir = tmp_path / "app" / "ui"
    base_dir.mkdir(parents=True)
    valid_file = base_dir / "valid.ui"
    valid_file.touch()
    validator = PathValidator(base_dir)
    
    # Act
    result = validator.validate(str(valid_file))
    
    # Assert
    assert result.is_valid is True
    assert result.data == valid_file.resolve()
