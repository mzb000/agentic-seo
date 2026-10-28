"""SSRF Prevention and Network Safety Layer for MZ SEO Agent."""

import ipaddress
import socket
from urllib.parse import urlparse
from typing import Tuple


BLOCKED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),      # Loopback
    ipaddress.ip_network("10.0.0.0/8"),       # Private class A
    ipaddress.ip_network("172.16.0.0/12"),    # Private class B
    ipaddress.ip_network("192.168.0.0/16"),   # Private class C
    ipaddress.ip_network("169.254.0.0/16"),   # Link-local / AWS metadata
    ipaddress.ip_network("0.0.0.0/8"),        # Current network
    ipaddress.ip_network("224.0.0.0/4"),      # Multicast
    ipaddress.ip_network("240.0.0.0/4"),      # Reserved
    ipaddress.ip_network("::1/128"),          # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),         # IPv6 unique local
    ipaddress.ip_network("fe80::/10"),        # IPv6 link-local
]


def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validates a URL to prevent SSRF and DNS-rebinding attacks.
    Ensures URL uses http/https and does not resolve to private or internal addresses.
    """
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string."

    parsed = urlparse(url.strip())
    if parsed.scheme.lower() not in ("http", "https"):
        return False, f"Unsupported scheme '{parsed.scheme}'. Only HTTP and HTTPS are permitted."

    hostname = parsed.hostname
    if not hostname:
        return False, "URL missing valid hostname."

    # Prevent localhost explicitly
    if hostname.lower() in ("localhost", "localhost.localdomain", "broadcasthost"):
        return False, "Direct access to localhost is blocked."

    try:
        # Resolve IP addresses for the hostname
        addr_info = socket.getaddrinfo(hostname, None)
        for family, _, _, _, sockaddr in addr_info:
            ip_str = sockaddr[0]
            ip_obj = ipaddress.ip_address(ip_str)

            for blocked_net in BLOCKED_NETWORKS:
                if ip_obj in blocked_net:
                    return False, f"Security Violation: Target resolves to blocked network address {ip_str}."
    except socket.gaierror as e:
        return False, f"DNS resolution failed for hostname '{hostname}': {str(e)}"
    except Exception as e:
        return False, f"URL validation error: {str(e)}"

    return True, "URL is safe."
