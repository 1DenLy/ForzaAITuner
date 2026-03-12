import dataclasses
from typing import Any, List

import structlog

from desktop_client.infrastructure.sync.protocols import IBuffer, ISyncWorker
from desktop_client.presentation.interfaces.protocols import ICoreFacade

logger = structlog.get_logger(__name__)

class TelemetryManager:
    """
    Менеджер сессии (Session Manager).
    Единая точка управления стартом и остановкой гонки для UI.
    Связывает ядро Форзы, локальный буфер и HTTP-воркер в единый конвейер.
    """

    def __init__(self, buffer: IBuffer, sync_worker: ISyncWorker, core_facade: ICoreFacade):
        # Dependencies injected from Composition Root
        self.local_buffer = buffer
        self.sync_worker = sync_worker
        self.core_facade = core_facade

    async def start_session(self) -> None:
        """
        Запускает конвейер сбора и отправки телеметрии.
        Сначала стартует воркер, затем ядро начинает писать в буфер.
        """
        logger.info("Starting telemetry session pipeline...")
        # Запускаем асинхронный метод start() у SyncWorker
        await self.sync_worker.start()
        
        # Вызываем обычный (синхронный) метод start_tracking() у RealCoreFacade
        self.core_facade.start_tracking()
        logger.info("Telemetry session pipeline started successfully.")

    async def stop_session(self) -> None:
        """
        Останавливает конвейер.
        Сначала ядро перестает писать данные, затем воркер делает Force Flush.
        """
        logger.info("Stopping telemetry session pipeline...")
        # Вызываем stop_tracking() у RealCoreFacade (чтобы игра перестала писать в буфер)
        self.core_facade.stop_tracking()
        
        # Дожидаемся выполнения метода stop() у SyncWorker (выгребает остатки и отправляет)
        await self.sync_worker.stop()
        logger.info("Telemetry session pipeline stopped successfully.")

