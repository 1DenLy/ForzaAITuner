import pytest
from desktop_client.infrastructure.parsers.packet_parser import PacketParser

@pytest.fixture
def parser():
    return PacketParser()

def test_parse_invalid_length(parser):
    # Пакет неверной длины (например, 10 байт вместо 311/324)
    bad_data = b'\x00' * 10
    result = parser.parse(bad_data)
    assert result is None, "Парсер должен возвращать None для пакетов неверного размера"

def test_parse_valid_sled_format(parser):
    # Создаем фейковый пакет правильного размера (324 байта)
    # Заполняем нулями, чтобы struct.unpack не упал, а просто вернул нули
    fake_data = b'\x00' * 324
    result = parser.parse(fake_data)
    
    assert result is not None
    assert result.is_race_on == 0
    assert result.speed_mps == 0.0

def test_parse_valid_dash_format(parser):
    # То же самое, но для формата Dash (311 байт)
    fake_data = b'\x00' * 311
    result = parser.parse(fake_data)
    assert result is not None