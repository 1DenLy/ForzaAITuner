import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.forza_core.application.ingestion_service import IngestionService
from src.forza_core.domain.models import TelemetryPacket
from src.forza_core.config import IngestionConfig

# Helper to create a dummy packet
def create_packet(is_race_on=1):
    # Minimal fields needed to pass instantiation
    # using a dict optimization or just dumb values
    return TelemetryPacket(
        is_race_on=is_race_on,
        timestamp_ms=0, engine_max_rpm=0, engine_idle_rpm=0, current_engine_rpm=0,
        acceleration_x=0, acceleration_y=0, acceleration_z=0,
        velocity_x=0, velocity_y=0, velocity_z=0,
        angular_velocity_x=0, angular_velocity_y=0, angular_velocity_z=0,
        yaw=0, pitch=0, roll=0,
        normalized_suspension_travel_fl=0, normalized_suspension_travel_fr=0,
        normalized_suspension_travel_rl=0, normalized_suspension_travel_rr=0,
        tire_slip_ratio_fl=0, tire_slip_ratio_fr=0, tire_slip_ratio_rl=0, tire_slip_ratio_rr=0,
        wheel_rotation_speed_fl=0, wheel_rotation_speed_fr=0,
        wheel_rotation_speed_rl=0, wheel_rotation_speed_rr=0,
        wheel_on_rumble_strip_fl=0, wheel_on_rumble_strip_fr=0,
        wheel_on_rumble_strip_rl=0, wheel_on_rumble_strip_rr=0,
        wheel_in_puddle_depth_fl=0, wheel_in_puddle_depth_fr=0,
        wheel_in_puddle_depth_rl=0, wheel_in_puddle_depth_rr=0,
        surface_rumble_fl=0, surface_rumble_fr=0, surface_rumble_rl=0, surface_rumble_rr=0,
        tire_slip_angle_fl=0, tire_slip_angle_fr=0, tire_slip_angle_rl=0, tire_slip_angle_rr=0,
        tire_combined_slip_fl=0, tire_combined_slip_fr=0,
        tire_combined_slip_rl=0, tire_combined_slip_rr=0,
        suspension_travel_meters_fl=0, suspension_travel_meters_fr=0,
        suspension_travel_meters_rl=0, suspension_travel_meters_rr=0,
        car_ordinal=0, car_class=0, car_performance_index=0, drivetrain_type=0, num_cylinders=0,
        position_x=0, position_y=0, position_z=0,
        speed=0, power=0, torque=0,
        tire_temp_fl=0, tire_temp_fr=0, tire_temp_rl=0, tire_temp_rr=0,
        boost=0, fuel=0, distance_traveled=0,
        best_lap=0, last_lap=0, current_lap=0, current_race_time=0,
        lap_number=0, race_position=0,
        accel=0, brake=0, clutch=0, handbrake=0, gear=0, steer=0,
        normalized_driving_line=0, normalized_ai_brake_difference=0
    )

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.save_batch = AsyncMock()
    return repo

@pytest.fixture
def mock_config():
    # Use small buffer for testing
    conf = IngestionConfig()
    conf.buffer_size = 5
    conf.flush_interval_sec = 0.5
    return conf

@pytest.fixture
def mock_queue():
    return asyncio.Queue()

@pytest.fixture
def service(mock_repo, mock_config, mock_queue):
    return IngestionService(mock_repo, mock_config, mock_queue)

@pytest.mark.asyncio
async def test_buffer_flush_on_full(service, mock_repo, mock_queue, mock_config):
    """Test that buffer flushes when it reaches buffer_size."""
    # Mock PacketParser to return our dummy packet
    dummy_packet = create_packet(is_race_on=1)
    
    with patch("src.forza_core.application.ingestion_service.PacketParser") as MockParser:
        MockParser.parse.return_value = dummy_packet
        
        # Start service in background
        task = asyncio.create_task(service.run())
        
        # Send packets to fill buffer (size 5)
        for _ in range(mock_config.buffer_size):
            await mock_queue.put((b"dummy_data", ("127.0.0.1", 1234)))
            
        # Give a little time for processing
        await asyncio.sleep(0.1)
        
        # At this point, save_batch should have been called once
        mock_repo.save_batch.assert_called_once()
        args, _ = mock_repo.save_batch.call_args
        assert len(args[0]) == mock_config.buffer_size
        
        # Clean up
        service._running = False
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

@pytest.mark.asyncio
async def test_buffer_flush_on_timer(service, mock_repo, mock_queue, mock_config):
    """Test that buffer flushes after interval even if not full."""
    dummy_packet = create_packet(is_race_on=1)
    
    with patch("src.forza_core.application.ingestion_service.PacketParser") as MockParser:
        MockParser.parse.return_value = dummy_packet
        
        task = asyncio.create_task(service.run())
        
        # Send 1 packet (less than buffer size 5)
        await mock_queue.put((b"dummy_data", ("127.0.0.1", 1234)))
        
        # Verify not flushed yet
        await asyncio.sleep(0.1)
        mock_repo.save_batch.assert_not_called()
        
        # Wait for interval (0.5s) + buffer
        await asyncio.sleep(0.6)
        
        # Should be flushed now
        mock_repo.save_batch.assert_called_once()
        args, _ = mock_repo.save_batch.call_args
        assert len(args[0]) == 1
        
        service._running = False
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

@pytest.mark.asyncio
async def test_graceful_shutdown_waits(service, mock_repo):
    """Test that flush() waits for active save tasks."""
    
    # Create a slow save_batch
    async def slow_save(packets):
        await asyncio.sleep(0.2)
    
    mock_repo.save_batch.side_effect = slow_save
    
    # Manually add something to buffer
    service._buffer.append(create_packet())
    
    # Trigger flush (starts background task)
    start_time = asyncio.get_running_loop().time()
    await service.flush() # This calls internal _flush then waits
    end_time = asyncio.get_running_loop().time()
    
    duration = end_time - start_time
    # It should have waited at least 0.2s
    assert duration >= 0.2
    
    mock_repo.save_batch.assert_called_once()
    assert len(service._active_saves) == 0

