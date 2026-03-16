import pytest
from unittest.mock import patch, MagicMock

from desktop_client.presentation.viewmodels.config_viewmodel import ConfigViewModel
from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.application.config_state_manager import ConfigStateManager
from desktop_client.domain.tuning_defaults import TuningDefaults
from desktop_client.application.exceptions import ConfigLockedError

@pytest.fixture
def validator_mock():
    return MagicMock(spec=ConfigValidatorService)

@pytest.fixture
def state_manager_mock():
    return MagicMock(spec=ConfigStateManager)

@pytest.fixture
def preset_repository_mock():
    return MagicMock()

@pytest.fixture
def view_model(validator_mock, state_manager_mock, preset_repository_mock):
    return ConfigViewModel(validator_mock, state_manager_mock, preset_repository_mock)

def test_get_last_valid_config_no_config(view_model, state_manager_mock):
    state_manager_mock.get_config.return_value = None
    data = view_model.get_last_valid_config()
    assert data == TuningDefaults.as_dict()

def test_get_last_valid_config_with_config(view_model, state_manager_mock):
    config_mock = MagicMock()
    config_mock.model_dump.return_value = {"tires": {"front_pressure_bar": 2.0}}
    state_manager_mock.get_config.return_value = config_mock
    
    data = view_model.get_last_valid_config()
    assert data == {"tires": {"front_pressure_bar": 2.0}}

def test_apply_config_validation_failed(view_model, validator_mock, qtbot):
    result_mock = MagicMock()
    result_mock.is_valid = False
    result_mock.errors = {
        "tires -> front_pressure_bar": "Error msg",
        "__root__": "Global error"
    }
    validator_mock.validate.return_value = result_mock

    with qtbot.waitSignal(view_model.validation_failed) as blocker:
        view_model.apply_config({"raw": "data"})
    
    # blocker.args contains the emitted arguments: [field_errors, global_errors]
    assert blocker.args == [{"tires.front_pressure_bar": "Error msg"}, ["Global error"]]

def test_apply_config_success(view_model, validator_mock, state_manager_mock, qtbot):
    result_mock = MagicMock()
    result_mock.is_valid = True
    result_mock.data = {"valid": "data"}
    validator_mock.validate.return_value = result_mock

    with qtbot.waitSignal(view_model.config_saved) as blocker:
        view_model.apply_config({"raw": "data"})
    
    state_manager_mock.update_config.assert_called_once_with({"valid": "data"})

def test_apply_config_locked_error(view_model, validator_mock, state_manager_mock, qtbot):
    result_mock = MagicMock()
    result_mock.is_valid = True
    result_mock.data = {"valid": "data"}
    validator_mock.validate.return_value = result_mock
    
    state_manager_mock.update_config.side_effect = ConfigLockedError("Locked!")

    with qtbot.waitSignal(view_model.global_error_occurred) as blocker:
        view_model.apply_config({"raw": "data"})
    
    assert blocker.args == ["Locked!"]

def test_load_config_from_file_success(view_model, preset_repository_mock, qtbot):
    # Setup mock file reading
    valid_json = TuningDefaults.as_dict()
    import json
    preset_repository_mock.load_preset.return_value = json.dumps(valid_json)

    with qtbot.waitSignal(view_model.preset_loaded) as blocker:
        view_model.load_config_from_file("dummy_path")
    
    # The loaded dictionary should equal our defaults
    assert blocker.args == [valid_json]

def test_load_config_from_file_validation_error(view_model, preset_repository_mock, qtbot):
    preset_repository_mock.load_preset.return_value = '{"tires": {"front_pressure_bar": "INVALID_FLOAT"}}'

    with qtbot.waitSignal(view_model.global_error_occurred) as blocker:
        view_model.load_config_from_file("dummy_path")
    
    assert "Ошибка содержимого файла пресета" in blocker.args[0]

def test_load_config_from_file_read_error(view_model, preset_repository_mock, qtbot):
    preset_repository_mock.load_preset.side_effect = FileNotFoundError("Not found")

    with qtbot.waitSignal(view_model.global_error_occurred) as blocker:
        view_model.load_config_from_file("dummy_path")
    
    assert "Ошибка безопасности/поиска файла" in blocker.args[0]

def test_load_config_from_file_security_violation(view_model, preset_repository_mock, qtbot):
    preset_repository_mock.load_preset.side_effect = PermissionError("Access denied")

    with qtbot.waitSignal(view_model.global_error_occurred) as blocker:
        view_model.load_config_from_file("dummy_path")
            
    assert "Ошибка безопасности/поиска" in blocker.args[0]
