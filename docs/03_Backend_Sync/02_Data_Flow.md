# Data Flow Process

```mermaid
sequenceDiagram
    participant UI as UI
    participant Game as Game
    participant Core as forza_core
    participant Buf as LocalBuffer
    participant Sync as SyncWorker
    participant EventBus as SignalBus
    participant API as Backend API

    loop while session is active
        Game->>Core: UDP Datagram
        Note right of Core: No wait network
        Core->>Core: Validate packet size/magic number
        Core->>Buf: put_nowait(TelemetryDTO)
    end

    loop On BatchReady Event Triggered
        Sync->>Buf: with Buf.transaction_n(N) as batch
        Buf-->>Sync: List[TelemetryDTO]
        Sync->>API: HTTPS POST /api/telemetry/batch (Headers: Authorization Bearer JWT)
        
        alt if Authorized & Network OK
            API-->>Sync: 200 OK
            Note right of Buf: _commit() auto-called on clean exit
        else 401 Unauthorized (No/Invalid JWT)
            API-->>Sync: 401 Unauthorized
            Sync->>EventBus: emit BackendErrorEvent(401)
            EventBus->>UI: show error popup
            Sync->>Sync: log.error("Auth failed") & raise exception
            Note right of Buf: _rollback() auto-called on exception
        else Network Error / Timeout
            API--xSync: Timeout / 500 Error
            Sync->>EventBus: emit BackendErrorEvent(NetworkError)
            EventBus->>UI: show error popup
            Sync->>Sync: log.warning("Network issue") & raise exception
            Note right of Buf: _rollback() auto-called on exception
        end
    end

    opt on User clicks Stop Session
        UI->>Sync: stop_sync()
        Sync->>Buf: with Buf.transaction() as remaining
        Buf-->>Sync: List[TelemetryDTO]
        Sync->>API: HTTPS POST /api/telemetry/batch (Final, Headers: Auth JWT)
        API-->>Sync: 200 OK
        Note right of Buf: _commit() (auto)
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

### Configuration & Local Paths
> [!IMPORTANT]
> **Защита от утечки данных (Data Leak) и обхода каталога (Path Traversal):**
> 1. Все пути (`pathlib.Path`), передаваемые через конфигурацию или `.env` файлы к локальным ресурсам (модели AI, UI-формы), обязаны валидироваться: путь должен разрешаться (`.resolve()`) и строго входить в границы `BASE_DIR` (`is_relative_to(BASE_DIR)`). Это предотвращает атаки с использованием символических ссылок и `../`.
> 2. При обработке ошибок валидации (`pydantic.ValidationError`) во время загрузки конфигурации категорически запрещено логировать сам объект исключения целиком. Для извлечения структуры ошибки следует использовать методы `e.errors(include_input=False)`, гарантирующие отсутствие пользовательского ввода или критических данных (как пароли или DSN-ссылки) в логах.

## Transport
HTTPS POST батчами (batches) является утвержденным и оптимальным транспортом для текущей архитектуры (stateless backend). Данный подход минимизирует количество HTTP-запросов и обеспечивает надежную передачу телеметрии.

