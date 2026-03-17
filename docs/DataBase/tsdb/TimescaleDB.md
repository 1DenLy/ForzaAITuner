# Модель временных рядов (TimescaleDB)

Спроектирована для максимального сжатия и скорости записи потоковых UDP данных. Поля полностью соответствуют спецификации Forza Horizon (Data Out) и доменной модели `TelemetryPacket`.

## 1. Таблица `telemetry`

* **Primary Keys (Composite):** `time` (Timestamptz) и `session_id` (UUID, Index). 
* **Примечание:** TimescaleDB требует, чтобы колонка времени (`time`) была частью первичного ключа.

### 1.1 Метаданные и Двигатель
* `session_id` (UUID, Index) — ID сессии (часть композитного ПК).
* `tuning_config_id` (UUID, Index, Nullable) — ID активной конфигурации тюнинга.
* `IsRaceOn` (SmallInt) — 1 при активном заезде, 0 в меню.
* `TimestampMS` (BigInt) — внутренний таймштамп пакета в мс (может сбрасываться в 0).
* `EngineMaxRpm`, `EngineIdleRpm`, `CurrentEngineRpm` (Float4)
* `Power`, `Torque` (Float4) — мощность (ватты) и крутящий момент (Н·м).
* `Boost`, `Fuel` (Float4)
* `NumCylinders` (SmallInt) — количество цилиндров.

### 1.2 Динамика и Векторы (Локальное пространство авто)
*Для всех векторов: X = вправо (right), Y = вверх (up), Z = вперед (forward).*

* `AccelerationX`, `AccelerationY`, `AccelerationZ` (Float4) — ускорение в локальных осях.
* `VelocityX`, `VelocityY`, `VelocityZ` (Float4) — скорость в локальных осях.
* `AngularVelocityX` (Pitch), `AngularVelocityY` (Yaw), `AngularVelocityZ` (Roll) (Float4).
* `Yaw`, `Pitch`, `Roll` (Float4) — углы ориентации кузова.

### 1.3 Позиционирование и Скорость
* `PositionX`, `PositionY`, `PositionZ` (Float4) — мировые координаты.
* `Speed` (Float4) — общая скорость в метрах в секунду (м/с).
* `DistanceTraveled` (Float4) — общее пройденное расстояние.

### 1.4 Подвеска и Колеса (FL, FR, RL, RR)
Группы полей для четырех колес: FrontLeft, FrontRight, RearLeft, RearRight.

* `NormalizedSuspensionTravel*` (Float4) — ход подвески (0.0 = растяжение, 1.0 = сжатие).
* `SuspensionTravelMeters*` (Float4) — фактический ход подвески в метрах.
* `TireSlipRatio*` (Float4) — коэффициент продольного скольжения (0 = зацеп, >1.0 = срыв).
* `TireSlipAngle*` (Float4) — угол увода (боковое скольжение).
* `TireCombinedSlip*` (Float4) — комбинированное скольжение.
* `WheelRotationSpeed*` (Float4) — скорость вращения колес (рад/сек).
* `WheelOnRumbleStrip*` (SmallInt) — флаг наезда на поребрик (1 = на поребрике, 0 = нет).
* `WheelInPuddleDepth*` (Float4) — глубина лужи (0.0 to 1.0).
* `SurfaceRumble*` (Float4) — вибрация поверхности (FFB).
* `TireTemp*` (Float4) — температура шин.

### 1.5 Ввод управления (Inputs)
* `Accel`, `Brake`, `Clutch`, `HandBrake` (SmallInt) — значения 0-255.
* `Gear` (SmallInt) — текущая передача (0-15).
* `Steer` (SmallInt) — поворот руля (-127 to 127).
* `NormalizedDrivingLine`, `NormalizedAIBrakeDifference` (SmallInt).

### 1.6 Гоночные данные и Автомобиль
* `BestLap`, `LastLap`, `CurrentLap`, `CurrentRaceTime` (Float4) — время кругов и гонки.
* `LapNumber`, `RacePosition` (SmallInt).
* `CarOrdinal` (Int) — уникальный ID модели автомобиля.
* `CarClass` (SmallInt) — класс (0=D, 7=X).
* `CarPerformanceIndex` (SmallInt) — PI (100-999).
* `DrivetrainType` (SmallInt) — привод (0=FWD, 1=RWD, 2=AWD).
* `HorizonPlaceholder` (SmallInt, Nullable) — зарезервировано (unknown FH4 values).

---

## 2. Конфигурация TimescaleDB

Настроена гипертаблица (hypertable) по колонке `time`.

### 2.1 Оптимизация
* **Сжатие (Compression):** Включено. Сегментация (Segment by) выполняется по `session_id` (UUID) для обеспечения высокой производительности при выборке телеметрии конкретного заезда.
* **Автоматизация:** Таблица создается средствами SQLAlchemy в `init_telemetry_db` с последующим вызовом `SELECT create_hypertable(...)`.
