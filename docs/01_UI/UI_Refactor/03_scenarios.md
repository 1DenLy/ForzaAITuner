# Сценарии изменений UI

> Инструкции применяются ко всему UI проекта. Примеры показаны на диалоге конфигурации, но принцип одинаков для любого окна.

Пошаговые инструкции для типовых задач.

---

## Сценарий 1: Добавить новый слайдер (×10 scale, float)

*Применяется для:* давление шин, развал, схождение, кастор.

1. Добавить `horizontalSlider_<name>` и `label_<name>_value` в `.ui` через Qt Designer
2. Перегенерировать:
   ```powershell
   pyside6-uic resources/config_dialog.ui -o src/.../ui_gen/ui_config_dialog.py
   ```
3. Добавить поле в `tuning.py` с `Field(ge=..., le=...)`
4. Добавить `WidgetBinding` в `TuningMapper._init_bindings()`:
   ```python
   WidgetBinding("horizontalSlider_<name>", ("<section>", "<field>"),
       ui_to_model=Transformers.slider_x10_to_model,
       model_to_ui=Transformers.slider_x10_to_ui,
       label_name="label_<name>_value",
       label_format="float"),
   ```
5. Добавить дефолт в `TuningDefaults.create()`

---

## Сценарий 2: Добавить новый слайдер (×1 scale, int)

*Применяется для:* ARB, тормоза, дифференциал.

Аналогично Сценарию 1, но трансформеры:
```python
ui_to_model=Transformers.slider_x1_to_model,
model_to_ui=Transformers.slider_x1_to_ui,
# label_format="int" — это значение по умолчанию, можно опустить
```

---

## Сценарий 3: Добавить новый QDoubleSpinBox

*Применяется для:* suspension, damping, и любых float-полей.

1. Добавить `doubleSpinBox_<name>` в `.ui`
2. Перегенерировать
3. Добавить поле в `tuning.py`
4. Добавить `WidgetBinding` — трансформаторы не нужны (identity по умолчанию):
   ```python
   WidgetBinding("doubleSpinBox_<name>", ("<section>", "<field>")),
   ```
5. Добавить дефолт в `TuningDefaults.create()`

---

## Сценарий 4: Добавить новый QSpinBox (int)

Аналогично Сценарию 3, виджет `spinBox_<name>`.

---

## Сценарий 5: Добавить новый QComboBox

1. Добавить `comboBox_<name>` в `.ui`
2. Перегенерировать
3. Добавить варианты значений в `TuningOptions.for_path()` (`tuning_options.py`)
4. Добавить `WidgetBinding`:
   ```python
   # Строковые значения — трансформация не нужна:
   WidgetBinding("comboBox_<name>", ("<section>", "<field>")),

   # Булевые значения через комбобокс ("True" / "False"):
   WidgetBinding("comboBox_<name>", ("<section>", "<field>"),
       ui_to_model=Transformers.str_to_bool,
       model_to_ui=Transformers.bool_to_str),
   ```
5. `populate_combo_boxes()` заполнит список автоматически при старте

---

## Сценарий 6: Переименовать виджет (objectName)

1. Найти старое имя в `tuning_binder.py` — grep по `"старое_имя"`
2. Заменить `widget_name=` в `WidgetBinding`
3. Если есть `label_name=` — обновить и его

---

## Сценарий 7: Удалить виджет

1. Удалить `WidgetBinding` из `_init_bindings()`
2. Удалить поле из `tuning.py` (если нигде больше не используется)
3. Удалить дефолт из `TuningDefaults.create()`

---

## Сценарий 8: Изменить scale существующего слайдера

Изменить трансформеры в одном `WidgetBinding`:
```python
# Было (×1):
ui_to_model=Transformers.slider_x1_to_model,
model_to_ui=Transformers.slider_x1_to_ui,

# Стало (×10):
ui_to_model=Transformers.slider_x10_to_model,
model_to_ui=Transformers.slider_x10_to_ui,
label_format="float",
```

> Диапазоны min/max подтянутся из `Field(ge/le)` автоматически — менять их не нужно.
