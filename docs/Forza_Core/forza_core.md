# ForzaCore (Module Facade)

## Суть

`ForzaCore` реализует интерфейс `IForzaCore` и выступает **фасадом модуля**: предоставляет публичное API (`start_tracking`, `stop_tracking`), управляет жизненным циклом и делегирует работу внутренним компонентам. Сам `ForzaCore` не знает ни о UDP, ни о бинарных форматах, ни о порядке шагов пайплайна.

Оркестрация конвейера (Decode → Parse → Validate) вынесена в [PipelineManager](pipeline_manager.md) для соблюдения SRP.

---

## Dependency Injection (Assembly)

Ниже показано, как Composition Root (`main.py`) собирает все компоненты. `ForzaCore` зависит только от интерфейсов и не знает о конкретных реализациях.

```mermaid
classDiagram
    class CompositionRoot["main.py (Bootstrap)"] {
        +bootstrap_dependencies()
    }

    class ForzaCore {
        -IUdpListener listener
        -IPipelineManager pipeline
        +__init__(listener, pipeline)
        +start_tracking()
        +stop_tracking()
    }

    class UdpListener {
        +start(host, port)
        +stop()
    }
    class WhitelistSourceValidator {
        +is_allowed(ip) bool
    }
    class TokenBucketRateLimiter {
        +allow(ip) bool
    }
    class PipelineManager {
        +start()
        +stop()
        +enqueue(packet)
    }
    class PacketDecoderFactory {
        -_registry: Map~int  IPacketDecoder~
        +get_decoder(size) IPacketDecoder
    }
    class Fm7Decoder { +decode(bytes) }
    class Fh4Decoder { +decode(bytes) }
    class Fh5Decoder { +decode(bytes) }
    class PacketParser { +parse(raw) }
    class TelemetrySanityValidator { +validate(packet) }

    CompositionRoot ..> ForzaCore : creates
    CompositionRoot ..> UdpListener : creates
    CompositionRoot ..> WhitelistSourceValidator : creates
    CompositionRoot ..> TokenBucketRateLimiter : creates
    CompositionRoot ..> PipelineManager : creates
    CompositionRoot ..> PacketDecoderFactory : creates
    CompositionRoot ..> PacketParser : creates
    CompositionRoot ..> TelemetrySanityValidator : creates

    ForzaCore o-- IUdpListener
    ForzaCore o-- IPipelineManager

    IUdpListener <|.. UdpListener
    UdpListener o-- ISourceValidator
    UdpListener o-- IRateLimiter
    ISourceValidator <|.. WhitelistSourceValidator
    IRateLimiter <|.. TokenBucketRateLimiter

    IPipelineManager <|.. PipelineManager
    PipelineManager o-- IPacketDecoderFactory
    PipelineManager o-- IPacketParser
    PipelineManager o-- IPacketValidator

    IPacketDecoderFactory <|.. PacketDecoderFactory
    PacketDecoderFactory ..> Fm7Decoder : registry (311b)
    PacketDecoderFactory ..> Fh4Decoder : registry (324b)
    PacketDecoderFactory ..> Fh5Decoder : registry (331b)
    IPacketParser <|.. PacketParser
    IPacketValidator <|.. TelemetrySanityValidator
```

Через интерфейсы внутрь `ForzaCore` инжектируются:
* `IUdpListener` — сетевой I/O, Source Validation (делегирует `ISourceValidator`), Rate Limiting (делегирует `IRateLimiter`), Timestamping
* `IPipelineManager` — оркестрация Decode → Parse → Validate, управление очередями и воркерами

`ForzaCore` связывает их: `listener.on_packet = pipeline.enqueue`.

---

## Управление состоянием (Жизненный цикл)

```mermaid
flowchart TB
    Stopped["Stopped"]
    Starting["Starting"]
    Listening["Listening (Main Loop)"]
    Stopping["Stopping"]
    Error["Error"]

    Stopped -->|"start_tracking() / init queue, bind port"| Starting
    Stopped -->|"stop_tracking() / ignore"| Stopped

    Starting -->|"[port bound successfully] / start listener + pipeline"| Listening
    Starting -->|"[port already in use] / throw AddressError"| Error

    Error -->|"[recover]"| Stopped

    Listening -->|"stop_tracking() / stop listener + pipeline"| Stopping
    Listening -->|"start_tracking() / ignore, log warning"| Listening

    Stopping -->|"[resources freed]"| Stopped
    Stopping -->|"stop_tracking() / ignore"| Stopping

    classDef stateNode fill:#d4e5ff,stroke:#5c8ce6,stroke-width:2px,color:#000;
    classDef errorNode fill:#f9d0c4,stroke:#e84a5f,stroke-width:2px,color:#000;

    class Stopped,Starting,Listening,Stopping stateNode;
    class Error errorNode;
```

---

## Методы `start_tracking()` и `stop_tracking()`

При вызове `start_tracking()` фасад последовательно:
1. Запускает `pipeline.start()` — инициализирует очереди и воркеры
2. Устанавливает callback: `listener.on_packet = pipeline.enqueue`
3. Запускает `listener.start(host, port)` — начинает чтение из сети

При вызове `stop_tracking()` — в обратном порядке:
1. `listener.stop()` — прекращает чтение
2. `pipeline.stop()` — дожидается обработки оставшейся очереди и останавливает воркеры

* **Идемпотентность**: повторный `start_tracking()` при уже запущенном цикле логирует предупреждение и игнорируется (не вызывает "Port in use"). Аналогично `stop_tracking()` у остановленного модуля.

---

## Execution Model

Подробности асинхронного выполнения, Producer-Consumer паттерна и управления потоками: **[Execution Model](execution_model.md)**
