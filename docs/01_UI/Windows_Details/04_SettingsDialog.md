Рекомендация: Так как мне запрещено править 

.ui
 файлы вручную, вам нужно:

Открыть 

src/desktop_client/presentation/assets/settings_dialog.ui
 в Qt Designer.
Добавить QCheckBox с именем lanTelemetryCheckBox.
В SettingsDialog._on_accepted добавить логику сохранения: если галочка стоит — ставить в конфиг 0.0.0.0, если нет — 127.0.0.1.