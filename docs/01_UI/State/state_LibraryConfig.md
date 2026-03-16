# Состояния окна LibraryConfig

Данный файл описывает логику работы окна библиотеки конфигураций.

## 1. Детальные диаграммы состояний

### Инициализация (INITIALIZING)
Загрузка данных из БД/Файлов.
```mermaid
stateDiagram-v2
    state "Сканирование хранилища (ScanningStorage)" as ScanningStorage
    state "Парсинг конфигов (ParsingConfigs)" as ParsingConfigs
    state "Обновление списка (UpdatingList)" as UpdatingList
    state "Пустое состояние (EmptyState)" as EmptyState

    [*] --> ScanningStorage
    ScanningStorage --> ParsingConfigs : Найдено N файлов
    ParsingConfigs --> UpdatingList : N > 0 (Валидация)
    ParsingConfigs --> EmptyState : N == 0
    UpdatingList --> [*] : Данные во ViewModel
    EmptyState --> [*] : Показать плейсхолдер
```

### Просмотр (VIEWING)
Активный режим пользователя.
```mermaid
stateDiagram-v2
    state "Ожидание действий (Idle)" as Idle
    state "Фильтрация (Filtering)" as Filtering
    state "Пересборка списка (RebuildingList)" as RebuildingList
    state "Сортировка (Sorting)" as Sorting
    state "Удаление элемента (Deleting)" as Deleting

    [*] --> Idle
    Idle --> Filtering : Переключение чекбокса
    Filtering --> RebuildingList : Применение предиката
    RebuildingList --> Idle : list_updated
    Idle --> Sorting : Смена комбобокса
    Sorting --> RebuildingList : Сортировка коллекции
    Idle --> Deleting : Клик "Delete" (ID)
    Deleting --> RebuildingList : Подтверждено (I/O)
```

### Вызов редактора (EDITOR_INVOCATION)
Подготовка диалога для нового или существующего конфига.
```mermaid
stateDiagram-v2
    state "Сброс полей UI (ResettingUIFields)" as ResettingUIFields
    state "Загрузка данных (LoadingExistingData)" as LoadingExistingData
    state "Вызов диалога (RequestingConfigDialog)" as RequestingConfigDialog

    [*] --> ResettingUIFields : Клик "New"
    [*] --> LoadingExistingData : Клик на карточку "Edit" (ID)
    
    ResettingUIFields --> RequestingConfigDialog
    LoadingExistingData --> RequestingConfigDialog
    RequestingConfigDialog --> [*] : Ждем завершения
```

### Импорт/Экспорт (IMPORTING_EXPORTING)
Обработка внешних файлов конфигураций с валидацией и обработкой ошибок.
```mermaid
stateDiagram-v2
    state "Выбор файла (SelectingFile)" as SelectingFile
    state "Валидация (ValidatingFile)" as ValidatingFile
    state "Операция I/O (IoOperation)" as IoOperation
    state "Ошибка I/O (HandleIOError)" as HandleIOError
    state "Пересборка списка (RebuildingList)" as RebuildingList

    [*] --> SelectingFile
    SelectingFile --> ValidatingFile : Файл выбран
    SelectingFile --> [*] : Отмена

    ValidatingFile --> IoOperation : Валидно
    ValidatingFile --> HandleIOError : Ошибка структуры/JSON

    IoOperation --> RebuildingList : Успех Import
    IoOperation --> [*] : Успех Export
    IoOperation --> HandleIOError : Ошибка доступа/диска
    
    HandleIOError --> SelectingFile : Попробовать снова
    HandleIOError --> [*] : Закрыть (Отмена)
    
    RebuildingList --> [*] : Список обновлен
```


## 2. Диаграмма связей и переходов

Высокоуровневая логика библиотеки.

```mermaid
stateDiagram-v2
    direction LR
    state "Библиотека (VIEWING)" as VIEWING
    state "Редактор (EDITOR)" as EDITOR
    state "Удаление (DELETING)" as DELETING

    [*] --> INITIALIZING
    INITIALIZING --> VIEWING : list_ready / empty_processed
    
    VIEWING --> EDITOR : "New Config" / "Select Config" (Click)
    EDITOR --> VIEWING : dialog_closed (Accept/Reject)
    
    VIEWING --> DELETING : "Delete" (Click)
    DELETING --> VIEWING : file_removed (Rebuild list)
    
    VIEWING --> IMPORTING_EXPORTING : "Import" / "Export" (Click)
    IMPORTING_EXPORTING --> VIEWING : transfer_done / error_ignored
    
    VIEWING --> [*] : "Back to Main" (Click)
```


## Описание состояний

| Состояние | Описание |
| :--- | :--- |
| **INITIALIZING** | Первичная загрузка списка. Теперь включает обработку **EmptyState** для первого запуска. |
| **VIEWING** | Основной экран. Позволяет не только фильтровать, но и инициировать удаление или редактирование. |
| **EDITOR_INVOCATION** | Промежуточный стейт для подготовки данных (сброс для новых, загрузка для старых) перед открытием диалога. |
| **DELETING** | Фаза физического удаления файла с последующим автоматическим обновлением списка. |
| **IMPORTING_EXPORTING** | Работа с системным диалогом файлов. Блокирует основной UI. Включает валидацию JSON и обновление списка после импорта. |

---
**Связанный код:**
- [config_library_viewmodel.py](./src/desktop_client/presentation/viewmodels/config_library_viewmodel.py)
- [ui_config_library.py](./src/desktop_client/presentation/ui/generated/ui_config_library.py)
