# Справочник привязок — WidgetBinding по секциям

> Принципы применимы к любому UI-окну в проекте, не только к диалогу конфигурации.

Полный пример того, как выглядит каждый тип виджета в `TuningMapper._init_bindings()`.

---

## Как читать `ui_config_dialog.py`

Искать все `self.<name> = Q<WidgetType>(...)` — это полный список виджетов:

```python
# QSlider — нужен WidgetBinding с трансформерами и label_name
self.horizontalSlider_tire_front_pressure = QSlider(...)

# QDoubleSpinBox — для float-полей (suspension, damping, info.front_weight)
self.doubleSpinBox_spring_front = QDoubleSpinBox(...)

# QSpinBox — для int-полей
self.spinBox_info_weight = QSpinBox(...)

# QLineEdit — строковые поля
self.lineEdit_session_name = QLineEdit(...)

# QLabel — для отображения значения слайдера (label_name в binding)
self.label_tire_front_value = QLabel(...)

# QCheckBox — булево значение
self.checkBox_aero_front = QCheckBox(...)

# QComboBox — список вариантов (заполняется из TuningOptions автоматически)
self.comboBox_session_road_type = QComboBox(...)
```

---

## Структура _init_bindings() по секциям

```python
# ── Session ───────────────────────────────────────────────────────
WidgetBinding("lineEdit_session_name", ("session", "name")),
WidgetBinding("lineEdit_session_car",  ("session", "car")),
WidgetBinding("spinBox_session_class", ("session", "class_pi")),
WidgetBinding("comboBox_session_road_type", ("session", "road_type")),
WidgetBinding("comboBox_session_location", ("session", "location")),
WidgetBinding("comboBox_session_surface",  ("session", "surface")),

# ── Info ──────────────────────────────────────────────────────────
WidgetBinding("spinBox_info_weight",            ("info", "weight")),
WidgetBinding("spinBox_info_power",             ("info", "power")),
WidgetBinding("spinBox_info_torque",            ("info", "torque")),
WidgetBinding("doubleSpinBox_info_front_weight",("info", "front_weight")),
WidgetBinding("spinBox_info_suspension_travel", ("info", "suspension_travel")),
WidgetBinding("comboBox_info_drive_type",       ("info", "drive_type")),
WidgetBinding("comboBox_info_engine_placement", ("info", "engine_placement")),

# ── Tires — слайдер ×10 (float label: "2.1 bar") ─────────────────
WidgetBinding("horizontalSlider_tire_front_pressure", ("tires", "front_pressure_bar"),
    ui_to_model=Transformers.slider_x10_to_model,
    model_to_ui=Transformers.slider_x10_to_ui,
    label_name="label_tire_front_value",
    label_format="float"),
WidgetBinding("horizontalSlider_tire_rear_pressure", ("tires", "rear_pressure_bar"),
    ui_to_model=Transformers.slider_x10_to_model,
    model_to_ui=Transformers.slider_x10_to_ui,
    label_name="label_tire_rear_value",
    label_format="float"),
WidgetBinding("spinBox_tire_width_front", ("tires", "width_front")),
WidgetBinding("spinBox_tire_width_rear",  ("tires", "width_rear")),
WidgetBinding("comboBox_tire_compound",   ("tires", "compound")),

# ── Alignment — слайдер ×10 (float label: "-1.5°") ──────────────
WidgetBinding("horizontalSlider_alignment_front_camber", ("alignment", "camber_front_deg"),
    ui_to_model=Transformers.slider_x10_to_model,
    model_to_ui=Transformers.slider_x10_to_ui,
    label_name="label_alignment_front_camber_value",
    label_format="float"),
# ... (rear_camber, front_toe, rear_toe, front_caster — аналогично)

# ── AntiRollBars — слайдер ×1 (int label: "32") ─────────────────
WidgetBinding("horizontalSlider_roll_bar_front", ("anti_roll_bars", "front"),
    ui_to_model=Transformers.slider_x1_to_model,
    model_to_ui=Transformers.slider_x1_to_ui,
    label_name="label_roll_bar_front_value"),
WidgetBinding("horizontalSlider_roll_bar_rear", ("anti_roll_bars", "rear"),
    ui_to_model=Transformers.slider_x1_to_model,
    model_to_ui=Transformers.slider_x1_to_ui,
    label_name="label_roll_bar_rear_value"),

# ── Suspension / Damping — QDoubleSpinBox, без трансформации ─────
WidgetBinding("doubleSpinBox_spring_front",    ("suspension", "spring_front")),
WidgetBinding("doubleSpinBox_spring_rear",     ("suspension", "spring_rear")),
WidgetBinding("doubleSpinBox_sping_min",       ("suspension", "spring_min")),  # опечатка в UI зафиксирована
WidgetBinding("doubleSpinBox_spring_max",      ("suspension", "spring_max")),
WidgetBinding("doubleSpinBox_clearance_front", ("suspension", "clearance_front")),
WidgetBinding("doubleSpinBox_clearance_rear",  ("suspension", "clearance_rear")),
# ... damping аналогично

# ── Aerodynamics — CheckBox + SpinBox ────────────────────────────
WidgetBinding("checkBox_aero_front", ("aerodynamics", "front_enabled"),
    ui_to_model=bool, model_to_ui=bool),
WidgetBinding("spinBox_aero_front",     ("aerodynamics", "front")),
WidgetBinding("spinBox_aero_front_min", ("aerodynamics", "front_min")),
WidgetBinding("spinBox_aero_front_max", ("aerodynamics", "front_max")),

# ── Brakes / Differential — слайдер ×1 (int label: "50") ────────
WidgetBinding("horizontalSlider_brake_balance", ("brakes", "balance_pct"),
    ui_to_model=Transformers.slider_x1_to_model,
    model_to_ui=Transformers.slider_x1_to_ui,
    label_name="label_brake_balance_value"),

# ── Assists — QComboBox с bool-строками ──────────────────────────
WidgetBinding("comboBox_assists_abs", ("assists", "abs"),
    ui_to_model=Transformers.str_to_bool,
    model_to_ui=Transformers.bool_to_str),
WidgetBinding("comboBox_assists_shifting", ("assists", "shifting")),  # строка — без трансформации
```

---

## Соответствие model_path → Pydantic

```python
("tires", "front_pressure_bar")  →  TuningSetup.tires.front_pressure_bar
("suspension", "spring_front")   →  TuningSetup.suspension.spring_front
("assists", "abs")               →  TuningSetup.assists.abs
```

> Ошибка пути — поле будет молча проигнорировано маппером (Fail-Safe поведение).
