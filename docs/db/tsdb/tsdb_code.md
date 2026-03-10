Table Telemetry {
  // Ключи
  time timestamptz [not null]
  session_id integer

  // --- Группа 1: Общая физика ---
  speed_mps float4 // float4 (real) экономит место (4 байта вместо 8 у double)
  rpm integer      // Обороты дробными не нужны
  gear integer
  
  // Вектор ускорений (X, Y, Z) - массив из 3 элементов
  g_force float4[] [note: "Index: 1=X (Side), 2=Y (Vert), 3=Z (Accel)"]
  
  // Углы кузова (Yaw, Pitch, Roll) - массив из 3 элементов
  body_angles float4[] [note: "Index: 1=Yaw, 2=Pitch, 3=Roll"]

  // --- Группа 2: Колеса (Отдельные колонки для аналитики) ---
  // Храним FL, FR, RL, RR отдельными колонками типа real/integer
  // В аналитических БД (Timescale) агрегация и поиск по элементам
  // массива часто убивает использование индексов и снижает производительность

  susp_travel_fl float4
  susp_travel_fr float4
  susp_travel_rl float4
  susp_travel_rr float4

  wheel_slip_fl float4
  wheel_slip_fr float4
  wheel_slip_rl float4
  wheel_slip_rr float4

  wheel_speed_fl float4
  wheel_speed_fr float4
  wheel_speed_rl float4
  wheel_speed_rr float4

  tire_temp_fl integer
  tire_temp_fr integer
  tire_temp_rl integer
  tire_temp_rr integer
  // --- Группа 3: Ввод (Inputs) ---
  // Можно хранить отдельно, так как их часто смотрят отдельно от колес
  throttle float4
  brake float4
  steer float4
  clutch float4
  handbrake boolean
}