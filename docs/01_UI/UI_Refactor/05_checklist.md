# Чеклист и запреты

> Правила этого документа действуют для всего UI проекта. Обязательно прочитать перед коммитом с любыми UI-правками.

## Что обязан проверить после любой правки

[ ] `ui_config_dialog.py` содержит `objectName`, совпадающий с `widget_name` в `WidgetBinding`
[ ] Каждый `QSlider` имеет `WidgetBinding` с `ui_to_model`/`model_to_ui` трансформерами
[ ] Каждый слайдер с live-лейблом имеет `label_name` и `label_format` в своём `WidgetBinding`
[ ] `model_path` в каждом `WidgetBinding` соответствует реальному полю в `tuning.py`
[ ] Новое поле домена добавлено в `TuningDefaults.create()`
[ ] `QComboBox` с новыми вариантами добавлен в `TuningOptions.for_path()`
[ ] `validation_failed` подключён: `self.vm.validation_failed.connect(self._on_validation_failed)`
[ ] `config_saved` подключён: `self.vm.config_saved.connect(self.accept)`
[ ] `global_error_occurred` подключён: `self.vm.global_error_occurred.connect(self._on_global_error)`

---

## Что никогда не делать

### ❌ Не трогать `.ui`-файлы напрямую в коде

`.ui`-файлы — это XML, которые редактируются **только в Qt Designer**.

# ЗАПРЕЩЕНО
resources/config_dialog.ui  →  открывать как текст и менять вручную

# ПРАВИЛЬНО
resources/config_dialog.ui  →  открывать только через Qt Designer

---

### ❌ Не трогать Python-файлы, сгенерированные из `.ui`

`ui_config_dialog.py` генерируется автоматически командой `pyside6-uic`.
Любые ручные правки будут уничтожены при следующей регенерации:

# ЗАПРЕЩЕНО
src/desktop_client/presentation/ui_gen/ui_config_dialog.py  →  редактировать вручную

# ПРАВИЛЬНО
pyside6-uic resources/config_dialog.ui -o src/desktop_client/presentation/ui_gen/ui_config_dialog.py
