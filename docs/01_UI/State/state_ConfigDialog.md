# Состояния окна ConfigDialog

Данный файл описывает состояния и логику работы диалогового окна конфигурации.

## 1. Детальные диаграммы состояний

### Загрузка (LOADING)
Подготовка данных для формы.
```mermaid
stateDiagram-v2
    state "Получение доменных данных (FetchingDomainData)" as FetchingDomainData
    state "Маппинг в форму (MappingToForm)" as MappingToForm
    state "Инициализация виджетов (InitializingWidgets)" as InitializingWidgets

    [*] --> FetchingDomainData
    FetchingDomainData --> MappingToForm : JSON/Object -> UI
    MappingToForm --> InitializingWidgets : Установка Min/Max/Default
    InitializingWidgets --> [*] : Форма готова
```

### Редактирование (EDITING)
Интерактивное взаимодействие.
```mermaid
stateDiagram-v2
    state "Ожидание ввода (Idle)" as Idle
    state "Обновление локальной модели (UpdatingLocalModel)" as UpdatingLocalModel
    state "Загрузка пресета (LoadingPreset)" as LoadingPreset

    [*] --> Idle
    Idle --> UpdatingLocalModel : Изменение виджета
    UpdatingLocalModel --> Idle : Модель синхронизирована
    Idle --> LoadingPreset : Выбор JSON файла
    LoadingPreset --> UpdatingLocalModel : Импорт данных
```

### Проверка (VALIDATING)
Валидация бизнес-правил и типов.
```mermaid
stateDiagram-v2
    state "Сбор данных формы (CollectingFormData)" as CollectingFormData
    state "Pydantic-валидация (PydanticValidation)" as PydanticValidation
    state "Успех (ResultOk)" as ResultOk
    state "Ошибка (ResultFail)" as ResultFail
    state "Подсветка UI (HighlightingUI)" as HighlightingUI

    [*] --> CollectingFormData
    CollectingFormData --> PydanticValidation : Вызов ViewModel
    PydanticValidation --> ResultOk : Ошибок нет
    PydanticValidation --> ResultFail : Ошибки найдены
    ResultFail --> HighlightingUI : Красные рамки/Тултипы
    ResultOk --> [*]
    HighlightingUI --> [*]
```

### Сохранение (SAVING)
Фиксация изменений.
```mermaid
stateDiagram-v2
    state "Создание доменной модели (CreatingDomainModel)" as CreatingDomainModel
    state "Обновление глобального стейта (UpdatingGlobalState)" as UpdatingGlobalState
    state "Запись на диск (PersistingToDisk)" as PersistingToDisk
    state "Обработка ошибки I/O (HandleIOError)" as HandleIOError

    [*] --> CreatingDomainModel
    CreatingDomainModel --> UpdatingGlobalState : Передача в ConfigDataManager
    UpdatingGlobalState --> PersistingToDisk : Запись в .json
    PersistingToDisk --> [*] : Сохранение подтверждено
    PersistingToDisk --> HandleIOError : Ошибка записи (диск/права)
    HandleIOError --> [*] : Возврат к редактированию
```

## 2. Диаграмма связей и переходов

Высокоуровневая логика управления диалогом.

```mermaid
stateDiagram-v2
    direction LR
    [*] --> LOADING
    LOADING --> EDITING : setup_complete
    
    EDITING --> VALIDATING : "Save" (Click)
    EDITING --> [*] : "Cancel" / "Close" (Reject)
    
    VALIDATING --> SAVING : validation_success
    VALIDATING --> EDITING : validation_failed
    
    SAVING --> EDITING : io_error (Notify user)
    SAVING --> [*] : config_saved (Accept)
```

## Описание состояний

| Состояние | Описание |
| :--- | :--- |
| **LOADING** | Загрузка текущих настроек из доменного слоя и инициализация виджетов маппером. |
| **EDITING** | Основное состояние взаимодействия. Пользователь меняет параметры или загружает пресеты из JSON. |
| **VALIDATING** | Проверка введенных данных через Pydantic-модели во ViewModel. |
| **SAVING** | Применение изменений к глобальному стейту приложения и сохранение на диск. |

---
**Связанный код:**
- [config_dialog.py](./src/desktop_client/presentation/views/config_dialog.py)
- [tuning_binder.py](./src/desktop_client/presentation/mappers/tuning_binder.py)
