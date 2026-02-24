# UI Update Workflow

> **Для ИИ-ассистента:** этот файл — обязательный чеклист при любом запросе,
> связанном с изменением UI диалога конфигурации. Читай его до начала правок.

---

## Контекст архитектуры

| Роль | Файл | Трогать руками? |
|---|---|---|
| Источник истины для UI | `resources/config_dialog.ui` (XML) | ✅ Qt Designer |
| Сгенерированный Python-класс | `src/desktop_client/presentation/ui_gen/ui_config_dialog.py` | ❌ никогда |
| View (логика привязки) | `src/desktop_client/presentation/views/config_dialog.py` | ✅ единственный редактируемый |
| ViewModel (бизнес-логика) | `src/desktop_client/presentation/viewmodels/config_viewmodel.py` | ⚠️ только если меняется контракт данных |

**Пайплайн:**
```
config_dialog.ui  ──[pyside6-uic]──►  ui_config_dialog.py  ──[import]──►  config_dialog.py
```

---

## Команда перегенерации (обязательна после правки .ui)

```powershell
pyside6-uic resources/config_dialog.ui -o src/desktop_client/presentation/ui_gen/ui_config_dialog.py
```

---

## Как ИИ должен анализировать изменения

### Шаг A — Прочитать `ui_config_dialog.py`

Искать все `self.<name> = Q<WidgetType>(...)` — это полный список виджетов.
Ключевые паттерны по типам:

```python
# QSlider — требует scale-коэффициент в config_dialog.py
self.front_camber_horizontalSlider = QSlider(...)

# QSpinBox — значение целое, scale не нужен
self.front_spring_min_spinBox = QSpinBox(...)

# QLabel для отображения значения слайдера (живое обновление)
self.lbl_front_camber_value = QLabel(...)

# QCheckBox — булево значение
self.front_aero_checkBox = QCheckBox(...)

# QDialogButtonBox — кнопки Save / Close / Reset / Open
self.buttonBox = QDialogButtonBox(...)
```

---

### Шаг B — Сверить с тремя таблицами в `config_dialog.py`

Каждый виджет должен присутствовать **во всех трёх местах** (или ни в одном, если он только декоративный):

#### Таблица 1 — `_setup_slider_labels()` (только QSlider + его QLabel)
```python
# Формат кортежа:
(self.ui.<slider_name>, self.ui.<lbl_name>, <scale: float>)
```
**Проверить:** у каждого `horizontalSlider` из `ui_config_dialog.py`
есть соответствующая строка здесь.

#### Таблица 2 — `_populate_initial_data()`
```python
# QSlider:
_set_slider("domain.field_name", self.ui.<slider_name>, scale=<float>)

# QSpinBox:
_set_spinbox("domain.field_name", self.ui.<spinBox_name>)

# QCheckBox — отдельный if-блок:
if "domain.field_enabled" in data:
    self.ui.<checkBox_name>.setChecked(bool(data["domain.field_enabled"]))
```
**Проверить:** каждый виджет, откуда берутся данные для ViewModel,
представлен в этом методе.

#### Таблица 3 — `_gather_data()` → словарь `return {...}`
```python
# QSlider с scale=0.1:
"domain.field_name": sl(self.ui.<slider_name>),

# QSlider с scale=1.0:
"domain.field_name": sl(self.ui.<slider_name>, scale=1.0),

# QSpinBox:
"domain.field_name": sp(self.ui.<spinBox_name>),

# QCheckBox:
"domain.field_enabled": str(self.ui.<checkBox_name>.isChecked()),
```
**Проверить:** каждый ключ в этом словаре — это `"section.field_name"`
в точечной нотации, совпадающей с полями Pydantic-моделей.

---

### Шаг C — Проверить коэффициент scale

> ⚠️ **Не смотри в эту документацию за конкретными числами.**
> Единственный источник истины — константы класса `_SCALE_*` в начале `config_dialog.py`.
> Документ намеренно не дублирует цифры, чтобы не устаревать.

Открой `config_dialog.py` и найди блок `_SCALE_*` в начале класса `ConfigDialog`:

```python
# STABLE — физически зафиксированные диапазоны Forza, не меняются при редизайне UI:
_SCALE_PRESSURE  = 0.1   # Давление шин
_SCALE_ALIGNMENT = 0.1   # Развал / схождение / кастор
_SCALE_ROLLBAR   = 1.0   # Стабилизаторы (стабы)
_SCALE_BRAKE     = 1.0   # Тормоза

# DYNAMIC — могут меняться при изменении UI-дизайна.
# При добавлении нового слайдера — добавь константу сюда.
```

**Разделение STABLE / DYNAMIC:**

| Категория | Параметры | Почему стабильны |
|---|---|---|
| **STABLE** | Давление шин, развал, схождение, кастор, стабы, тормоза | Физические диапазоны Forza фиксированы игрой |
| **DYNAMIC** | Spring, Clearance, Aero, Differential (будущий) | Диапазоны могут меняться при редизайне UI |

**Правило при изменении scale:**
Если в `.ui` изменился `minimum` или `maximum` слайдера — менять **только константу**
`_SCALE_*` в начале класса. Код в трёх методах (`_setup_slider_labels`,
`_populate_initial_data`, `_gather_data`) подтянется автоматически, так как
все они ссылаются на эту константу.

---

## Сценарии изменений и что делать

### Сценарий 1: Изменил диапазон существующего слайдера

1. `ui_config_dialog.py` — найти виджет, проверить новые `setMinimum` / `setMaximum`
2. `config_dialog.py` → обновить таблицу scale выше
3. Обновить `scale=` в `_setup_slider_labels()`, `_populate_initial_data()`, `_gather_data()`

### Сценарий 2: Переименовал виджет (objectName)

1. Найти старое имя в `config_dialog.py` (grep по `self.ui.старое_имя`)
2. Заменить везде на `self.ui.новое_имя`
3. Обновить таблицу scale в этом файле

### Сценарий 3: Добавил новый слайдер

1. В `_setup_slider_labels()` добавить кортеж `(slider, label, scale)`
2. В `_populate_initial_data()` добавить `_set_slider(...)`
3. В `_gather_data()` добавить строку ключ→`sl(...)`
4. Добавить строку в таблицу scale

### Сценарий 4: Добавил новый SpinBox

1. В `_populate_initial_data()` добавить `_set_spinbox(...)`
2. В `_gather_data()` добавить строку ключ→`sp(...)`

### Сценарий 5: Удалил виджет

1. Удалить из `_setup_slider_labels()` (если слайдер)
2. Удалить из `_populate_initial_data()`
3. Удалить из `_gather_data()`
4. Удалить строку из таблицы scale (если слайдер)

---

## Что ИИ обязан проверить после любой правки

```
[ ] ui_config_dialog.py содержит objectName, который используется в config_dialog.py
[ ] Каждый QSlider присутствует в _setup_slider_labels() с корректным scale
[ ] Каждый виджет с данными присутствует в _populate_initial_data()
[ ] Каждый виджет с данными присутствует в _gather_data() с правильным ключом
[ ] Ключи в _gather_data() соответствуют полям Pydantic-моделей (точечная нотация)
[ ] validation_failed подключён: self.vm.validation_failed.connect(self._on_validation_failed)
[ ] config_saved подключён: self.vm.config_saved.connect(self.accept)
[ ] global_error_occurred подключён: self.vm.global_error_occurred.connect(self._on_global_error)
```

---

## Что никогда не делать

- ❌ Редактировать `ui_config_dialog.py` вручную
- ❌ Убирать `self.ui = Ui_ConfigDialog()` / `self.ui.setupUi(self)`
- ❌ Менять ключи `_gather_data()` без синхронного обновления Pydantic-моделей
- ❌ Загружать `.ui` через `QUiLoader` (проект использует AOT-компиляцию)
