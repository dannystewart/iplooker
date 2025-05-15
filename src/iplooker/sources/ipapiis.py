from __future__ import annotations

from typing import TYPE_CHECKING, Any

from iplooker.api_key_manager import APIKeyManager
from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address


class IPAPIIsLookup(IPLookupSource):
    """Perform IP lookups using the ipapi.is service."""

    SOURCE_NAME = "ipapi.is"
    API_URL = "https://api.ipapi.is"

    @classmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address using ipapi.is."""
        ip_obj = cls._validate_ip(ip)
        if not ip_obj:
            return None

        api_key = APIKeyManager.get_key(cls.SOURCE_NAME)
        if not api_key:
            return None

        # Set up the query parameters
        params = {"q": ip, "key": api_key}

        data = cls._make_request(cls.API_URL, params=params)
        if not data:
            return None

        # Check for error in response
        if "error" in data:
            print(f"{cls.SOURCE_NAME} error: {data.get('error')}")
            return None

        return cls._parse_response(data, ip_obj)

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult:
        """Parse the ipapi.is response into a LookupResult."""
        result = IPLookupResult(ip=ip_obj, source=cls.SOURCE_NAME)

        # Extract location data
        if location := data.get("location", {}):
            result.country = location.get("country")
            result.region = location.get("state")
            result.city = location.get("city")

        # Extract organization data
        if company := data.get("company", {}):
            result.org = company.get("name")

        # If no org was found in company, try asn
        if not result.org and (asn := data.get("asn", {})):
            result.org = asn.get("org")

        # Extract ISP information (datacenter info can serve as ISP)
        if datacenter := data.get("datacenter", {}):
            result.isp = datacenter.get("datacenter")
        elif not result.isp and (asn := data.get("asn", {})):
            result.isp = asn.get("domain")

        # Security information
        result.is_vpn = data.get("is_vpn")
        result.is_proxy = data.get("is_proxy")
        result.is_tor = data.get("is_tor")
        result.is_datacenter = data.get("is_datacenter")

        if (vpn := data.get("vpn", {})) and vpn.get("is_vpn") and vpn.get("service"):
            result.vpn_service = vpn.get("service")

        return result
