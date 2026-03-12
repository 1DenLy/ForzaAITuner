import dataclasses
import structlog
from typing import Any, List

logger = structlog.get_logger(__name__)

def serialize_batch(batch: List[Any], max_input_size: int = 1000) -> List[dict]:
    """
    Convert a batch of TelemetryPacket dataclasses to JSON-serialisable dicts.
    
    Args:
        batch: List of telemetry dataclasses.
        max_input_size: Maximum allowed batch size to prevent DoS during parsing.
    
    Returns:
        List of dictionaries ready for JSON serialization.
    """
    if len(batch) > max_input_size:
        logger.warning(
            "Telemetry batch size exceeds safety limit",
            batch_size=len(batch),
            max_limit=max_input_size,
        )
        # We process only up to the limit to prevent unbound memory/CPU usage
        batch = batch[:max_input_size]

    # TODO: Implement an allowlist/blocklist for fields when serializing
    # to prevent accidental leakage of sensitive data (e.g., session tokens, player IDs)
    # if such fields are added to TelemetryPacket in the future.
    return [dataclasses.asdict(packet) for packet in batch]
