# CoreFacade Details

## Суть
Описание главного класса-фасада `CoreFacade` и его жизненного цикла.

## Управление состоянием (Жизненный цикл Фасада)
Ниже представлена стейт-машина Фасада, которая отображает возможные состояния модуля и переходы между ними:
```mermaid
flowchart TB
    %% Состояния
    Stopped["Stopped"]
    Starting["Starting"]
    Listening["Listening"]
    Stopping["Stopping"]
    Error["Error"]

    %% Переходы
    Stopped -->|"start() / init queue, bind port"| Starting
    Stopped -->|"stop() / ignore"| Stopped

    Starting -->|"[port bound successfully] / start async loop"| Listening
    Starting -->|"[port already in use] / throw AddressError"| Error

    Error -->|"[recover]"| Stopped

    Listening -->|"stop() / send close signal"| Stopping
    Listening -->|"start() / ignore, log warning"| Listening
    Listening -->|"[invalid UDP packet] / drop, log(RateLimit)"| Listening

    Stopping -->|"[resources freed] / clean port"| Stopped
    Stopping -->|"stop() / ignore"| Stopping

    %% Стилизация классов (с черным текстом)
    classDef stateNode fill:#d4e5ff,stroke:#5c8ce6,stroke-width:2px,color:#000;
    classDef errorNode fill:#f9d0c4,stroke:#e84a5f,stroke-width:2px,color:#000;

    class Stopped,Starting,Listening,Stopping stateNode;
    class Error errorNode;
```

## Методы `start()` и `stop()`
Методы управления Фасадом подчиняются важным правилам надежности:
* **Идемпотентность**: Повторный вызов метода `start()` не должен приводить к падению приложения (например, с ошибкой "Port in use"). В этом случае фасад логирует предупреждение и игнорирует команду. Аналогично, вызов `stop()` у уже остановленного модуля не должен вызывать никаких ошибок.

## Изолированность потока выполнения
Модуль **ни в коем случае не должен блокировать основной поток** вызывающего приложения (например, UI).
Цикл прослушивания UDP-порта работает асинхронно в изолированном фоновом потоке, который управляется через внедренную зависимость `IAsyncRunner` (реализация `AsyncioThreadRunner`). Это устраняет нарушение SRP фасадом:
* Запуск инфраструктуры потока: `self._async_runner.start()`.
* Межпоточное взаимодействие и передача задач в фоновый Event Loop: `self._async_runner.submit(self._start_async())`.

```mermaid
sequenceDiagram
    participant Main as Main Thread
    participant AR as AsyncioThreadRunner
    participant CW as CoreFacade Async Task
    
    Main->>AR: Инициализация Runner()
    Main->>Main: Инициализация CoreFacade(runner)
    Note over AR: Выделенный Event Loop работает<br>в фоновом daemon-потоке
    Main->>AR: facade.__init__() вызывает runner.start()

    Main->>Main: facade.start()<br>[Синхронный вызов из UI]
    Note right of Main: Пересечение границы потоков!
    Main->>AR: runner.submit(_start_async())
    AR->>CW: Запуск _start_async() в фоне
```
