from __future__ import annotations

from typing import TYPE_CHECKING, Any

from iplooker.api_key_manager import APIKeyManager
from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address


class IPDataLookup(IPLookupSource):
    """Perform IP lookups using the ipdata.co service."""

    SOURCE_NAME = "ipdata.co"
    API_URL = "https://api.ipdata.co/{ip}"

    @classmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address using ipdata.co."""
        ip_obj = cls._validate_ip(ip)
        if not ip_obj:
            return None

        api_key = APIKeyManager.get_key(cls.SOURCE_NAME)
        if not api_key:
            return None

        params = {"api-key": api_key}
        url = cls.API_URL.format(ip=ip)

        data = cls._make_request(url, params=params)
        if not data:
            return None

        if "message" in data and "error" in data:
            print(f"{cls.SOURCE_NAME} error: {data.get('message')}")
            return None

        return cls._parse_response(data, ip_obj)

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult:
        """Parse the ipdata.co response into a LookupResult."""
        result = IPLookupResult(
            ip=ip_obj,
            source=cls.SOURCE_NAME,
            country=data.get("country_name"),
            region=data.get("region"),
            city=data.get("city"),
        )

        # Extract ASN information for ISP/org
        if asn_data := data.get("asn"):
            result.isp = asn_data.get("domain")
            result.org = asn_data.get("name")

        # Security information
        if threat := data.get("threat", {}):
            result.is_tor = threat.get("is_tor")
            result.is_proxy = threat.get("is_proxy")
            result.is_datacenter = threat.get("is_datacenter")
            result.is_anonymous = threat.get("is_anonymous")

        return result
