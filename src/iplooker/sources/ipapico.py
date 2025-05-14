from __future__ import annotations

from typing import TYPE_CHECKING, Any

from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address


class IPAPICoLookup(IPLookupSource):
    """Perform IP lookups using the ipapi.co service."""

    SOURCE_NAME = "ipapi.co"
    API_URL = "https://ipapi.co/{ip}/json/"

    @classmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address using ipapi.co."""
        ip_obj = cls._validate_ip(ip)
        if not ip_obj:
            return None

        url = cls.API_URL.format(ip=ip)
        data = cls._make_request(url)
        if not data:
            return None

        if "error" in data:
            print(f"{cls.SOURCE_NAME} error: {data.get('reason', 'Unknown error')}")
            return None

        return cls._parse_response(data, ip_obj)

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult:
        """Parse the ipapi.co response into a LookupResult."""
        return IPLookupResult(
            ip=ip_obj,
            source=cls.SOURCE_NAME,
            country=data.get("country_name"),
            region=data.get("region"),
            city=data.get("city"),
            isp=None,  # ipapi.co doesn't provide ISP information
            org=data.get("org"),
        )
