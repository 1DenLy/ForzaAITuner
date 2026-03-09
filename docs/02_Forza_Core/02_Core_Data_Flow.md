# Core Data Flow

## Суть
Как данные летят от игры до наружной очереди. Описание пути данных от момента их отправки игрой до попадания в наружную очередь для потребителей (от игры до UI/Backend).

## Core Data Ingestion Pipeline
```mermaid
flowchart LR
    %% Контекст Зоны А
    subgraph CorePipeline["Zone A: Core Data Ingestion Pipeline / IngestionService"]
        direction LR
        
        UdpListener["UdpListener"]
        
        subgraph PacketParserBlock["PacketParser"]
            direction TB
            Deserialize["Десериализация"]
            SanityCheck{"Sanity Check"}
            Deserialize --> SanityCheck
        end
        
        DataValidator["DataValidator"]
        IOutQueue[("Out Queue")]
        
        %% Связи внутри IngestionService
        UdpListener -- "Сырые байты" --> Deserialize
        
        SanityCheck -- "Фильтр пройден" --> DataValidator
        SanityCheck -. "Мусор/Ошибки" .-> Drop(("Drop Packet"))
        
        DataValidator -- "Валидный DTO" --> IOutQueue
    end
    
    UI["UI Components"]
    
    %% Связь наружу
    IOutQueue ==>|"Безопасные, отфильтрованные данные"| UI
    
    %% Стилизация для наглядности
    classDef untrusted fill:#f9d0c4,stroke:#e84a5f,stroke-width:2px,color:#000;
    classDef queue fill:#d4e5ff,stroke:#5c8ce6,stroke-width:2px,color:#000;
    classDef check fill:#ffe6cc,stroke:#ff9933,stroke-width:2px,color:#000;
    classDef secure fill:#dcf2d8,stroke:#66b266,stroke-width:2px,color:#000;
    
    class UdpListener untrusted;
    class IOutQueue queue;
    class SanityCheck,DataValidator check;
    class UI secure;
```

*Примечание к схеме:*
* **UdpListener** выступает как недоверенный источник данных.
* **Sanity Check** включает внутри себя базовый фильтр размера пакета и валидацию на `NaN`.

## How it works (По шагам)
1. **Получение UDP**: Приложение слушает UDP-порт и получает сырые байты от игры.
2. **Валидация размера пакета**: На самом раннем этапе (немедленно после `recvfrom`) отсеиваются пакеты с некорректным размером. Это происходит **строго до** попадания в пайплайн обработки и аллокации памяти под объекты.
3. **Парсинг**: Сырые байты десериализуются в понятную структуру данных (DTO) с помощью `PacketParser`.
4. **Sanity Check**: Выполняется валидация распакованных данных (проверка на `NaN`, отрицательные или нереалистичные значения) с помощью `DataValidator`.
5. **Отправка в OutQueue**: Полностью валидный `TelemetryDTO` передается в наружную очередь (IOutQueue), откуда его забирают другие модули (UI).

## Укороченная Sequence Diagram передачи данных
```mermaid
sequenceDiagram
    participant Game as ForzaGame
    participant Facade as CoreFacade
    participant Udp as UdpTransport
    participant Ingestion as IngestionService
    participant Parser as PacketParser
    participant Queue as OutQueue
    participant Consumer as UI / Backend

    Consumer->>Facade: start()
    Facade->>Udp: bind_port()
    
    Game->>Udp: send_bytes()
    
    alt valid_length
        Udp->>Ingestion: process_packet(bytes)
        Ingestion->>Parser: parse(bytes)
        Parser-->>Ingestion: DTO
        Ingestion->>Ingestion: sanity_check(DTO)
        
        alt valid_dto
            Ingestion->>Queue: put(DTO)
            Queue-->>Consumer: get() -> DTO
        else bad_data
            Ingestion->>Ingestion: drop & log(RateLimited)
        end
    else bad_length
        Udp->>Udp: drop_packet
    end
```
