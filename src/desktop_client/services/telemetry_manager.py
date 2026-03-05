import dataclasses
from typing import Any, List

import structlog

from desktop_client.backend_sync.local_buffer import LocalBuffer
from desktop_client.backend_sync.sync_worker import SyncWorker
from desktop_client.forza_core.application.core_facade import RealCoreFacade

logger = structlog.get_logger(__name__)

class TelemetryManager:
    """
    Менеджер сессии (Session Manager).
    Единая точка управления стартом и остановкой гонки для UI.
    Связывает ядро Форзы, локальный буфер и HTTP-воркер в единый конвейер.
    """

    def __init__(self, api_url: str):
        self.api_url = api_url
        
        # 1. Создаем локальный буфер
        self.local_buffer = LocalBuffer()
        
        # 2. Создаем HTTP-воркер, который будет вычитывать данные из буфера.
        #    Сериализатор определяется здесь — TelemetryManager знает о типах доменного
        #    слоя; SyncWorker остаётся независимым от них (SRP).
        self.sync_worker = SyncWorker(
            buffer=self.local_buffer,
            api_url=self.api_url,
            serializer=_serialize_batch,
        )
        
        # 3. Создаем фасад ядра Forza, передав ему буфер в качестве утиного out_queue
        # LocalBuffer реализует интерфейс IOutQueue (в частности, метод put_nowait()), 
        # который ожидается слоем forza_core (RealCoreFacade/IngestionService).
        self.core_facade = RealCoreFacade(out_queue=self.local_buffer)

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


def _serialize_batch(batch: List[Any]) -> List[dict]:
    """Convert a batch of TelemetryPacket dataclasses to JSON-serialisable dicts.

    Defined at module level (not inside SyncWorker) so that the worker stays
    ignorant of domain types — only TelemetryManager, which assembles the
    pipeline, needs to know the concrete packet format.
    """
    return [dataclasses.asdict(packet) for packet in batch]

