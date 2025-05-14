from __future__ import annotations

from typing import TYPE_CHECKING, Any

from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address


class IPAPILookup(IPLookupSource):
    """Perform IP lookups using the IP-API.com service."""

    SOURCE_NAME = "ip-api.com"
    API_URL = "http://ip-api.com/json/{ip}"

    @classmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address using IP-API."""
        ip_obj = cls._validate_ip(ip)
        if not ip_obj:
            return None

        url = cls.API_URL.format(ip=ip)
        data = cls._make_request(url)
        if not data:
            return None

        return cls._parse_response(data, ip_obj)

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult | None:
        """Parse the IP-API response into a LookupResult."""
        if data.get("status") != "success":
            print(f"IP-API error: {data.get('message', 'Unknown error')}")
            return None

        return IPLookupResult(
            ip=ip_obj,
            source=cls.SOURCE_NAME,
            country=data.get("country"),
            region=data.get("regionName"),
            city=data.get("city"),
            isp=data.get("isp"),
            org=data.get("org"),
        )
