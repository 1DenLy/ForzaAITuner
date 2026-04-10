from typing import Protocol


class ISourceValidator(Protocol):
    """
    Infrastructure interface for IP-based source validation.

    Delegates IP allow/deny logic away from UdpListener.
    Implementations: WhitelistSourceValidator, SubnetSourceValidator, etc.

    Security note: UDP does not guarantee authenticity of source_ip.
    IP spoofing is possible in LAN environments. This guard is a first-line
    filter, not a cryptographic one.
    """

    def is_allowed(self, ip: str) -> bool:
        """
        Returns True if the IP address is permitted to send packets.
        Drops are handled by UdpListener (metrics only, no DLQ).
        """
        ...
