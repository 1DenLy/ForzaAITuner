# Core Module Overview

## Суть
Верхнеуровневый взгляд на модуль `forza_core`. Модуль является исключительно "поставщиком" данных (Provider). Он не знает о базах данных, HTTP-запросах на бэкенд и пользовательском интерфейсе.

## Архитектура
```mermaid
flowchart LR
    %% Внешние системы
    Game["Forza Game"]
    UI["UI / Main Application"]
    DB[("PostgreSQL")]

    %% Главный модуль
    subgraph Core["Forza Core Module"]
        direction TB

        subgraph AppLayer["Applications"]
            direction TB
            CoreFacade["CoreFacade"]
            IngestionService["IngestionService"]
            PacketParser["PacketParser"]
            AppUdpTransport["UdpTransport"]
        end

        subgraph DomainLayer["Domain"]
            direction TB
            Models["Models"]
            Events["Events"]
            Interfaces["Interfaces"]
        end

        subgraph InfraLayer["Infrastructure"]
            direction TB
            InfraUdpTransport["UdpTransport"]
            PostgresRepo["PostgresRepository"]
            Logger["Logger"]
        end
    end

    %% Внешние связи
    Game -- "UDP Datagrams" --> AppUdpTransport
    UI -. "Uses" .-> CoreFacade
    PostgresRepo -- "SQL / TCP" --> DB

    %% Внутренние зависимости в Applications
    CoreFacade -.-> IngestionService
    IngestionService -.-> PacketParser
    
    %% Зависимости от Domain слоя
    PacketParser -.-> Models
    IngestionService -.-> Interfaces
    AppUdpTransport -.-> Interfaces

    %% Зависимости инфраструктуры
    PostgresRepo -.-> Interfaces

    %% Стилизация для наглядности (с черным текстом)
    classDef external fill:#f9d0c4,stroke:#e84a5f,stroke-width:2px,color:#000;
    classDef app fill:#d4e5ff,stroke:#5c8ce6,stroke-width:2px,color:#000;
    classDef domain fill:#dcf2d8,stroke:#66b266,stroke-width:2px,color:#000;
    classDef infra fill:#ffe6cc,stroke:#ff9933,stroke-width:2px,color:#000;
    classDef db fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000;

    class Game,UI external;
    class CoreFacade,IngestionService,PacketParser,AppUdpTransport app;
    class Models,Events,Interfaces domain;
    class InfraUdpTransport,PostgresRepo,Logger infra;
    class DB db;
```

## Component Brief

* **AppLayer**: Слой приложения, содержащий основные сервисы такие как `CoreFacade`, транспорт для получения данных (`UdpTransport`), пайплайн обработки (`IngestionService`) и логику парсинга сырых байтов (`PacketParser`).
* **DomainLayer**: Доменная логика, описывающая структуры данных и контракты. Включает строгие Pydantic модели (`Models`), интерфейсы (`Interfaces`) и события (`Events`).
* **InfraLayer**: Инфраструктурный слой (реализация интерфейсов). Содержит реализацию `UdpTransport`, работу с логгером (`Logger`) и репозиториями (`PostgresRepository`).
