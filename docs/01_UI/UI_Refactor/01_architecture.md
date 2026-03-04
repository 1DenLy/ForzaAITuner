# Архитектура UI — карта файлов и концепции

> Правила этого документа относятся ко всему UI проекта, не только к диалогу конфигурации.

## Карта файлов

| Роль | Файл | Трогать руками? |
|---|---|---|
| Источник истины для UI | `resources/config_dialog.ui` (XML) | ✅ Qt Designer |
| Сгенерированный Python-класс | `src/desktop_client/presentation/ui_gen/ui_config_dialog.py` | ❌ никогда |
| View (логика диалога) | `src/desktop_client/presentation/views/config_dialog.py` | ✅ только для новых сигналов |
| Маппер (центральный) | `src/desktop_client/presentation/mappers/tuning_binder.py` | ✅ единственное место для привязок |
| Трансформеры | `src/desktop_client/presentation/mappers/transformers.py` | ✅ при добавлении новой scale-логики |
| Доменные модели | `src/desktop_client/domain/tuning.py` | ⚠️ при изменении контракта данных |
| Дефолты и диапазоны | `src/desktop_client/domain/tuning_defaults.py` | ⚠️ при добавлении нового поля |

---

## Пайплайн

```
config_dialog.ui  ──[pyside6-uic]──►  ui_config_dialog.py
                                              │
                                    ConfigDialog.__init__
                                              │
                          ┌───────────────────┼────────────────────┐
                          ▼                   ▼                    ▼
              populate_combo_boxes    configure_sliders    setup_slider_labels
                   (TuningMapper)      (TuningDefaults)     (WidgetBinding)
                                              │
                              export_to_ui / update_from_ui
                                    (TuningMapper)
```

### Компиляция .ui → .py

Компиляция **автоматизирована**: pre-commit хук запускает её при каждом `git commit`,
если в staged-файлах есть изменённый `.ui`.

Вручную (если нужно запустить без коммита):

```powershell
make ui
# или напрямую:
python scripts/compile_ui.py
```

> Первичная настройка хука (один раз после клонирования репо):
> ```powershell
> make setup-hooks
> ```

---

## WidgetBinding — декларативная привязка

Каждый виджет с данными описан одной строкой в `TuningMapper._init_bindings()`:

```python
@dataclass
class WidgetBinding:
    widget_name: str                 # Имя виджета (objectName в Qt Designer)
    model_path: tuple[str, ...]      # Путь в Pydantic-модели: ("tires", "front_pressure_bar")

    ui_to_model: Callable = lambda x: x   # UI-значение → значение модели
    model_to_ui: Callable = lambda x: x   # Значение модели → UI-значение

    label_name: Optional[str] = None      # QLabel для живого отображения значения слайдера
    label_format: str = "int"             # "float" → "2.1", "int" → "50"
```

---

## Transformers — все scale-коэффициенты

Функции трансформации хранятся в `transformers.py`. Они чистые, именованные и покрыты тестами:

| Трансформер | Когда использовать | Пример |
|---|---|---|
| `Transformers.slider_x10_to_model` / `slider_x10_to_ui` | Слайдер с ценой деления 0.1 (давление, развал, схождение, кастор) | `21 → 2.1` / `2.1 → 21` |
| `Transformers.slider_x1_to_model` / `slider_x1_to_ui` | Слайдер с ценой деления 1.0 (ARB, тормоза, дифференциал) | `65 → 65.0` / `65.0 → 65` |
| `Transformers.str_to_bool` / `bool_to_str` | QComboBox с булевыми значениями ("True"/"False") | `"True" → True` |

> ⚠️ Старых констант `_SCALE_*` больше нет. Всё хранится в `transformers.py`.

---

## TuningDefaults — диапазоны и дефолты

`configure_sliders()` читает `min`/`max` автоматически из `Field(ge=..., le=...)` Pydantic-моделей:

```python
lo, hi = TuningDefaults.get_range(binding.model_path)  # читает ge/le из аннотации
```

> Не нужно ничего прописывать вручную для диапазонов слайдеров — они берутся из домена.
