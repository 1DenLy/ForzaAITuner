from dataclasses import dataclass, field
from typing import Optional, Any

from .raw_packet import RawPacket
from .raw_telemetry import RawTelemetry
from ...domain.models import TelemetryPacket
from .pipeline_metrics import PipelineMetrics


@dataclass
class PipelineContext:
    """
    Context object carrying the state of a single packet through the pipeline.
    
    Attributes:
        raw_packet: The original input from the network.
        raw_telemetry: Intermediate representation after decoding.
        telemetry_packet: Final domain object after parsing.
        
        is_dropped: Flag indicating if processing should stop.
        drop_reason: Identifier for DLQ and metrics routing.
        drop_detail: Human-readable error message.
        
        metrics: Reference to the shared metrics accumulator.
        metadata: Extensible dictionary for cross-cutting concerns (logging, timing, etc).
    """
    raw_packet: RawPacket
    metrics: PipelineMetrics
    
    raw_telemetry: Optional[RawTelemetry] = None
    telemetry_packet: Optional[TelemetryPacket] = None
    
    is_dropped: bool = False
    drop_reason: Optional[str] = None
    drop_detail: Optional[str] = None
    
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_diagnostic_value(self) -> bool:
        """
        Returns True if the drop reason warrants a Dead Letter Queue entry.
        Unknown packet size usually doesn't, while corrupt bytes or failed logic do.
        """
        return self.drop_reason not in (None, "UNKNOWN_SIZE")
