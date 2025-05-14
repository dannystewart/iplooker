from __future__ import annotations

from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import TYPE_CHECKING, Any, ClassVar

import requests
from polykit.formatters import print_color

if TYPE_CHECKING:
    from iplooker.lookup_result import IPLookupResult


class IPLookupSource(ABC):
    """Abstract base class for IP lookup sources."""

    # Class variables that should be overridden by subclasses
    SOURCE_NAME: ClassVar[str]
    API_URL: ClassVar[str]
    TIMEOUT: ClassVar[int] = 5

    @classmethod
    @abstractmethod
    def lookup(cls, ip: str) -> IPLookupResult | None:
        """Look up information about an IP address.

        Args:
            ip: The IP address to look up.

        Returns:
            A LookupResult object with the lookup results, or None if the lookup failed.
        """
        msg = "Subclasses must implement this method"
        raise NotImplementedError(msg)

    @classmethod
    def _make_request(
        cls,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | None:
        """Make an HTTP request and return the JSON response.

        Args:
            url: The URL to request.
            params: Query parameters to include in the request.
            headers: HTTP headers to include in the request.

        Returns:
            The parsed JSON response as a dict, or None if the request failed.
        """
        try:
            response = requests.get(url, params=params, headers=headers, timeout=cls.TIMEOUT)

            if response.status_code == 429:
                print_color(
                    f" {cls.SOURCE_NAME} rate limit exceeded. Please try again later.", "yellow"
                )
                return None

            if response.status_code == 200:
                return response.json()

            print(f"{cls.SOURCE_NAME} API error: {response.status_code} - {response.text[:100]}")
            return None

        except requests.RequestException as e:
            print(f"Request error during {cls.SOURCE_NAME} lookup: {e}")
            return None
        except ValueError as e:
            print(f"JSON decode error during {cls.SOURCE_NAME} lookup: {e}")
            return None

    @classmethod
    def _parse_response(cls, data: dict[str, Any], ip_obj: IPv4Address) -> IPLookupResult | None:
        """Parse the response into a LookupResult."""
        msg = "Subclasses must implement this method"
        raise NotImplementedError(msg)

    @classmethod
    def _validate_ip(cls, ip: str) -> IPv4Address | None:
        """Validate and convert an IP string to an IPv4Address object.

        Args:
            ip: The IP address string to validate.

        Returns:
            An IPv4Address object, or None if the IP is invalid.
        """
        try:
            return IPv4Address(ip)
        except ValueError:
            print(f"Invalid IP address: {ip}")
            return None
