class WhitelistSourceValidator:
    """
    ISourceValidator implementation using an IP whitelist.

    Allows only explicitly registered IP addresses to send packets.
    All other sources are silently dropped (metrics only, no DLQ).

    Security note: Does NOT protect against IP-spoofing in LAN environments.
    Rate limiting (IRateLimiter) is applied even for whitelisted IPs to limit
    damage from spoofed-source attacks.

    Usage (Composition Root):
        validator = WhitelistSourceValidator(allowed_ips={"192.168.1.10"})
    """

    def __init__(self, allowed_ips: set[str]) -> None:
        self._allowed_ips = frozenset(allowed_ips)

    def is_allowed(self, ip: str) -> bool:
        """Returns True if the IP is in the whitelist."""
        return ip in self._allowed_ips
