import time


class TokenBucketRateLimiter:
    """
    IRateLimiter implementation using a simple per-IP fixed-window counter.

    Allows at most `max_per_sec` packets per IP address per second.
    This is a simplified token-bucket: the window resets on each new second.

    Applied even for whitelisted IPs (limits damage from IP-spoofing in LAN).
    Drops are reported via metrics only — no DLQ (DoS protection on I/O logging).

    Usage (Composition Root):
        limiter = TokenBucketRateLimiter(max_per_sec=120)
    """

    def __init__(self, max_per_sec: int) -> None:
        self._max_per_sec = max_per_sec
        # dict[ip -> (count, window_start)]
        self._counters: dict[str, tuple[int, float]] = {}

    def allow(self, ip: str) -> bool:
        """
        Returns True if the packet is within the rate limit.
        Returns False if the rate limit for this IP is exceeded.
        """
        now = time.monotonic()
        count, window_start = self._counters.get(ip, (0, now))

        # New second — reset the window
        if now - window_start >= 1.0:
            count = 0
            window_start = now

        if count >= self._max_per_sec:
            return False

        self._counters[ip] = (count + 1, window_start)
        return True
