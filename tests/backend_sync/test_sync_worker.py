import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from desktop_client.backend_sync.local_buffer import LocalBuffer
from desktop_client.backend_sync.sync_worker import SyncWorker

@pytest.mark.asyncio
async def test_worker_successful_send():
    buffer = LocalBuffer()
    for i in range(1, 11):
        buffer.put_nowait(i)
        
    worker = SyncWorker(buffer, "http://dummy", batch_size=10, interval_sec=0.01)
    worker._is_running = True
    
    # Мокаем _send_batch, чтобы вернуть True и остановить цикл
    async def mock_send_batch(batch):
        worker._is_running = False
        return True
        
    worker._send_batch = AsyncMock(side_effect=mock_send_batch)
    
    # Убираем реальный sleep для скорости тестов
    with patch("asyncio.sleep", AsyncMock()):
        await worker._run_loop()
        
    assert buffer.size == 0
    worker._send_batch.assert_called_once()

@pytest.mark.asyncio
async def test_worker_failed_send_rolls_back():
    buffer = LocalBuffer()
    for i in range(1, 11):
        buffer.put_nowait(i)
        
    worker = SyncWorker(buffer, "http://dummy", batch_size=10, interval_sec=0.01)
    worker._is_running = True
    
    # Мокаем _send_batch, чтобы вернуть False и остановить цикл
    async def mock_send_batch(batch):
        worker._is_running = False
        return False
        
    worker._send_batch = AsyncMock(side_effect=mock_send_batch)
    
    with patch("asyncio.sleep", AsyncMock()):
        await worker._run_loop()
        
    # Размер должен остаться 10 из-за отката (rollback)
    assert buffer.size == 10
    worker._send_batch.assert_called_once()

@pytest.mark.asyncio
async def test_worker_stop_force_flushes():
    buffer = LocalBuffer()
    for i in range(1, 6):
        buffer.put_nowait(i)
        
    worker = SyncWorker(buffer, "http://dummy", batch_size=10, interval_sec=0.01)
    worker._send_batch = AsyncMock(return_value=True)
    
    await worker.stop()
    
    worker._send_batch.assert_called_once()
    # Буфер должен быть пуст после успешной отправки остатков
    assert buffer.size == 0
