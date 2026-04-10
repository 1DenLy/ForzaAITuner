# Cycle of Processing Packets

> **Словарь терминов:**
> * **Decode** — преобразование сырых байт в набор примитивов (float, int). Ответственность `IPacketDecoder`.
> * **Parse** — преобразование набора примитивов в доменную модель (`TelemetryPacket`). Ответственность `IPacketParser`.
> * **Validate** — проверка адекватности данных (NaN, диапазоны, бизнес-правила). Ответственность `IPacketValidator`.
> * **Drop** — пакет отброшен. Каждый drop фиксируется счётчиком метрик.

---

## Core Data Pipeline

Два слоя обработки: **Producer** (I/O) и **Consumer** (бизнес-логика), разделённые неблокирующей очередью.

```mermaid
flowchart LR
    Input["UDP Socket"]

    subgraph Producer["Producer — UdpListener (I/O)"]
        direction LR
        S0("① Source Validation\n[ISourceValidator]")
        S1("② Rate Limiting\n[IRateLimiter]")
        S2("③ Timestamping\n[UdpListener]")
    end

    Queue["InQueue\n(RawPacket)"]

    subgraph Consumer["Consumer — PipelineManager (CPU)"]
        direction LR
        S3("④ Decode\n[IPacketDecoder]")
        S4("⑤ Parse\n[IPacketParser]")
        S5("⑥ Validate\n[IPacketValidator]")
    end

    Output["Exit (OutQueue)\nTelemetryPacket + timestamp"]
    Metrics["Metrics\n(counters)"]
    DLQ["Dead Letter Queue\n(payload + reason)"]

    Input --> S0
    S0 -->|"✅ IP White"| S1
    S0 -->|"❌ Unknown IP"| Metrics
    S1 -->|"✅ In limit"| S2
    S1 -->|"❌ Exceeded limit"| Metrics
    S2 --> Queue
    Queue --> S3
    S3 -->|"✅ Decoded"| S4
    S3 -->|"❌ Unknown size"| Metrics
    S3 -->|"❌ Corrupt bytes"| DLQ
    S4 -->|"✅ Parsed"| S5
    S4 -->|"❌ struct.error"| DLQ
    S5 -->|"✅ Valid"| Output
    S5 -->|"❌ NaN / anomaly"| DLQ
```

*Описание шагов:*

| # | Шаг | Компонент | Слой | Обязанность |
|---|-----|-----------|------|-------------|
| ① | Source Validation | `ISourceValidator` | Infrastructure | Отклонить пакеты с неизвестных IP (→ только метрика) |
| ② | Rate Limiting | `IRateLimiter` | Infrastructure | Не пропускать более N пакетов/сек (→ только метрика) |
| ③ | Timestamping | `UdpListener` | Infrastructure | Проставить `received_at` сразу после `recvfrom()` |
| ④ | Decode | `IPacketDecoder` | Application | Байты → примитивы + инъекция `received_at`. Версия Forza через `IPacketDecoderFactory` |
| ⑤ | Parse | `IPacketParser` | Domain | Примитивы → `TelemetryPacket` (чистый маппинг, без валидации) |
| ⑥ | Validate | `IPacketValidator` | Domain | Sanity Check + бизнес-правила (Chain of Responsibility) |

> [!IMPORTANT]
> **Разделение дропов:**
> * Сетевые дропы (①②) → **только метрики** (без DLQ). Защита от DoS на I/O-уровне логирования.
> * Дропы данных (④⑤⑥) → **DLQ с payload + метрики**. Диагностическая ценность для дебага.

---

## IPacketDecoderFactory: Registry Pattern

Фабрика использует реестр (`Map<int, IPacketDecoder>`) для выбора декодера. Добавление нового декодера — регистрация записи, не правка условий (OCP).

```mermaid
flowchart TD
    Factory["PacketDecoderFactory\n.get_decoder(size: int)\n\nregistry: Map⟨int, IPacketDecoder⟩"]
    FM7["Fm7Decoder\n(size = 311 bytes)"]
    FH4["Fh4Decoder\n(size = 324 bytes)"]
    FH5["Fh5Decoder\n(size = 331 bytes)"]
    Unknown["❌ drop → Metrics\n(неизвестный размер)"]

    Factory -->|"311"| FM7
    Factory -->|"324"| FH4
    Factory -->|"331"| FH5
    Factory -->|"иной"| Unknown
```

---

## Happy Path: Sequence Diagram

Успешный путь прохождения пакета. Обратите внимание на границу между Producer (async I/O) и Consumer (CPU worker).

```mermaid
sequenceDiagram
    participant UDP as UDP Socket
    participant Listener as UdpListener
    participant SV as ISourceValidator
    participant RL as IRateLimiter
    participant Queue as InQueue
    participant PM as PipelineManager Worker
    participant Factory as IPacketDecoderFactory
    participant Decoder as IPacketDecoder
    participant Parser as IPacketParser
    participant Validator as IPacketValidator
    participant Out as OutQueue

    loop Постоянное чтение (async I/O thread)
        UDP->>Listener: recvfrom(512) → (bytes, addr)

        Listener->>SV: is_allowed(addr.ip)
        SV-->>Listener: true

        Listener->>RL: allow(addr.ip)
        RL-->>Listener: true

        Listener->>Listener: ③ stamp received_at = now()

        Listener->>Queue: enqueue(RawPacket)
    end

    loop Worker (ThreadPool / ProcessPool)
        Queue->>PM: dequeue() → RawPacket

        PM->>Factory: get_decoder(len(data))
        Factory-->>PM: IPacketDecoder

        PM->>Decoder: decode(data, received_at)
        Decoder-->>PM: RawTelemetry

        PM->>Parser: parse(RawTelemetry)
        Parser-->>PM: TelemetryPacket

        PM->>Validator: validate(TelemetryPacket)
        Validator-->>PM: ValidationResult(is_valid=true)

        PM->>Out: enqueue(TelemetryPacket)
    end
```

---

## Error Handling & Dead Letter Queue

Что происходит с каждым типом «плохого» пакета. Сетевые дропы → только метрики. Дропы данных → DLQ + метрики.

```mermaid
sequenceDiagram
    participant UDP as UDP Socket
    participant Listener as UdpListener
    participant SV as ISourceValidator
    participant RL as IRateLimiter
    participant Queue as InQueue
    participant PM as PipelineManager Worker
    participant Factory as IPacketDecoderFactory
    participant Decoder as IPacketDecoder
    participant Parser as IPacketParser
    participant Validator as IPacketValidator
    participant Metrics as MetricsCollector
    participant DLQ as Dead Letter Queue

    UDP->>Listener: recvfrom(512) → (bytes, addr)

    alt ❌ Неизвестный IP (Source Validation)
        Listener->>SV: is_allowed(addr.ip)
        SV-->>Listener: false
        Listener->>Metrics: counter_inc("drop.unknown_source")
        Note over Listener: DLQ НЕ пишется (защита от DoS I/O)
    else ❌ Превышен Rate Limit
        Listener->>RL: allow(addr.ip)
        RL-->>Listener: false
        Listener->>Metrics: counter_inc("drop.rate_limit")
        Note over Listener: DLQ НЕ пишется (защита от DoS I/O)
    else ✅ IP валиден, лимит не превышен
        Listener->>Queue: enqueue(RawPacket)

        Queue->>PM: dequeue() → RawPacket
        PM->>Factory: get_decoder(len(data))

        alt ❌ Неизвестный размер пакета
            PM->>Metrics: counter_inc("drop.unknown_size")
            Note over PM: DLQ НЕ пишется (нет диагностической ценности)
        else ✅ Декодер найден
            Factory-->>PM: IPacketDecoder
            PM->>Decoder: decode(data, received_at)

            alt ❌ Ошибка декодирования (corrupt bytes)
                PM->>DLQ: log(data, reason=DECODE_ERROR)
                PM->>Metrics: counter_inc("drop.decode_error")
            else ✅ RawTelemetry получен
                Decoder-->>PM: RawTelemetry
                PM->>Parser: parse(RawTelemetry)

                alt ❌ struct.error / невозможность маппинга
                    PM->>DLQ: log(raw, reason=PARSE_ERROR)
                    PM->>Metrics: counter_inc("drop.parse_error")
                else ✅ TelemetryPacket сформирован
                    Parser-->>PM: TelemetryPacket
                    PM->>Validator: validate(TelemetryPacket)

                    alt ❌ NaN / аномальные значения / бизнес-правило
                        PM->>DLQ: log(packet, reason=VALIDATION_FAILED)
                        PM->>Metrics: counter_inc("drop.validation_failed")
                    else ✅ TelemetryPacket валиден
                        Validator-->>PM: ValidationResult(is_valid=true)
                        Note over PM: Пакет успешно обработан → OutQueue
                    end
                end
            end
        end
    end
```

> **Ключевой принцип:** сетевые дропы логируются **только в метрики** (защита от DoS на I/O логирования). Payload сохраняется в DLQ **только** для DECODE_ERROR, PARSE_ERROR и VALIDATION_FAILED — то есть там, где нужны данные для дебага.
