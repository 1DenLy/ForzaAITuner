# Состояния окна Main

Данный файл описывает внутренние состояния главного окна приложения. Маршрутизация между окнами описана в [state_Overview.md](./state_Overview.md).

## 1. Детальные диаграммы состояний

### Ожидание (IDLE)
В этом состоянии приложение не собирает данные, но следит за готовностью конфигурации.
```mermaid
stateDiagram-v2
    state "Мониторинг конфига (MonitoringConfig)" as MonitoringConfig
    state "Конфиг готов (ValidConfig)" as ValidConfig
    state "Готов к старту (ReadyToStart)" as ReadyToStart

    [*] --> MonitoringConfig
    MonitoringConfig --> ValidConfig : Стейт валиден
    ValidConfig --> ReadyToStart : Кнопка разблокирована
    ReadyToStart --> MonitoringConfig : Изменение настроек
    ValidConfig --> MonitoringConfig : Сброс стейта
```

### Запуск (STARTING)
Процесс подготовки ресурсов.
```mermaid
stateDiagram-v2
    state "Инициализация ядра (InitializingCore)" as InitializingCore
    state "Подключение UDP (ConnectingUDP)" as ConnectingUDP
    state "Запуск воркера (SpawningSyncWorker)" as SpawningSyncWorker

    [*] --> InitializingCore
    InitializingCore --> ConnectingUDP : Слушатель запущен
    ConnectingUDP --> SpawningSyncWorker : Домен готов
    SpawningSyncWorker --> [*] : Все потоки активны
```

### Запись (RECORDING)
Цикл обработки данных в реальном времени.
```mermaid
stateDiagram-v2
    state "Запись в буфер (WritingToBuffer)" as WritingToBuffer
    state "Проверка пачки (BatchCheck)" as BatchCheck
    state "Запуск синхронизации (TriggeringSync)" as TriggeringSync

    [*] --> ReceivingPacket
    ReceivingPacket --> WaitingForData : UDP Timeout (>2s)
    WaitingForData --> ReceivingPacket : Данные получены
    ReceivingPacket --> WritingToBuffer : Прямая запись
    WritingToBuffer --> BatchCheck : Данные в очереди
    BatchCheck --> ReceivingPacket : < BatchLimit
    BatchCheck --> ReceivingPacket : < BatchLimit
    BatchCheck --> TriggeringSync : >= BatchLimit
    TriggeringSync --> ReceivingPacket : Success
    TriggeringSync --> SyncError : Backend/Network Error
    SyncError --> ReceivingPacket : Rollback & Continue
```

### Завершение (FLUSHING)
Гарантированная доставка данных перед выходом.
```mermaid
stateDiagram-v2
    state "Остановка потока (StoppingDataFlow)" as StoppingDataFlow
    state "Ожидание синхронизации (WaitingForLastSync)" as WaitingForLastSync
    state "Очистка ресурсов (CleaningResources)" as CleaningResources

    [*] --> StoppingDataFlow
    StoppingDataFlow --> WaitingForLastSync : UDP порт закрыт
    WaitingForLastSync --> CleaningResources : Очередь пуста
    CleaningResources --> [*] : Объекты уничтожены
```

## 2. Диаграмма связей и переходов

Эта диаграмма описывает только высокоуровневые триггеры между состояниями.

```mermaid
stateDiagram-v2
    direction LR
    [*] --> IDLE
    
    IDLE --> STARTING : "Start Session" (Click)
    STARTING --> RECORDING : status_changed (Started)
    STARTING --> IDLE : error_occurred (Notify)
    
    RECORDING --> FLUSHING : "Stop Session" (Click)
    RECORDING --> FLUSHING_EXIT : CloseEvent (Exit app)
    RECORDING --> FLUSHING : critical_error (Auto-stop)
    
    state "Завершение (FLUSHING)" as FLUSHING
    state "Завершение и Выход (FLUSHING_EXIT)" as FLUSHING_EXIT

    FLUSHING --> IDLE : status_changed (Stopped)
    FLUSHING_EXIT --> [*] : status_changed (Terminated)
```

## Описание состояний

| Состояние | Описание |
| :--- | :--- |
| **IDLE** | Окно ожидает действий пользователя. Кнопка Start активна только при наличии валидной конфигурации. |
| **STARTING** | Переходное состояние. Инициализация Core-компонентов и запуск потоков синхронизации. |
| **RECORDING** | Активная фаза сбора данных. UI находится в режиме ожидания, отображая только базовые индикаторы активности. |
| **FLUSHING** | Процесс остановки. Приложение дожидается отправки оставшихся данных из буфера перед возвратом в IDLE. |

## Переходы и события

- **Start Session**: Инициирует переход `IDLE -> STARTING`.
- **Stop Session**: Инициирует переход `RECORDING -> FLUSHING`.
- **Error**: Любая критическая ошибка во время `STARTING` возвращает систему в `IDLE`.
- **Shutdown**: Инициирует `FLUSHING` из любого активного состояния.

> [!WARNING]
> **ТЕХНИЧЕСКИЙ ДОЛГ:** ТЕКУЩИЙ LocalBuffer ХРАНИТ ДАННЫЕ В ПАМЯТИ. НЕОБХОДИМ РЕФАКТОРИНГ ПОД ХРАНЕНИЕ НА ДИСКЕ (DISK-QUEUE) ДЛЯ ПОЛНОЦЕННОЙ РЕАЛИЗАЦИИ СХЕМЫ "ЛОКАЛЬНЫЙ БУФЕР СПАСАЕТ ДАННЫЕ".

---
**Связанный код:**
- [main_window.py](./src/desktop_client/presentation/views/main_window.py)
- [app_state.py](./src/desktop_client/presentation/state/app_state.py)
