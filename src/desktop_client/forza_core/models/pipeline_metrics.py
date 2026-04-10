from dataclasses import dataclass

@dataclass
class PipelineMetrics:
    """
    Accumulator for pipeline performance and error metrics.
    Passed through the PipelineContext to be updated by steps.
    """
    packets_processed: int = 0
    drops_unknown_size: int = 0
    drops_decode_error: int = 0
    drops_parse_error: int = 0
    drops_validation_failed: int = 0
    drops_queue_full: int = 0

    def total_drops(self) -> int:
        return (
            self.drops_unknown_size +
            self.drops_decode_error +
            self.drops_parse_error +
            self.drops_validation_failed +
            self.drops_queue_full
        )
