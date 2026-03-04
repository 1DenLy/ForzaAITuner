# Порядок инициализации View

> Протокол относится к любому View-окну, которое использует `TuningMapper`. Пример на `ConfigDialog`.

## Порядок вызовов в `ConfigDialog.__init__`

```python
self.mapper = TuningMapper()                     # 0. создать маппер с bindings

self.ui = Ui_ConfigDialog()
self.ui.setupUi(self)

self.mapper.populate_combo_boxes(self.ui)        # 1. заполнить QComboBox из TuningOptions
self.mapper.configure_sliders(self.ui)           # 2. min/max/default слайдеров из домена
self.mapper.setup_slider_labels(self.ui)         # 3. подключить label к valueChanged
self._connect_signals()                          # 4. сигналы кнопок и ViewModel
self._populate_initial_data()                    # 5. загрузить реальные данные из ViewModel
```

---

## Почему порядок важен

| Шаг | Метод | Зависит от |
|---|---|---|
| 1 | `populate_combo_boxes` | Должен быть **до** `export_to_ui` — иначе `setCurrentText` не найдёт элемент в пустом списке |
| 2 | `configure_sliders` | Читает `ge`/`le` из Pydantic через `TuningDefaults.get_range()` |
| 3 | `setup_slider_labels` | Подключает `valueChanged` — должен быть после `configure_sliders`, чтобы начальное значение лейбла было корректным |
| 4 | `_connect_signals` | Подключает кнопки и сигналы ViewModel — не зависит от порядка, но логично после UI-инициализации |
| 5 | `_populate_initial_data` | Вызывает `mapper.export_to_ui()` — должен быть **последним**, когда ComboBox уже заполнен |

---

## Сигналы ViewModel (обязательны)

```python
self.vm.validation_failed.connect(self._on_validation_failed)
self.vm.config_saved.connect(self.accept)
self.vm.global_error_occurred.connect(self._on_global_error)
```
