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

  // --- Группа 2: Колеса (Массивы по 4 элемента) ---
  // Порядок всегда: [FL, FR, RL, RR]
  // Это сокращает кол-во колонок в 4 раза!
  
  susp_travel float4[] [note: "Ход подвески (нормализован 0-1)"]
  wheel_slip float4[]  [note: "Пробуксовка"]
  wheel_speed float4[] [note: "Скорость вращения каждого колеса"]
  tire_temp integer[]  [note: "Температура (целые числа)"]
  
  // --- Группа 3: Ввод (Inputs) ---
  // Можно хранить отдельно, так как их часто смотрят отдельно от колес
  throttle float4
  brake float4
  steer float4
  clutch float4
  handbrake boolean
}