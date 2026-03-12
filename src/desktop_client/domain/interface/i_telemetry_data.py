from typing import Protocol, List

class ITelemetryData(Protocol):
    """Интерфейс для запроса графиков и результатов заездов."""
    
    def get_sessions_history(self) -> List[dict]:
        """Возвращает список всех прошедших заездов пользователя."""
        ...
        
    def get_session_telemetry(self, session_id: int) -> List[dict]:
        """Выгружает массивы данных (скорость, обороты, подвеска) для графиков по конкретному заезду."""
        ...