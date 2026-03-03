"""
State management module for application configuration.
"""
import threading
from typing import Callable, Generic, Optional, TypeVar, Any, Protocol

from desktop_client.application.exceptions import ConfigLockedError

class IConfigRepository(Protocol):
    """Protocol defining the interface for a configuration repository."""
    def load_raw_data(self) -> dict[str, Any]:
        ...
        
    def save_raw_data(self, data: dict[str, Any]) -> None:
        ...

class PydanticModelProtocol(Protocol):
    """Protocol matching Pydantic (or similar) models that can dump their state to a dict."""
    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        ...

TModel = TypeVar("TModel", bound=PydanticModelProtocol)

class ConfigStateManager(Generic[TModel]):
    """
    Manager representing the Single Source of Truth for the application's configuration.
    
    Implements the Observer pattern to notify components of configuration updates.
    Ensures thread safety and prevents updates when a session is being recorded.
    """
    
    def __init__(self, repository: IConfigRepository) -> None:
        """
        Initializes the configuration state manager.
        
        Args:
            repository (IConfigRepository): The repository for persisting configuration data.
        """
        self.repository = repository
        self._current_config: Optional[TModel] = None
        self.is_recording_session: bool = False
        self._subscribers: list[Callable[[TModel], None]] = []
        self._lock = threading.RLock()

    def subscribe(self, callback: Callable[[TModel], None]) -> None:
        """
        Subscribes a callback to configuration updates.
        
        Args:
            callback (Callable[[TModel], None]): The function to call when the configuration changes.
        """
        with self._lock:
            if callback not in self._subscribers:
                self._subscribers.append(callback)

    def get_config(self) -> Optional[TModel]:
        """
        Retrieves the current configuration.
        
        Returns:
            Optional[TModel]: The current configuration state, or None if not set.
        """
        with self._lock:
            return self._current_config

    def update_config(self, new_config: TModel) -> None:
        """
        Updates the current configuration, saves it to the repository, and notifies subscribers.
        
        Args:
            new_config (TModel): The new configuration.
            
        Raises:
            ConfigLockedError: If attempting to update while a session is being recorded.
        """
        with self._lock:
            if self.is_recording_session:
                raise ConfigLockedError("Configuration update rejected: Currently recording a session.")
                
            self._current_config = new_config
            
            # Save to disk while holding the lock to prevent concurrent writes.
            # mode="json" ensures all complex types (datetime, UUID, Decimal) are serialized.
            self.repository.save_raw_data(new_config.model_dump(mode="json"))
            
            # Copy subscribers to avoid holding the lock while executing unknown external code,
            # which could block or cause deadlocks.
            subscribers_snapshot = self._subscribers.copy()
            
        # Notify subscribers outside the lock
        for subscriber in subscribers_snapshot:
            subscriber(new_config)
