# Спецификация компонентов системы **FH Telemetry Tuner**

**Архитектурный стиль:** Containerized Modular Monolith / Service-based Architecture  
**Основной протокол обмена:** Database-centric (асинхронный обмен через БД)

---

## 1. Контейнер: `forza_core` (Ingestion Engine)

**Роль:** Сборщик телеметрии и менеджер состояния  
**Тип запуска:** `restart: always` (Daemon)

### Ответственность
Это «сердце» real-time части. Он должен быть максимально лёгким и быстрым, чтобы не терять UDP-пакеты.

### Технические детали
- **Стек:** Python 3.11+ (`asyncio`)
- **Сетевой интерфейс:** проброс порта `5300/udp` (Host → Container)
- **Ключевые библиотеки:**
  - `asyncpg` — быстрая запись в PostgreSQL
  - `struct` — парсинг бинарных данных

### Логика работы
- **UDP Listener**
  - Асинхронный сервер
  - Принимает байт-поток (`324 байта / пакет`)
- **Binary Parser**
  - Преобразует байты в Python-словарь или `dataclass`
- **State Machine (машина состояний)**
  - Анализирует флаг `IsRaceOn`
    - `1` — гонка
    - `0` — меню / пауза
  - **Start Trigger**
    - Переход `0 → 1`
    - Генерирует новый `UUID (session_id)`
    - Фиксирует время старта
  - **End Trigger**
    - Переход `1 → 0`
    - Закрывает сессию
    - Фиксирует время финиша
- **Batch Writer**
  - Не пишет каждый пакет отдельно
  - Буферизация (например, `100 пакетов` или `1 секунда`)
  - Пакетная запись через `COPY` или `INSERT` в TimescaleDB

### Взаимодействие
- **Write →** `forza_db` (`telemetry_raw`)

---

## 2. Контейнер: `forza_db` (Data Warehouse)

**Роль:** Центральное хранилище данных и временных рядов  
**Тип запуска:** `restart: always` (Stateful Service)

### Ответственность
Надёжное хранение больших объёмов данных и быстрый доступ для аналитики.

### Технические детали
- **Образ:** `timescale/timescaledb:latest-pg14`
- **Persistence:** Docker Volume (обязательно)

### Структура данных (схема)

#### Hypertable `telemetry_raw`
- Тайм-серии (partition by time)
- Привязка к `session_id`
- Политика Data Retention  
  - Авто-удаление старых данных (например, 30 дней)

#### Table `sessions`
- `session_id`
- `car_id`
- `track_id`
- `date`
- `duration`
- `best_lap`

#### Table `analysis_results`
- Результаты AI-анализа
- Рекомендации по настройкам (подвеска, давление шин и т.д.)

---

## 3. Контейнер: `forza_dashboard` (Visualization)

**Роль:** Пользовательский интерфейс и BI-аналитика  
**Тип запуска:** `restart: always`

### Ответственность
Предоставление понятных визуализаций на основе данных БД.

### Технические детали
- **Образ:** `grafana/grafana:latest`
- **Порт:** `3000/tcp`  
  - Доступ: `http://localhost:3000`

### Конфигурация
- **Provisioning**
  - Автоматическое подключение к `forza_db`
  - Datasource as Code
- **Dashboards**
  - **Live Telemetry**
    - Автообновление: 1 секунда
    - Данные активной сессии
  - **Historical Analysis**
    - Выбор сессии
    - Детальный разбор заезда

### Взаимодействие
- **Read ←** `forza_db` (SQL)

---

## 4. Контейнер: `forza_ai` (Offline Analyst)

**Роль:** ML-обработчик и генератор инсайтов  
**Тип запуска:** `profiles: ["analysis"]`  
(Запускается вручную / скриптом и завершает работу)

### Ответственность
Тяжёлая аналитика завершённых заездов без влияния на ingestion.

### Технические детали
- **Стек:** Python
  - PyTorch / TensorFlow
  - Scikit-learn
  - Pandas
- **Жизненный цикл:** Ephemeral  
  - Запуск → обработка → завершение

### Логика работы (Job Flow)
1. **Fetch**
   - Аргументы: `--last`, `--session_id=...`
   - SQL-запрос к `forza_db`
   - Загрузка данных в `Pandas DataFrame`
2. **Process**
   - Анализ подвески (гистограммы хода амортизаторов)
   - Анализ сцепления шин
   - Поиск аномалий в поворотах
3. **Insight Generation**
   - Генерация человеко-читаемых советов  
     - Пример: *«Смягчи передний отбой на 2 клика»*
4. **Commit**
   - Запись JSON-результатов в `analysis_results`
5. **Exit**
   - Завершение с кодом `0`

### Взаимодействие
- **Read / Write ↔** `forza_db`

---

## 5. Контейнер: `forza_admin` (Admin Toolset)

**Роль:** Администрирование БД (DBA)  
**Тип запуска:** `restart: always` (или профиль `tools`)

### Ответственность
GUI-доступ к базе данных для разработки и отладки.

### Технические детали
- **Образ:** `dpage/pgadmin4`
- **Порт:** `5050/tcp`
- **Авторизация:** логин / пароль из `.env`

### Use Cases
- Проверка, пишутся ли данные
- Удаление тестовых заездов (`TRUNCATE`, `DELETE`)
- Анализ размера таблиц

---

## Сводная схема потоков данных

```mermaid
graph TD
    Game[Forza Horizon] -- UDP 5300 --> Core[forza_core]
    
    subgraph Docker Network [forza_net]
        Core -- Batch Insert --> DB[(forza_db / Timescale)]
        
        Dashboard[forza_dashboard] -- SELECT --> DB
        
        AI[forza_ai] -- SELECT Raw Data --> DB
        AI -- INSERT Insights --> DB
        
        Admin[forza_admin] -- Manage --> DB
    end
    
    User((User)) -- Browser :3000 --> Dashboard
    User -- Browser :5050 --> Admin
    User -- Manual Start --> AI
