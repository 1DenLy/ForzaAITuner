# Менеджмент Конфигураций (Domain/Application Layer)

В то время как UI слой отвечает за отображение и сбор данных, бизнес-логика валидации, сохранения и переиспользования конфигураций инкапсулирована в Domain и Application слоях. 

Этот документ описывает как происходит управление состоянием конфигурации (настроек автомобиля), ее сохранение и как она встраивается в процесс сбора телеметрии во время заездов.

## Архитектура Управления Состоянием (Config State Management)

Ниже представлена структурная схема взаимодействия компонентов при изменении и использовании конфигурации:

```mermaid
flowchart TD
    UI[UI / Config Dialog] -->|Data Binding| CVM(ConfigViewModel)
    
    subgraph Domain & Application Layer
        CVM -->|Обновление статуса| CSM(ConfigStateManager)
        CSM -->|Запрос валидации| CVS(ConfigValidatorService)
        CVS -.->|Создает & Проверяет| TS[Pydantic модель: TuningSetup]
        
        CSM -->|Сохранить / Получить| LCR[(LocalConfigRepository)]
    end
    
    LCR -.->|Чтение / Запись JSON| Disk[(Local Disk)]
    
    subgraph Forza Core Session
        DS[Сессия Заезда] -->|Читает последнюю конфигурацию| LCR
        DS -.->|Отправляет Config + Telemetry| Backend[Аналитика / Backend]
    end
```

### Основные компоненты системы:

1. **ConfigViewModel**
   - Точка входа для UI. Принимает сырые данные из формы.
   - Абстрагирует UI от прямой работы с сервисами.
   
2. **ConfigStateManager**
   - Управляет жизненным циклом конфигурации в памяти.
   - Оркестрирует процессы валидации и сохранения. Является единственным источником истины о текущем валидном конфиге.

3. **ConfigValidatorService**
   - Отвечает за проверку бизнес-правил.
   - Использует строгую типизацию и ограничения Pydantic модели `TuningSetup` (например, проверка диапазонов через `ge/le`, проверка допустимых типов машин).

4. **LocalConfigRepository**
   - Инфраструктурный слой. Отвечает за персистентность (сохранение на диск).
   - Читает и записывает данные настройки в формате JSON (например, файл `current_setup.json`). 
   - **Главное правило**: *Последняя валидная конфигурация всегда хранится локально*. Это сделано для удобства пользователя, чтобы после перезапуска приложения не приходилось вводить все заново.

## Жизненный Цикл и Использование в Сессии Заезда

Помимо локального сохранения для удобства, конфигурация является критически важной частью данных заезда.

```mermaid
sequenceDiagram
    autonumber
    
    participant UI as User Interface
    participant CVM as ConfigViewModel
    participant CSM as ConfigStateManager
    participant CVS as ConfigValidatorService
    participant LCR as LocalConfigRepository
    participant Session as Driving Session

    Note over UI, LCR: 1. Процесс редактирования
    UI->>CVM: Изменение слайдера/поля
    CVM->>CSM: Сохранить новые данные
    CSM->>CVS: Валидация
    CVS->>CVS: model_validate(TuningSetup)
    
    alt Валидация успешна
        CVS-->>CSM: Валидная модель (TuningSetup)
        CSM->>LCR: Сохранить (persist)
        LCR-->>CSM: JSON записан на диск
        CSM-->>CVM: State = OK
        CVM-->>UI: Индикатор успеха
    else Ошибка
        CVS-->>CSM: ValidationError
        CSM-->>CVM: State = Error
        CVM-->>UI: Блокировка / Подсветка ошибки
    end

    Note over LCR, Session: 2. Процесс заезда (Telemetry)
    Session->>Session: Обнаружено начало заезда
    Session->>LCR: Запрос актуального конфига
    LCR-->>Session: Последний валидный JSON конфиг
    Note right of Session: Конфиг прикрепляется к потоку данных<br>и отправляется вместе с телеметрией заезда!
```

### Идея связи Конфига с Телеметрией:
Как только начинается активная сессия в игре (старт телеметрии):
1. Ядро приложения (`Forza Core`) читает последнюю валидную конфигурацию через `LocalConfigRepository`.
2. Эта конфигурация неразрывно прикрепляется к данным сессии.
3. Таким образом, вся телеметрия данного заезда имеет точный слепок того, с какими настройками (подвеска, давление, аэродинамика) ехала машина.
