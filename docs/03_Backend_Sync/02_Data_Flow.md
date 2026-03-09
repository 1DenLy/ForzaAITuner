# Data Flow Process

```mermaid
sequenceDiagram
    participant UI as UI
    participant Game as Game
    participant Core as forza_core
    participant Buf as LocalBuffer
    participant Sync as SyncWorker
    participant API as Backend API

    loop while session is active
        Game->>Core: UDP Datagram
        Note right of Core: No wait network
        Core->>Core: Validate packet size/magic number
        Core->>Buf: put_nowait(TelemetryDTO)
    end

    loop On BatchReady Event Triggered
        Sync->>Buf: take_batch(N)
        Buf-->>Sync: List[TelemetryDTO]
        Sync->>API: HTTPS POST /api/telemetry/batch (Headers: Authorization Bearer JWT)
        
        alt if Authorized & Network OK
            API-->>Sync: 200 OK
            Sync->>Buf: commit() / delete_batch()
        else 401 Unauthorized (No/Invalid JWT)
            API-->>Sync: 401 Unauthorized
            Sync->>Sync: log.error("Auth failed, stop syncing or refresh token")
        else Network Error / Timeout
            API--xSync: Timeout / 500 Error
            Sync->>Sync: log.warning("Keep data in buffer")
        end
    end

    opt on User clicks Stop Session
        UI->>Sync: stop_sync()
        Sync->>Buf: take_ALL_remaining()
        Buf-->>Sync: List[TelemetryDTO]
        Sync->>API: HTTPS POST /api/telemetry/batch (Final, Headers: Auth JWT)
        API-->>Sync: 200 OK / 401 Unauthorized
        Sync-->>UI: status = "Session Saved & Closed"
    end
```

## How it works:
1. The game constanty streams **UDP Datagrams**, which are processed by `forza_core` and immediately stored in the **LocalBuffer**.
2. The **SyncWorker** periodically takes a batch of data and attempts to send it to the **Backend API**.
3. If the connection fails, data remains in the buffer.
4. When the session is stopped, all remaining data is force-synced to ensure no loss.

## Security & Logging
> [!CAUTION]
> **Архитектурное правило безопасности:** Все логирующие компоненты (и особенно `SyncWorker`), взаимодействующие с API, обязаны использовать фильтр (например, `logging.Filter`), который по регулярному выражению заменяет токены в заголовке `Authorization: Bearer ...` на `***`. Это исключает риск утечки JWT в файлы логов.

## Transport
HTTPS POST батчами (batches) является утвержденным и оптимальным транспортом для текущей архитектуры (stateless backend). Данный подход минимизирует количество HTTP-запросов и обеспечивает надежную передачу телеметрии.

