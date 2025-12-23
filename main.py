import socket
import struct

# Настройки сети
UDP_IP = "127.0.0.1"
UDP_PORT = 5300

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Слушаем телеметрию на {UDP_IP}:{UDP_PORT}...")

try:
    while True:
        # Получаем пакет данных (размер пакета Forza Data Out обычно 324 байта)
        data, addr = sock.recvfrom(1024)

        # Формат пакета Forza сложный. Вот основные смещения (offsets) для формата 'Sled':
        # Данные приходят в Little Endian (<), f = float

        # Пример распаковки только части данных:
        # RPM находится по смещению, Скорость по другому.
        # Для Forza Horizon 5 (Data Out) формат 'dash' часто используется.

        # Полная структура сложная, вот пример для получения RPM и скорости:
        # Обычно:
        # ID (s32) - 0
        # ...
        # EngineMaxRpm (f32) - 8
        # ...
        # CurrentEngineRpm (f32) - 16
        # ...
        # Speed (f32) - 256 (примерно, зависит от версии формата)

        # Упрощенный парсинг (нужно сверяться с документацией Forza для точных байтов):
        # Если формат 'Data Out' (Sled), то данные идут сплошным потоком float32.

        # Проверяем длину пакета (324 байта для FH5/FM)
        if len(data) == 324:
            # Распаковываем данные
            # < = little endian, f = float. Всего 81 float значений.
            decoded_data = struct.unpack('<81f', data)

            # Индексы могут отличаться в зависимости от версии игры!
            # Обычно:
            # [4] = Engine Max RPM
            # [37] = Engine Idle RPM
            # [4] = Current Engine RPM
            # [62] = Скорость (м/с)

            rpm = decoded_data[4]
            speed_ms = decoded_data[62]
            speed_kmh = speed_ms * 3.6
            gear = int(decoded_data[80])  # Передача

            print(f"RPM: {rpm:.0f} | Скорость: {speed_kmh:.0f} км/ч | Передача: {gear}")

except KeyboardInterrupt:
    print("Остановка...")