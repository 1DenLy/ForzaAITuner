from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable
import logging

from PySide6.QtWidgets import (
    QAbstractSlider,
    QAbstractSpinBox,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QWidget,
)

from desktop_client.presentation.mappers.transformers import (
    slider_x10_to_model, slider_x10_to_ui,
    slider_x1_to_model,  slider_x1_to_ui,
    str_to_bool, bool_to_str,
)
from desktop_client.domain.tuning_defaults import TuningDefaults
from desktop_client.domain.tuning_options import TuningOptions

logger = logging.getLogger(__name__)

# Тип для ui_widgets: генерированный Ui_* объект Qt или словарь для тестов.
# QWidget — наименьший общий предок для генерированных Ui_* классов Qt Designer.
UiSource = QWidget | dict[str, QWidget]

@dataclass
class WidgetBinding:
    """
    Декларативное правило привязки виджета UI к полю Pydantic модели.
    """
    widget_name: str                 # Имя виджета в Qt Designer (напр. "spinBox_info_weight")
    model_path: tuple[str, ...]      # Путь в модели (напр. ("info", "weight"))

    # Функции трансформации (по умолчанию возвращают значение как есть)
    ui_to_model: Callable[[Any], Any] = lambda x: x
    model_to_ui: Callable[[Any], Any] = lambda x: x

    # Имя QLabel для отображения числового значения слайдера (None — не отображать)
    label_name: str | None = field(default=None)

    # Формат отображения в лейбле:
    #   "float" — 1 знак после запятой: "-1.5", "2.1"  (sliders ×10, ось, давление шин)
    #   "int"   — целое:           "50", "33"    (ARB, тормоза, дифференциал)
    label_format: str = field(default="int")

class TuningMapper:
    """
    Класс, содержащий карту привязок и логику двунаправленного обмена данными.
    """
    def __init__(self, extractors: dict[type[QWidget], Callable[[Any], Any]] | None = None,
                 injectors: dict[type[QWidget], Callable[[Any, Any], None]] | None = None):
        # Базовые стратегии извлечения данных
        self.extractors = extractors or {
            QCheckBox: lambda w: w.isChecked(),
            QComboBox: lambda w: w.currentText(),
            QAbstractSpinBox: lambda w: w.value(),
            QAbstractSlider: lambda w: w.value(),
            QLineEdit: lambda w: w.text(),
        }
        
        # Базовые стратегии установки данных
        self.injectors = injectors or {
            QCheckBox: lambda w, v: w.setChecked(bool(v)),
            QComboBox: lambda w, v: w.setCurrentText(str(v)),
            QAbstractSpinBox: lambda w, v: w.setValue(v),
            QAbstractSlider: lambda w, v: w.setValue(v),
            QLineEdit: lambda w, v: w.setText(str(v)),
            QLabel: lambda w, v: w.setText(str(v)),
        }
        
        self.bindings: list[WidgetBinding] = self._init_bindings()

    def register_widget_type(self, widget_type: type[QWidget], 
                             extractor: Callable[[Any], Any], 
                             injector: Callable[[Any, Any], None]) -> None:
        """
        Добавление поддержки новых типов виджетов без изменения кода самого маппера (OCP).
        """
        self.extractors[widget_type] = extractor
        self.injectors[widget_type] = injector

    def _init_bindings(self) -> list[WidgetBinding]:
        """
        Регистрация всех правил привязки.
        Функции трансформации берутся из модуля transformers — они именованы, чистые и покрыты тестами.
        """

        return [
            # ── Session ───────────────────────────────────────────────────────
            WidgetBinding("lineEdit_session_name", ("session", "name")),
            WidgetBinding("lineEdit_session_car", ("session", "car")),
            WidgetBinding("spinBox_session_class", ("session", "class_pi")),
            WidgetBinding("comboBox_session_road_type", ("session", "road_type")),
            WidgetBinding("comboBox_session_location", ("session", "location")),
            WidgetBinding("comboBox_session_surface", ("session", "surface")),

            # ── Info ──────────────────────────────────────────────────────────
            WidgetBinding("spinBox_info_weight", ("info", "weight")),
            WidgetBinding("spinBox_info_power", ("info", "power")),
            WidgetBinding("spinBox_info_torque", ("info", "torque")),
            WidgetBinding("doubleSpinBox_info_front_weight", ("info", "front_weight")),
            WidgetBinding("spinBox_info_suspension_travel", ("info", "suspension_travel")),
            WidgetBinding("comboBox_info_drive_type", ("info", "drive_type")),
            WidgetBinding("comboBox_info_engine_placement", ("info", "engine_placement")),

            # ── Tires — label_format="float": 2.1 bar ─────────────────────────
            WidgetBinding("horizontalSlider_tire_front_pressure", ("tires", "front_pressure_bar"), ui_to_model=slider_x10_to_model, model_to_ui=slider_x10_to_ui, label_name="label_tire_front_value",  label_format="float"),
            WidgetBinding("horizontalSlider_tire_rear_pressure",  ("tires", "rear_pressure_bar"),  ui_to_model=slider_x10_to_model, model_to_ui=slider_x10_to_ui, label_name="label_tire_rear_value",   label_format="float"),
            WidgetBinding("spinBox_tire_width_front", ("tires", "width_front")),
            WidgetBinding("spinBox_tire_width_rear",  ("tires", "width_rear")),
            WidgetBinding("comboBox_tire_compound",   ("tires", "compound")),

            # ── Alignment — label_format="float": -1.5°, 5.0° ───────────────
            WidgetBinding("horizontalSlider_alignment_front_camber", ("alignment", "camber_front_deg"), ui_to_model=slider_x10_to_model, model_to_ui=slider_x10_to_ui, label_name="label_alignment_front_camber_value", label_format="float"),
            WidgetBinding("horizontalSlider_alignment_rear_camber",  ("alignment", "camber_rear_deg"),  ui_to_model=slider_x10_to_model, model_to_ui=slider_x10_to_ui, label_name="label_alignment_rear_camber_value",  label_format="float"),
            WidgetBinding("horizontalSlider_alignment_front_toe",    ("alignment", "toe_front_deg"),    ui_to_model=slider_x10_to_model, model_to_ui=slider_x10_to_ui, label_name="label_alignment_front_toe_value",    label_format="float"),
            WidgetBinding("horizontalSlider_alignment_rear_toe",     ("alignment", "toe_rear_deg"),     ui_to_model=slider_x10_to_model, model_to_ui=slider_x10_to_ui, label_name="label_alignment_rear_toe_value",     label_format="float"),
            WidgetBinding("horizontalSlider_alignment_front_caster", ("alignment", "caster_front_deg"), ui_to_model=slider_x10_to_model, model_to_ui=slider_x10_to_ui, label_name="label_alignment_front_caster_value", label_format="float"),

            # ── AntiRollBars — label_format="int": 32, 28 ───────────────────
            WidgetBinding("horizontalSlider_roll_bar_front", ("anti_roll_bars", "front"), ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_roll_bar_front_value"),
            WidgetBinding("horizontalSlider_roll_bar_rear",  ("anti_roll_bars", "rear"),  ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_roll_bar_rear_value"),

            # ── Suspension (Spring / Clearance) ───────────────────────────────
            WidgetBinding("doubleSpinBox_spring_front",    ("suspension", "spring_front")),
            WidgetBinding("doubleSpinBox_spring_rear",     ("suspension", "spring_rear")),
            WidgetBinding("doubleSpinBox_spring_min",      ("suspension", "spring_min")),
            WidgetBinding("doubleSpinBox_spring_max",      ("suspension", "spring_max")),
            WidgetBinding("doubleSpinBox_clearance_front", ("suspension", "clearance_front")),
            WidgetBinding("doubleSpinBox_clearance_rear",  ("suspension", "clearance_rear")),
            WidgetBinding("doubleSpinBox_clearance_min",   ("suspension", "clearance_min")),
            WidgetBinding("doubleSpinBox_clearance_max",   ("suspension", "clearance_max")),

            # ── Damping ───────────────────────────────────────────────────────
            WidgetBinding("doubleSpinBox_damping_rebound_front", ("damping", "rebound_front")),
            WidgetBinding("doubleSpinBox_damping_rebound_rear",  ("damping", "rebound_rear")),
            WidgetBinding("doubleSpinBox_damping_rebound_min",   ("damping", "rebound_min")),
            WidgetBinding("doubleSpinBox_damping_rebound_max",   ("damping", "rebound_max")),
            WidgetBinding("doubleSpinBox_damping_bump_front",    ("damping", "bump_front")),
            WidgetBinding("doubleSpinBox_damping_bump_rear",     ("damping", "bump_rear")),
            WidgetBinding("doubleSpinBox_damping_bump_min",      ("damping", "bump_min")),
            WidgetBinding("doubleSpinBox_damping_bump_max",      ("damping", "bump_max")),

            # ── Aerodynamics ──────────────────────────────────────────────────
            WidgetBinding("checkBox_aero_front",    ("aerodynamics", "front_enabled"), ui_to_model=bool, model_to_ui=bool),
            WidgetBinding("checkBox_aero_rear",     ("aerodynamics", "rear_enabled"),  ui_to_model=bool, model_to_ui=bool),
            WidgetBinding("spinBox_aero_front",     ("aerodynamics", "front")),
            WidgetBinding("spinBox_aero_front_min", ("aerodynamics", "front_min")),
            WidgetBinding("spinBox_aero_front_max", ("aerodynamics", "front_max")),
            WidgetBinding("spinBox_aero_rear",      ("aerodynamics", "rear")),
            WidgetBinding("spinBox_aero_rear_min",  ("aerodynamics", "rear_min")),
            WidgetBinding("spinBox_aero_rear_max",  ("aerodynamics", "rear_max")),

            # ── Brakes — label_format="int": 50%, 100% ─────────────────────
            WidgetBinding("horizontalSlider_brake_balance", ("brakes", "balance_pct"), ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_brake_balance_value"),
            WidgetBinding("horizontalSlider_brake_power",   ("brakes", "power_pct"),   ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_brake_power_value"),

            # ── Differential — label_format="int": 50, 75 ──────────────────
            WidgetBinding("horizontalSlider_differential_acceleration_front", ("differential", "acceleration_front"), ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_differential_acceleration_front_value"),
            WidgetBinding("horizontalSlider_differential_deceleration_front", ("differential", "deceleration_front"), ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_differential_deceleration_front_value"),
            WidgetBinding("horizontalSlider_differential_acceleration_rear",  ("differential", "acceleration_rear"),  ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_differential_acceleration_rear_value"),
            WidgetBinding("horizontalSlider_differential_deceleration_rear",  ("differential", "deceleration_rear"),  ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_differential_deceleration_rear_value"),
            WidgetBinding("horizontalSlider_differential_balance",            ("differential", "balance"),            ui_to_model=slider_x1_to_model, model_to_ui=slider_x1_to_ui, label_name="label_differential_balance_value"),

            # ── Assists ───────────────────────────────────────────────────────
            WidgetBinding("comboBox_assists_abs",      ("assists", "abs"), ui_to_model=str_to_bool, model_to_ui=bool_to_str),
            WidgetBinding("comboBox_assists_stm",      ("assists", "stm"), ui_to_model=str_to_bool, model_to_ui=bool_to_str),
            WidgetBinding("comboBox_assists_tcs",      ("assists", "tcs"), ui_to_model=str_to_bool, model_to_ui=bool_to_str),
            WidgetBinding("comboBox_assists_shifting", ("assists", "shifting")),
            WidgetBinding("comboBox_assists_steering", ("assists", "steering")),
        ]

    def configure_ranges(self, ui_widgets: UiSource) -> None:
        """
        Устанавливает setMinimum/setMaximum/setValue слайдеров и спинбоксов:
          - min/max  — читает из Field(ge/le) через TuningDefaults.get_range()
          - default  — читает через TuningDefaults.get()

        Вызывается один раз до export_to_ui. Автоматически подхватывает
        ge/le при изменении Field в tuning.py — дополнить/изменить мапер не нужно.
        Виджет пропускается, если поле не имеет ge/le (напр. str-поля).
        """
        for binding in self.bindings:
            widget = self._get_widget_from_dict_or_obj(ui_widgets, binding.widget_name)
            if widget is None or not isinstance(widget, (QAbstractSlider, QAbstractSpinBox)):
                continue

            lo, hi = TuningDefaults.get_range(binding.model_path)
            
            if lo is not None:
                widget.setMinimum(binding.model_to_ui(lo))
            if hi is not None:
                widget.setMaximum(binding.model_to_ui(hi))
            
            if isinstance(widget, QAbstractSlider):
                # Гарантируем шаг 1 для колёсика и стрелок — независимо от Qt Designer
                widget.setSingleStep(1)
                widget.setPageStep(1)

            default_model = TuningDefaults.get(binding.model_path)
            if default_model is not None:
                widget.setValue(binding.model_to_ui(default_model))

    def populate_combo_boxes(self, ui_widgets: UiSource) -> None:
        """
        Заполняет QComboBox-виджеты допустимыми значениями из TuningOptions.

        Вызывается один раз при инициализации view, до export_to_ui —
        чтобы setCurrentText нашёл нужный элемент в уже заполненном списке.
        Если для поля нет вариантов в TuningOptions — пропускается.
        """
        for binding in self.bindings:
            options = TuningOptions.for_path(binding.model_path)
            if options is None:
                continue

            widget = self._get_widget_from_dict_or_obj(ui_widgets, binding.widget_name)
            if widget is None or not isinstance(widget, QComboBox):
                continue

            widget.blockSignals(True)   # не триггерим сигналы при заполнении
            widget.clear()
            widget.addItems(options)
            widget.blockSignals(False)

    # ── Константы стилей подсветки ошибок ────────────────────────────
    _ERROR_STYLE = "border: 1px solid #e05252; background-color: #3a1f1f;"
    _CLEAR_STYLE = ""

    def highlight_errors(self, ui_widgets: UiSource, errors: dict[str, str]) -> None:
        """
        Подсвечивает виджеты, связанные с ошибочными полями модели.

        errors: словарь {"tires.front_pressure_bar": "Сообщение об ошибке", ...}
        Схема ключей должна совпадать с тем, что излучает ConfigValidatorService:
        ".".join(binding.model_path).
        """
        # Сначала сбрасываем всю предыдущую подсветку
        self.clear_highlights(ui_widgets)

        for binding in self.bindings:
            error_key = ".".join(binding.model_path)
            if error_key not in errors:
                continue

            widget = self._get_widget_from_dict_or_obj(ui_widgets, binding.widget_name)
            if widget is None:
                continue

            if isinstance(widget, QWidget):
                widget.setStyleSheet(self._ERROR_STYLE)
                widget.setToolTip(errors[error_key])

    def clear_highlights(self, ui_widgets: UiSource) -> None:
        """Сбрасывает стили ошибок со всех виджетов — вызывается перед каждой попыткой сохранения."""
        for binding in self.bindings:
            widget = self._get_widget_from_dict_or_obj(ui_widgets, binding.widget_name)
            if widget is not None and isinstance(widget, QWidget):
                widget.setStyleSheet(self._CLEAR_STYLE)
                widget.setToolTip("")

    def setup_slider_labels(self, ui_widgets: UiSource) -> None:
        """
        Динамически связывает слайдеры с QLabel.
        Формат берётся из binding.label_format:
          "float" → один знак после запятой (slider_x10: "-1.5", "2.1")
          "int"   → целое без дробной части (slider_x1:  "50", "33")
        """
        for binding in self.bindings:
            if binding.label_name is None:
                continue

            slider = self._get_widget_from_dict_or_obj(ui_widgets, binding.widget_name)
            label  = self._get_widget_from_dict_or_obj(ui_widgets, binding.label_name)
            if slider is None or label is None:
                logger.warning(
                    "setup_slider_labels: не найден слайдер '%s' или лейбл '%s'",
                    binding.widget_name, binding.label_name,
                )
                continue

            fmt = binding.label_format

            def _format(raw_slider_val: int, _fmt: str = fmt, _fn=binding.ui_to_model) -> str:
                model_val = _fn(raw_slider_val)
                if _fmt == "float":
                    return f"{model_val:.1f}"
                return str(int(model_val))

            # Устанавливаем начальное значение лейбла
            if isinstance(slider, QAbstractSlider):
                label.setText(_format(slider.value()))

                def _make_handler(lbl=label, f=_format):
                    def _handler(val: int) -> None:
                        lbl.setText(f(val))
                    return _handler

                slider.valueChanged.connect(_make_handler())

    def _get_widget_from_dict_or_obj(self, ui_widgets: UiSource, widget_name: str) -> QWidget | None:
        """Возвращает виджет из генерированного Ui_* объекта или словаря (для тестов)."""
        if isinstance(ui_widgets, dict):
            return ui_widgets.get(widget_name)  # type: ignore[return-value]
        return getattr(ui_widgets, widget_name, None)

    def _ui_get_value(self, widget: QWidget) -> Any:
        """Извлечение значения виджета через реестр стратегий (Extractors)."""
        widget_type = type(widget)
        
        # Быстрый поиск по точному типу
        if widget_type in self.extractors:
            return self.extractors[widget_type](widget)
            
        # Поиск по иерархии (MRO), соблюдая порядок регистрации
        for cls, extractor in self.extractors.items():
            if isinstance(widget, cls):
                return extractor(widget)

        logger.warning(
            "_ui_get_value: неизвестный тип виджета %s — значение не прочитано",
            widget_type.__name__,
        )
        return None

    def _ui_set_value(self, widget: QWidget, value: Any) -> None:
        """Установка значения виджета через реестр стратегий (Injectors)."""
        widget_type = type(widget)
        
        # Быстрый поиск по точному типу
        if widget_type in self.injectors:
            self.injectors[widget_type](widget, value)
            return
            
        # Поиск по иерархии (MRO), соблюдая порядок регистрации
        for cls, injector in self.injectors.items():
            if isinstance(widget, cls):
                injector(widget, value)
                return

        logger.warning(
            "_ui_set_value: неизвестный тип виджета %s — значение не установлено",
            widget_type.__name__,
        )

    def update_from_ui(self, ui_widgets: UiSource) -> dict[str, Any]:
        """
        Считывает данные из UI, применяет функции ui_to_model и собирает словарь для Pydantic.
        """
        result_dict: dict[str, Any] = {}

        for binding in self.bindings:
            widget = self._get_widget_from_dict_or_obj(ui_widgets, binding.widget_name)
            if widget is None:
                continue

            raw_val = self._ui_get_value(widget)
            if raw_val is None or raw_val == "":
                continue

            try:
                model_val = binding.ui_to_model(raw_val)
            except (ValueError, TypeError) as e:
                # Ожидаемые ошибки преобразования: логируем и пропускаем поле.
                # Пользователь получит ошибку валидации о недостающем поле.
                logger.warning(
                    "update_from_ui: ошибка преобразования виджета '%s' (raw=%r): %s",
                    binding.widget_name, raw_val, e,
                )
                continue

            # Сборка многоуровневого словаря без ошибок KeyError
            current_level = result_dict
            for path_part in binding.model_path[:-1]:
                current_level = current_level.setdefault(path_part, {})
            current_level[binding.model_path[-1]] = model_val

        return result_dict

    def export_to_ui(self, model_data: dict[str, Any], ui_widgets: UiSource) -> None:
        """
        Заполняет UI виджеты данными из словаря модели (через model_dump()), 
        игнорируя отсутствующие в словаре поля Fail-Safe.
        """
        for binding in self.bindings:
            widget = self._get_widget_from_dict_or_obj(ui_widgets, binding.widget_name)
            if widget is None:
                continue

            # Поиск данных в model_data по пути model_path
            current_level = model_data
            found = True
            for path_part in binding.model_path:
                if isinstance(current_level, dict) and path_part in current_level:
                    current_level = current_level[path_part]
                else:
                    found = False
                    break
            
            if not found:
                continue

            try:
                ui_val = binding.model_to_ui(current_level)
                self._ui_set_value(widget, ui_val)
            except (ValueError, TypeError) as e:
                # Ожидаемые ошибки преобразования: логируем, UI-поле остаётся со старым значением.
                logger.warning(
                    "export_to_ui: ошибка преобразования виджета '%s' (model_val=%r): %s",
                    binding.widget_name, current_level, e,
                )
