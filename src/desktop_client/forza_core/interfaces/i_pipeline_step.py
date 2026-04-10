from typing import Protocol
from ..models.pipeline_context import PipelineContext


class IPipelineStep(Protocol):
    """
    Interface for a single transformation or check in the packet processing pipeline.
    
    Adheres to the Open/Closed Principle: new steps can be added without
    modifying the PipelineManager engine.
    """

    def process(self, context: PipelineContext) -> None:
        """
        Executes the step logic on the context.
        Should set context.is_dropped = True and a drop_reason to abort the pipeline.
        """
        ...
