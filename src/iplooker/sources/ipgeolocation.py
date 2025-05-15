from __future__ import annotations

from typing import TYPE_CHECKING, Any

from iplooker.api_key_manager import APIKeyManager
from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address


class IPGeoLocationLookup(IPLookupSource):
    """Perform IP lookups using the ipgeolocation.io service."""

    SOURCE_NAME = "ipgeolocation.io"
    API_URL = "https://api.ipgeolocation.io/v2/ipgeo"

    @classmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address using ipgeolocation.io."""
        ip_obj = cls._validate_ip(ip)
        if not ip_obj:
            return None

        api_key = APIKeyManager.get_key(cls.SOURCE_NAME)
        if not api_key:
            return None

        params = {"apiKey": api_key, "ip": ip}

        data = cls._make_request(cls.API_URL, params=params)
        if not data:
            return None

        # Check for error response
        if "message" in data and "status" in data and data.get("status") != 200:
            print(f"{cls.SOURCE_NAME} error: {data.get('message')}")
            return None

        return cls._parse_response(data, ip_obj)

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult:
        """Parse the ipgeolocation.io response into a LookupResult."""
        result = IPLookupResult(ip=ip_obj, source=cls.SOURCE_NAME)

        # Extract location information
        if location := data.get("location", {}):
            result.country = location.get("country_name")
            result.region = location.get("state_prov")
            result.city = location.get("city")

        return result
