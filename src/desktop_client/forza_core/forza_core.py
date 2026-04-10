import logging

from .interfaces import IUdpListener, IPipelineManager
from ..domain.interface.i_async_runner import IAsyncRunner

logger = logging.getLogger(__name__)


class ForzaCore:
    """
    Module facade implementing IForzaCore.

    Provides the public API: start_tracking() / stop_tracking().
    Manages the module lifecycle and wires Producer ↔ Consumer:
        listener.on_packet = pipeline.enqueue

    ForzaCore does NOT know about:
      - UDP or binary formats (UdpListener's job).
      - Pipeline step order (PipelineManager's job).

    Lifecycle states:
        Stopped → Starting → Listening → Stopping → Stopped
        Starting → Error (port in use / socket error)

    Idempotency:
        - start_tracking() while already running → logs warning, ignored.
        - stop_tracking() while already stopped → logs warning, ignored.

    Assembly (Composition Root / main.py):
        core = ForzaCore(
            async_runner=AsyncioThreadRunner(),
            listener=UdpListener(source_validator, rate_limiter),
            pipeline=PipelineManager(factory, parser, validator, out_queue),
            host="0.0.0.0",
            port=1337,
        )
    """

    def __init__(
        self,
        async_runner: IAsyncRunner,
        listener: IUdpListener,
        pipeline: IPipelineManager,
        host: str,
        port: int,
    ) -> None:
        self._async_runner = async_runner
        self._listener = listener
        self._pipeline = pipeline
        self._host = host
        self._port = port
        self._is_running = False

    # ------------------------------------------------------------------ IForzaCore

    def start_tracking(self) -> None:
        """
        Starts the tracking session.

        Sequence:
          1. pipeline.start()  — init InQueue + workers
          2. listener.on_packet = pipeline.enqueue  — wire callback
          3. async_runner.submit(_start_async())    — bind socket, begin receiving

        Idempotent: a second call while already running logs a warning and returns.
        """
        if self._is_running:
            logger.warning(
                "ForzaCore.start_tracking() called while already running — ignored."
            )
            return

        logger.info(
            "ForzaCore: starting tracking on %s:%d ...", self._host, self._port
        )

        # Step 1: bring up the Consumer before the Producer
        self._pipeline.start()

        # Step 2: wire Producer → Consumer
        self._listener.on_packet = self._pipeline.enqueue

        # Step 3: start the async I/O Producer in the background Event Loop
        self._async_runner.submit(self._start_async())

        self._is_running = True
        logger.info("ForzaCore: tracking started.")

    def stop_tracking(self) -> None:
        """
        Stops the tracking session.

        Sequence:
          1. listener.stop()  — stop receiving new packets
          2. pipeline.stop()  — drain remaining InQueue + stop workers

        Idempotent: a call when already stopped logs a warning and returns.
        """
        if not self._is_running:
            logger.warning(
                "ForzaCore.stop_tracking() called while not running — ignored."
            )
            return

        logger.info("ForzaCore: stopping tracking ...")

        # Step 1: stop the Producer first to prevent new packets entering the queue
        self._listener.stop()

        # Step 2: drain and stop the Consumer
        self._pipeline.stop()

        self._is_running = False
        logger.info("ForzaCore: tracking stopped.")

    def is_tracking(self) -> bool:
        """Returns True if a session is currently active."""
        return self._is_running

    def cleanup(self) -> None:
        """
        Performs graceful shutdown. Stops tracking if active, then stops the runner.
        Called during application exit.
        """
        if self._is_running:
            self.stop_tracking()
        self._async_runner.stop()
        logger.info("ForzaCore: cleanup complete.")

    # ------------------------------------------------------------------ internal async

    async def _start_async(self) -> None:
        """
        Coroutine executed inside the async Event Loop (via IAsyncRunner.submit).
        Binds the UDP socket and initiates datagram reception.
        """
        try:
            await self._listener.start(self._host, self._port)
        except OSError as exc:
            logger.error(
                "ForzaCore: failed to bind %s:%d — %s. "
                "Stopping pipeline to prevent resource leak.",
                self._host, self._port, exc,
            )
            self._pipeline.stop()
            self._is_running = False
