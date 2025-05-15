from __future__ import annotations

from typing import TYPE_CHECKING, Any

from iplooker.api_key_manager import APIKeyManager
from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address


class IPRegistryLookup(IPLookupSource):
    """Perform IP lookups using the IPRegistry API."""

    SOURCE_NAME = "ipregistry.co"
    API_URL = "https://api.ipregistry.co/{ip}"

    @classmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address using IPRegistry."""
        ip_obj = cls._validate_ip(ip)
        if not ip_obj:
            return None

        api_key = APIKeyManager.get_key(cls.SOURCE_NAME)
        if not api_key:
            return None

        url = cls.API_URL.format(ip=ip)
        data = cls._make_request(url, params={"key": api_key})
        if not data:
            return None

        return cls._parse_response(data, ip_obj)

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult:
        """Parse the IPRegistry API response into a LookupResult."""
        # Handle the case where the response has a 'results' array
        if "results" in data and isinstance(data["results"], list) and data["results"]:
            data = data["results"][0]

        result = IPLookupResult(ip=ip_obj, source=cls.SOURCE_NAME)

        # Extract location data
        if location := data.get("location", {}):
            if country := location.get("country", {}):
                result.country = country.get("name")

            if region := location.get("region", {}):
                result.region = region.get("name")

            result.city = location.get("city")

        # Extract organization/ISP data
        if connection := data.get("connection", {}):
            result.isp = connection.get("domain")
            result.org = connection.get("organization")
        elif company := data.get("company", {}):
            result.org = company.get("name")

        # Extract security information
        if security := data.get("security", {}):
            result.is_vpn = security.get("is_vpn")
            result.is_proxy = security.get("is_proxy")
            result.is_tor = security.get("is_tor")
            result.is_datacenter = security.get("is_cloud_provider")
            result.is_anonymous = security.get("is_anonymous")

        return result
