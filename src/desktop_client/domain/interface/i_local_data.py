from typing import Protocol, Optional
from models.car_config import CarConfig

class ILocalData(Protocol):
    """Интерфейс для работы с текущим активным состоянием (локальный кэш)."""
    
    def get_active_config(self) -> Optional[CarConfig]:
        """Загружает последнюю активную настройку при старте программы."""
        ...
        
    def set_active_config(self, config: CarConfig) -> None:
        """Делает переданную настройку активной (нажатие кнопки Change)."""
        ...
        
    def clear_active_config(self) -> None:
        """Сбрасывает активную настройку (например, если ее удалили из Библиотеки)."""
        ...
        
    def is_session_used(self) -> bool:
        """Читает поле 'Used' из твоего JSON, чтобы понять, идет ли заезд."""
        ...