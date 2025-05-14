from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipaddress import IPv4Address


@dataclass
class IPLookupResult:
    """Dataclass to hold the result of an IP lookup from a single source."""

    ip: IPv4Address
    source: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    isp: str | None = None
    org: str | None = None
