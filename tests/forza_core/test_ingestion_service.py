import pytest
import asyncio
from unittest.mock import MagicMock
from forza_core.application.ingestion_service import IngestionService
from forza_core.domain.models import TelemetryPacket

@pytest.mark.asyncio
async def test_ingestion_service_routes_valid_packet():
    # 1. Подготовка очередей и моков
    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()
    
    # Мокаем парсер, чтобы он всегда возвращал валидный пакет
    mock_parser = MagicMock()
    mock_packet = MagicMock(spec=TelemetryPacket)
    mock_packet.is_race_on = 1  # Чтобы пакет прошел фильтр в сервисе
    mock_parser.parse.return_value = mock_packet
    
    service = IngestionService(queue=in_queue, out_queue=out_queue, parser=mock_parser)
    
    # 2. Запускаем сервис в фоне
    task = asyncio.create_task(service.run())
    
    # 3. Кидаем фейковые сырые байты во входную очередь (как будто от UDP)
    fake_addr = ("127.0.0.1", 5300)
    await in_queue.put((b'raw_bytes', fake_addr))
    
    # 4. Ждем, пока пакет появится в выходной очереди
    result_packet = await asyncio.wait_for(out_queue.get(), timeout=1.0)
    
    # 5. Проверки
    assert result_packet is mock_packet
    mock_parser.parse.assert_called_once_with(b'raw_bytes')
    
    # 6. Убираем за собой (останавливаем сервис)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass