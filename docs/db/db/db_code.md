// ==========================================
// 1. АВТОМОБИЛИ (Справочник)
// ==========================================
Table Cars {
  id integer [primary key, increment]
  manufacturer varchar
  model varchar
  year integer
  game_ordinal integer
}

// ==========================================
// 2. БИЛД: СТАТИСТИКА (Hot Table)
// Сюда стучимся постоянно для фильтров и сортировок
// ==========================================
Table BuildStats {
  id integer [primary key, increment]
  car_id integer [ref: > Cars.id]
  
  // Ключевые метрики производительности
  pi_rating integer [note: "800, 900, 998"]
  car_class CarClass
  
  // Физика (Результат установки деталей)
  horsepower_kw integer
  torque_nm integer
  weight_kg integer
  weight_distribution float [note: "Развесовка (Front %)"]
  
  // Конфигурация привода (влияет на физику, нужно часто)
  drivetrain DrivetrainType
  engine_location EngineLocation
  
  // Флаги возможностей (для UI и валидации тюнинга)
  has_adjustable_aero_front boolean
  has_adjustable_aero_rear boolean
  
  created_at datetime
}

// ==========================================
// 3. БИЛД: ЗАПЧАСТИ (Cold Table)
// Запрашиваем только когда открываем карточку конкретного билда
// Связь 1 к 1 с BuildStats
// ==========================================
Table BuildParts {
  build_id integer [primary key, ref: - BuildStats.id] // Тот же ID, что у Stats
  
  // Важные детали выносим в колонки (влияют на категорию гонок)
  tire_compound varchar [note: "Slick, Rally, Drift, Street..."]
  tire_width_front integer [note: "mm, например 245"]
  tire_width_rear integer [note: "mm, например 315"]
  
  // Свапы (очень важно для понимания билда)
  engine_swap_name varchar [note: "Например '3.0L I6 TT' или NULL (сток)"]
  aspiration_swap_type varchar [note: "Twin Turbo, Supercharger..."]
  body_kit_name varchar [note: "Например 'Rocket Bunny'"]

  // Остальные детали (двигатель, ходовая) храним в JSONB.
  // Делать 50 колонок (camshaft, pistons, flywheel...) — это "Over-normalization".
  // JSONB позволяет гибко хранить список установленных улучшений.
  engine_parts jsonb [note: "{intake: 'Race', ignition: 'Sport', ...}"]
  platform_parts jsonb [note: "{brakes: 'Race', springs: 'Rally', ...}"]
  drivetrain_parts jsonb [note: "{clutch: 'Stock', transmission: '10 Speed', ...}"]
}

// ==========================================
// 4. НАСТРОЙКИ (TUNES) - С ЗАЩИТОЙ ДАННЫХ
// Добавляем ограничения, чтобы в базу не попал мусор
// ==========================================
Table Tunes {
  id integer [primary key, increment]
  build_id integer [ref: > BuildStats.id] 
  name varchar [not null]
  description varchar
  created_at datetime [default: `now()`]
  
  // --- Шины (Bar) ---
  // Constraint: Давление не может быть отрицательным или > 10 бар (взрыв)
  tire_pressure_front float [note: "CHECK(value > 0 AND value < 10)"]
  tire_pressure_rear float  [note: "CHECK(value > 0 AND value < 10)"]
  
  // --- Геометрия (Градусы) ---
  // Развал в игре обычно от -5.0 до +5.0
  camber_front float [note: "CHECK(value BETWEEN -10 AND 10)"]
  camber_rear float
  // Кастер обычно положительный 1.0 - 7.0
  caster_front float [note: "CHECK(value BETWEEN 0 AND 10)"]
  
  // --- Тормоза ---
  // Баланс это %, он не может быть > 100% (1.0)
  brake_balance float [note: "CHECK(value BETWEEN 0 AND 1)"]
  brake_pressure float [note: "CHECK(value BETWEEN 0 AND 2.0)"] // 200% макс

  // Остальные поля...
  // JSONB отлично подходит для gear_ratios, но валидировать его придется в коде приложения
  gear_ratios jsonb 
}

// ==========================================
// 5. СЕССИИ
// ==========================================
Table Sessions {
  id integer [primary key, increment]
  tune_id integer [ref: > Tunes.id]
  track_name varchar
  // Вместо строк "Sunny", "Rain" лучше использовать Enum или ID справочника погоды
  weather_type varchar 
  recorded_at datetime [default: `now()`]
  duration_seconds float
}

// ==========================================
// 6. ТЕЛЕМЕТРИЯ (TIME-SERIES)
// Оптимизировано для TimescaleDB
// ==========================================




// ==========================================
// ENUMS (Ваши + Новые)
// ==========================================

Enum CarClass {
  D
  C
  B
  A
  S1
  S2
  X
}

Enum DrivetrainType {
  RWD
  FWD
  AWD
}

Enum EngineLocation {
  Front
  Mid
  Rear
}

