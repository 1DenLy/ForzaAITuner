from typing import Protocol


class IRateLimiter(Protocol):
    """
    Infrastructure interface for per-IP rate limiting.

    Delegates rate control logic away from UdpListener.
    Implementations: TokenBucketRateLimiter, FixedWindowRateLimiter, etc.

    Rate limiting is applied EVEN for valid IPs — this limits damage
    from IP-spoofing attacks (spoofed whitelist IP still gets throttled).
    """

    def allow(self, ip: str) -> bool:
        """
        Returns True if the packet from this IP is within the allowed rate.
        Returns False if the rate limit is exceeded.
        Drops are handled by UdpListener (metrics only, no DLQ).
        """
        ...
