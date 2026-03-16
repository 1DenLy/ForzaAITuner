# Standard library imports
import asyncio
import logging
import signal
import sys

# Third-party imports
import qasync
from pydantic import ValidationError
from PySide6.QtWidgets import QApplication

# Application configuration
from config import BASE_DIR, get_settings

# Domain & Infrastructure layer
from desktop_client.domain.tuning import TuningSetup
from desktop_client.infrastructure.local_preset_repository import LocalPresetRepository
from desktop_client.validation import PathValidator, FileSizeValidator, PacketValidator, TelemetrySanityValidator
from desktop_client.infrastructure.local_config_repository import LocalConfigRepository

# Application layer & Services
from desktop_client.application.config_data_manager import ConfigDataManager
from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.application.services.telemetry_manager import TelemetryManager
from desktop_client.infrastructure.sync.local_buffer import LocalBuffer
from desktop_client.infrastructure.sync.sync_worker import SyncWorker
from desktop_client.application.services.core_facade import RealCoreFacade
from desktop_client.application.mappers.telemetry_mapper import serialize_batch
from desktop_client.infrastructure.network.udp_transport import UdpListener

# Presentation layer
from desktop_client.presentation.helpers.dialog_service import DialogService
from desktop_client.domain.models import ConfigState, SessionState, MainState
from desktop_client.presentation.viewmodels.config_viewmodel import ConfigViewModel
from desktop_client.presentation.viewmodels.main_vm import MainViewModel
from desktop_client.presentation.views.main_window import MainWindow

# State Management
from desktop_client.application.state.main_flow import MainFlowManager
from desktop_client.application.state.session_flow import SessionFlowManager
from desktop_client.application.state.config_flow import ConfigFlowManager
from desktop_client.application.state.library_flow import LibraryFlowManager
from desktop_client.presentation.viewmodels.config_library_viewmodel import ConfigLibraryViewModel

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Sets up the environment for the application."""
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

def log_secure_validation_error(e: ValidationError, logger_instance: logging.Logger):
    """
    Safely logs Pydantic ValidationErrors without leaking sensitive inputs
    (like passwords or internal absolute paths).
    """
    error_list = e.errors(include_url=False, include_input=False)
    
    formatted_errors = []
    for error in error_list:
        loc = " -> ".join([str(p) for p in error.get("loc", ())])
        msg = error.get("msg", "Unknown error")
        formatted_errors.append(f"Field [{loc}]: {msg}")
        
    error_message = "\n".join(formatted_errors)
    logger_instance.critical(f"Failed to validate configuration.\nDetails:\n{error_message}")


from desktop_client.infrastructure.network.asyncio_runner import AsyncioThreadRunner
from desktop_client.infrastructure.parsers.packet_parser import PacketParser
from desktop_client.application.services.ingestion_service import IngestionService
from desktop_client.domain.interface.interfaces import IOutQueue, IPacketParser

def bootstrap_dependencies(settings):
    """Initializes and returns the core application dependencies."""
    logger.info("Initializing services...")
    from desktop_client.infrastructure.signal_bus import SignalBus
    signal_bus = SignalBus()
    
    # 1. Telemetry Pipeline Dependencies
    local_buffer = LocalBuffer()
    sync_worker = SyncWorker(
        buffer=local_buffer,
        api_url=settings.network.api_url,
        serializer=serialize_batch,
        event_bus=signal_bus,
    )
    
    async_runner = AsyncioThreadRunner()
    packet_parser = PacketParser()
    
    sanity_validator = TelemetrySanityValidator()
    
    def ingestion_factory(udp_q: asyncio.Queue, out_q: IOutQueue, parser: IPacketParser) -> IngestionService:
        return IngestionService(queue=udp_q, out_queue=out_q, parser=parser, sanity_validator=sanity_validator)

    packet_validator = PacketValidator()
    
    def udp_protocol_factory(q: asyncio.Queue) -> UdpListener:
        return UdpListener(q, packet_validator)

    core_facade = RealCoreFacade(
        out_queue=local_buffer,
        async_runner=async_runner,
        packet_parser=packet_parser,
        ingestion_factory=ingestion_factory,
        udp_protocol_factory=udp_protocol_factory,
        host=settings.network.host,
        port=settings.network.port
    )
    
    # Assembly
    telemetry_manager = TelemetryManager(
        buffer=local_buffer,
        sync_worker=sync_worker,
        core_facade=core_facade
    )

    logger.info("Initializing ViewModels...")

    main_flow = MainFlowManager()
    session_flow = SessionFlowManager()
    config_flow = ConfigFlowManager()
    library_flow = LibraryFlowManager()

    main_vm = MainViewModel(
        telemetry_manager=telemetry_manager, 
        session_flow=session_flow, 
        main_flow=main_flow
    )
    
    app_config_validator = ConfigValidatorService(TuningSetup)
    local_config_repo = LocalConfigRepository(BASE_DIR)
    
    path_validator = PathValidator(BASE_DIR)
    size_validator = FileSizeValidator()
    local_preset_repo = LocalPresetRepository(path_validator, size_validator)
    app_config_data_manager = ConfigDataManager(local_config_repo)
    app_config_data_manager.initialize(TuningSetup.model_validate)
    
    config_vm = ConfigViewModel(
        app_config_validator, 
        app_config_data_manager, 
        local_preset_repo,
        config_flow
    )

    library_vm = ConfigLibraryViewModel(
        config_repo=local_config_repo,
        local_state=app_config_data_manager, # Using app_config_data_manager as local_state contextually
        library_flow=library_flow
    )
    
    return main_vm, config_vm, library_vm, app_config_data_manager, signal_bus


def setup_state_bridges(main_vm: MainViewModel, app_config_data_manager: ConfigDataManager, signal_bus=None):
    """Sets up the reactive bridges between view models and state managers."""
    # ── Config-state bridge ──────────────────────────────────────────────────
    # Unlock 'Start Session' when valid config is available
    def _on_config_updated(_new_config) -> None:
        if _new_config:
            main_vm.main_flow.set_state(MainState.VALID_CONFIG)
            main_vm.main_flow.set_state(MainState.READY_TO_START)
        else:
            main_vm.main_flow.set_state(MainState.MONITORING_CONFIG)

    app_config_data_manager.subscribe(_on_config_updated)

    # Promote state if config already exists on disk
    if app_config_data_manager.get_config() is not None:
        main_vm.main_flow.set_state(MainState.VALID_CONFIG)
        main_vm.main_flow.set_state(MainState.READY_TO_START)
        logger.info("Cold-start: persisted config found — main_flow set to READY_TO_START.")

    # ── Session-lock bridge ──────────────────────────────────────────────────
    # Prevent config changes mid-race (while session is active)
    _PIPELINE_ACTIVE = frozenset({
        SessionState.STARTING,
        SessionState.RECORDING,
        SessionState.FLUSHING,
    })

    def _on_session_state_changed(state: SessionState) -> None:
        app_config_data_manager.is_recording_session = state in _PIPELINE_ACTIVE

    main_vm.session_flow.state_changed.connect(_on_session_state_changed)

    # ── Backend-Error bridge ──────────────────────────────────────────────────
    def _on_backend_error(event):
        main_vm.error_occurred.emit(f"Backend Sync Error: {event.message}")
        
    if signal_bus:
        signal_bus.backend_error_occurred.connect(_on_backend_error)


async def async_main():
    """Async GUI entry point."""
    # 1. Load Configuration
    try:
        settings = get_settings()
        logger.info(f"Configuration loaded successfully. Environment: {settings.env}")
        # Security Note: sensitive parameters like settings.network.api_url 
        # are intentionally omitted from startup logs to prevent leakage.
    except ValidationError as e:
        log_secure_validation_error(e, logger)
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Failed to load configuration (System Error): {e}")
        sys.exit(1)


    # 2. Initialize Dependencies (Services & ViewModels)
    main_vm, config_vm, library_vm, app_config_data_manager, signal_bus = bootstrap_dependencies(settings)

    # 3. Setup reactive bridges
    setup_state_bridges(main_vm, app_config_data_manager, signal_bus)

    # 4. Initialize Dialog Services and View (Window)
    logger.info("Initializing View...")
    dialog_service = DialogService(main_vm, config_vm)
    window = MainWindow(main_vm, dialog_service)
    dialog_service.set_main_window(window)
    window.show()

    # 5. Keep coroutine alive until Qt application quits
    future = asyncio.get_event_loop().create_future()

    def on_app_quit():
        if not future.done():
            future.set_result(None)

    QApplication.instance().aboutToQuit.connect(on_app_quit)
    await future


def main():
    """Synchronous entry point."""
    setup_environment()

    app = QApplication(sys.argv)
    app.setApplicationName("ForzaAITuner")
    app.setApplicationVersion("1.0.0")

    # Bridge Qt and asyncio event loops
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda *_: app.quit())

    try:
        with loop:
            loop.run_until_complete(async_main())
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()