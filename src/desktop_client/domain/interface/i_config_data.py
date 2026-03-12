from typing import Protocol, List, Optional
from models.car_config import CarConfig # Твоя Pydantic модель

class IConfigData(Protocol):
    """Интерфейс для работы с основной базой данных конфигураций."""
    
    def get_all_configs(self) -> List[CarConfig]:
        """Возвращает список всех сохраненных конфигураций для окна Библиотеки."""
        ...
        
    def get_config_by_id(self, config_id: int) -> Optional[CarConfig]:
        """Получает полные данные одной конфигурации для окна Редактора."""
        ...
        
    def create_config(self, config: CarConfig) -> int:
        """Сохраняет новую конфигурацию в БД. Возвращает её новый ID."""
        ...
        
    def update_config(self, config_id: int, config: CarConfig) -> bool:
        """Обновляет существующую конфигурацию после редактирования."""
        ...
        
    def delete_config(self, config_id: int) -> bool:
        """Удаляет конфигурацию из БД."""
        ...