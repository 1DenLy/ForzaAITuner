from PySide6.QtCore import QObject, Signal
from desktop_client.domain.events import BackendErrorEvent

class SignalBus(QObject):
    """
    Decoupled event dispatcher. 
    Injected via DI to avoid Global State.
    Supports Thread Hopping automatically via PySide6 Signals.
    """
    backend_error_occurred = Signal(BackendErrorEvent)
    # Add only cross-module global events here to avoid "God Object" anti-pattern.
