import logging
import queue
import struct
import threading
from concurrent.futures import ThreadPoolExecutor, Future

from .interfaces import IPacketDecoderFactory, IPacketParser, IPacketValidator
from .models import RawPacket, ValidationResult
from ..domain.interface.i_out_queue import IOutQueue

logger = logging.getLogger(__name__)

# Sentinel value to signal worker shutdown
_STOP_SENTINEL = None


class PipelineManager:
    """
    Application Consumer: orchestrates the Decode → Parse → Validate pipeline.

    Receives RawPacket items from UdpListener via enqueue() (wired by ForzaCore).
    Processes them in a ThreadPoolExecutor worker. Pushes valid TelemetryPacket
    items to OutQueue. Routes errors to DLQ (logger) and updates metrics counters.

    SRP: this is the ONLY component that knows the order of pipeline steps.

    Does NOT:
      - Work with the network (UdpListener's job).
      - Manage module lifecycle (ForzaCore's job).
      - Implement business logic (delegated to Decoder / Parser / Validator).

    Dead Letter Queue policy:
      - Unknown packet size → metrics only (drop.unknown_size), no DLQ.
      - Corrupt bytes (struct.error) → DLQ (drop.decode_error) + metrics.
      - Mapping failure → DLQ (drop.parse_error) + metrics.
      - Validation failed → DLQ (drop.validation_failed) + metrics.
    """

    def __init__(
        self,
        decoder_factory: IPacketDecoderFactory,
        parser: IPacketParser,
        validator: IPacketValidator,
        out_queue: IOutQueue,
        num_workers: int = 1,
    ) -> None:
        self._decoder_factory = decoder_factory
        self._parser = parser
        self._validator = validator
        self._out_queue = out_queue
        self._num_workers = num_workers

        self._in_queue: queue.Queue[RawPacket | None] = queue.Queue()
        self._executor: ThreadPoolExecutor | None = None
        self._worker_futures: list[Future] = []

        # Lightweight metrics counters
        self._drops_unknown_size: int = 0
        self._drops_decode_error: int = 0
        self._drops_parse_error: int = 0
        self._drops_validation_failed: int = 0
        self._packets_processed: int = 0

    # ------------------------------------------------------------------ lifecycle

    def start(self) -> None:
        """Initialises the InQueue and starts Worker thread(s)."""
        self._executor = ThreadPoolExecutor(
            max_workers=self._num_workers,
            thread_name_prefix="pipeline-worker",
        )
        for _ in range(self._num_workers):
            future = self._executor.submit(self._worker_loop)
            self._worker_futures.append(future)
        logger.info(
            "PipelineManager: started with %d worker(s).", self._num_workers
        )

    def stop(self) -> None:
        """
        Sends stop sentinels to drain the remaining queue and shut down workers.
        Blocks until all workers have exited.
        """
        # One sentinel per worker
        for _ in range(self._num_workers):
            self._in_queue.put(_STOP_SENTINEL)

        for future in self._worker_futures:
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.error("PipelineManager: worker error during shutdown: %s", exc)

        if self._executor:
            self._executor.shutdown(wait=False)
            self._executor = None

        self._worker_futures.clear()
        logger.info(
            "PipelineManager: stopped. stats=processed=%d "
            "drops(size=%d decode=%d parse=%d validation=%d)",
            self._packets_processed,
            self._drops_unknown_size,
            self._drops_decode_error,
            self._drops_parse_error,
            self._drops_validation_failed,
        )

    def enqueue(self, packet: RawPacket) -> None:
        """
        Called by UdpListener via on_packet callback.
        Places the RawPacket into the InQueue for asynchronous processing.
        """
        self._in_queue.put_nowait(packet)

    # ------------------------------------------------------------------ worker

    def _worker_loop(self) -> None:
        """
        Worker thread main loop. Runs Decode → Parse → Validate for each RawPacket.
        Exits cleanly on sentinel (None) from stop().
        """
        while True:
            raw_packet = self._in_queue.get()

            # Shutdown sentinel
            if raw_packet is _STOP_SENTINEL:
                self._in_queue.task_done()
                break

            self._process(raw_packet)
            self._in_queue.task_done()

    def _process(self, raw_packet: RawPacket) -> None:
        data = raw_packet.data

        # ④ Decode — find the right decoder by packet size
        decoder = self._decoder_factory.get_decoder(len(data))
        if decoder is None:
            self._drops_unknown_size += 1
            logger.debug(
                "PipelineManager: drop.unknown_size size=%d", len(data)
            )
            return

        try:
            raw_telemetry = decoder.decode(data, raw_packet.received_at)
        except struct.error as exc:
            self._drops_decode_error += 1
            self._log_dlq(
                reason="DECODE_ERROR",
                payload=data,
                detail=str(exc),
            )
            return
        except Exception as exc:
            self._drops_decode_error += 1
            self._log_dlq(
                reason="DECODE_ERROR",
                payload=data,
                detail=f"unexpected: {exc}",
            )
            return


        # ⑤ Parse — RawTelemetry → TelemetryPacket
        try:
            packet = self._parser.parse(raw_telemetry)
        except (struct.error, TypeError) as exc:
            self._drops_parse_error += 1
            self._log_dlq(
                reason="PARSE_ERROR",
                payload=raw_telemetry,
                detail=str(exc),
            )
            return
        except Exception as exc:
            self._drops_parse_error += 1
            self._log_dlq(
                reason="PARSE_ERROR",
                payload=raw_telemetry,
                detail=f"unexpected: {exc}",
            )
            return

        # ⑥ Validate — full Chain of Responsibility
        result: ValidationResult = self._validator.validate(packet)
        if not result.is_valid:
            self._drops_validation_failed += 1
            self._log_dlq(
                reason="VALIDATION_FAILED",
                payload=packet,
                detail=result.reason or "unknown",
            )
            return

        # ✅ Happy path — push to OutQueue
        self._out_queue.put_nowait(packet)
        self._packets_processed += 1

    @staticmethod
    def _log_dlq(reason: str, payload: object, detail: str) -> None:
        """
        Dead Letter Queue: logs the rejected payload for debugging.
        On first implementation this is a structured log warning.
        Can be replaced with a file/queue DLQ writer via interface injection.
        """
        logger.warning(
            "PipelineManager: DLQ reason=%s detail=%s payload_type=%s",
            reason, detail, type(payload).__name__,
        )
