import pytest
from PySide6.QtWidgets import QApplication, QSpinBox, QDoubleSpinBox, QSlider
from PySide6.QtCore import Qt

from desktop_client.presentation.mappers.tuning_binder import TuningMapper

# Псевдо-UI для тестов
@pytest.fixture
def mock_ui():
    # Создаем фиктивный объект UI, чтобы TuningMapper мог брать оттуда виджеты
    class MockUI:
        def __init__(self):
            # weight имеет только ограничение gt=0 в домене
            self.spinBox_info_weight = QSpinBox()
            self.spinBox_info_weight.setMinimum(-9999) # Дефолтный мусор Qt Designer
            self.spinBox_info_weight.setMaximum(9999)
            
            # camber имеет ge=-5.0, le=5.0 в домене, умножается на 10 для слайдера
            self.horizontalSlider_alignment_front_camber = QSlider(Qt.Orientation.Horizontal)
            
            # rebound имеет ge=1.0, le=20.0 в домене
            self.doubleSpinBox_damping_rebound_front = QDoubleSpinBox()
            self.doubleSpinBox_damping_rebound_front.setMinimum(-100.0) # Дефолтный мусор
            self.doubleSpinBox_damping_rebound_front.setMaximum(100.0)
            
            # tire pressure имеет ge=1.0, le=3.8 в домене, умножается на 10 для слайдера
            self.horizontalSlider_tire_front_pressure = QSlider(Qt.Orientation.Horizontal)
            
            # aero_front_enabled (checkbox) не имеет ge/le, должен игнорироваться configure_ranges
            # Но не будем его добавлять, чтобы не усложнять.

    return MockUI()

def test_configure_ranges_applies_domain_limits(mock_ui, qapp):
    """
    Проверяет, что TuningMapper.configure_ranges() правильно считывает ge/le из Pydantic (доменной модели)
    и применяет их как minimum() и maximum() к слайдерам и спинбоксам,
    корректно обрабатывая ситуации, когда есть только нижний (gt=0) лимит.
    """
    mapper = TuningMapper()
    mapper.configure_ranges(mock_ui)
    
    # 1. Проверяем spinBox_info_weight (domain: weight=int, ge=1 -> lo=1.0, hi=None)
    # Нижний лимит должен установиться в 1, а верхний остаться старым (9999)
    assert mock_ui.spinBox_info_weight.minimum() == 1
    assert mock_ui.spinBox_info_weight.maximum() == 9999 # Не тронут
    
    # 2. Проверяем doubleSpinBox_damping_rebound_front (domain: ge=1.0, le=20.0)
    assert mock_ui.doubleSpinBox_damping_rebound_front.minimum() == 1.0
    assert mock_ui.doubleSpinBox_damping_rebound_front.maximum() == 20.0
    
    # 3. Проверяем horizontalSlider_alignment_front_camber (domain: ge=-5.0, le=5.0)
    # Так как slider_x10, должно быть -50 и 50
    assert mock_ui.horizontalSlider_alignment_front_camber.minimum() == -50
    assert mock_ui.horizontalSlider_alignment_front_camber.maximum() == 50
    # Проверяем также, что слайдеру установился шаг 1
    assert mock_ui.horizontalSlider_alignment_front_camber.singleStep() == 1
    assert mock_ui.horizontalSlider_alignment_front_camber.pageStep() == 1
    
    # 4. Проверяем horizontalSlider_tire_front_pressure (domain: ge=1.0, le=3.8)
    # slider_x10 -> 10 и 38
    assert mock_ui.horizontalSlider_tire_front_pressure.minimum() == 10
    assert mock_ui.horizontalSlider_tire_front_pressure.maximum() == 38

def test_mapper_preserves_spinbox_step(mock_ui, qapp):
    """
    Проверяет, что спинбоксам не устанавливается принудительно singleStep=1 и pageStep,
    так как это может сломать точно настроенный float шаг из Qt Designer.
    """
    # Настроим кастомный шаг до применения маппера
    mock_ui.doubleSpinBox_damping_rebound_front.setSingleStep(0.1)
    
    mapper = TuningMapper()
    mapper.configure_ranges(mock_ui)
    
    # Шаг должен остаться 0.1
    assert mock_ui.doubleSpinBox_damping_rebound_front.singleStep() == 0.1
