import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call

# We use patch or just mock the attributes after instantiation
from desktop_client.application.services.telemetry_manager import TelemetryManager

@pytest.fixture
def manager():
    # DIP makes testing easier - we just inject the mocks
    buffer_mock = MagicMock()
    
    worker_mock = MagicMock()
    worker_mock.start = AsyncMock()
    worker_mock.stop = AsyncMock()
    
    facade_mock = MagicMock()
    facade_mock.start_tracking = MagicMock()
    facade_mock.stop_tracking = MagicMock()
    
    m = TelemetryManager(
        buffer=buffer_mock, 
        sync_worker=worker_mock, 
        core_facade=facade_mock
    )
    return m
@pytest.mark.asyncio
async def test_start_session(manager):
    # Check the order: start worker, then start tracking
    parent = MagicMock()
    parent.attach_mock(manager.sync_worker.start, "worker_start")
    parent.attach_mock(manager.core_facade.start_tracking, "facade_start")

    await manager.start_session()
    
    manager.sync_worker.start.assert_awaited_once()
    manager.core_facade.start_tracking.assert_called_once()
    
    parent.assert_has_calls([
        call.worker_start(),
        call.facade_start()
    ])

@pytest.mark.asyncio
async def test_stop_session(manager):
    # To precisely test that stop_tracking was called BEFORE stop finishes,
    # we can use side_effect on the async mock or check order with a parent mock.
    
    parent = MagicMock()
    parent.attach_mock(manager.core_facade.stop_tracking, "facade_stop")
    parent.attach_mock(manager.sync_worker.stop, "worker_stop")
    
    await manager.stop_session()
    
    manager.core_facade.stop_tracking.assert_called_once()
    manager.sync_worker.stop.assert_awaited_once()
    
    parent.assert_has_calls([
        call.facade_stop(),
        call.worker_stop()
    ])
