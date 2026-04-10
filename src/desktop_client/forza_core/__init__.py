"""
forza_core — UDP telemetry ingestion module for Forza games.

Public surface:
    IForzaCore      — interface consumed by the Presentation layer.
    ForzaCore       — concrete facade (assembled in main.py Composition Root).

Internal building blocks (for Composition Root):
    UdpListener, PipelineManager,
    PacketDecoderFactory, Fm7Decoder, Fh4Decoder, Fh5Decoder,
    PacketParser,
    TelemetrySanityValidator, NaNCheck, RangeCheck, ConsistencyCheck,
    WhitelistSourceValidator, TokenBucketRateLimiter.

See docs/Forza_Core/Forza_Core_Overview.md for architecture overview.
"""

from .interfaces import IForzaCore
from .forza_core import ForzaCore

__all__ = [
    "IForzaCore",
    "ForzaCore",
]
