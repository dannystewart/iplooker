from __future__ import annotations

from typing import TYPE_CHECKING, Any

from iplooker.api_key_manager import APIKeyManager
from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address


class IPLocateLookup(IPLookupSource):
    """Perform IP lookups using the iplocate.io service."""

    SOURCE_NAME = "iplocate.io"
    API_URL = "https://iplocate.io/api/lookup/{ip}"

    @classmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address using iplocate.io."""
        ip_obj = cls._validate_ip(ip)
        if not ip_obj:
            return None

        api_key = APIKeyManager.get_key(cls.SOURCE_NAME)
        if not api_key:
            return None

        params = {"apikey": api_key}
        url = cls.API_URL.format(ip=ip)

        data = cls._make_request(url, params=params)
        if not data:
            return None

        # Check for error response
        if "error" in data:
            print(f"{cls.SOURCE_NAME} error: {data.get('message', 'Unknown error')}")
            return None

        return cls._parse_response(data, ip_obj)

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult:
        """Parse the iplocate.io response into a LookupResult."""
        result = IPLookupResult(
            ip=ip_obj,
            source=cls.SOURCE_NAME,
            country=data.get("country"),
            region=data.get("subdivision"),
            city=data.get("city"),
        )

        # Extract organization information
        if (company := data.get("company", {})) and isinstance(company, dict):
            result.org = company.get("name")

        # Extract ASN information for ISP
        if (asn := data.get("asn", {})) and isinstance(asn, dict):
            result.isp = asn.get("name") or asn.get("domain")
            # If we don't have org info from company, use ASN data
            if not result.org:
                result.org = asn.get("name")

        return result
