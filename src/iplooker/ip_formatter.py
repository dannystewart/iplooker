from __future__ import annotations

import operator
from collections import Counter
from typing import Any, ClassVar

import pycountry
from polykit.formatters import color

from iplooker.ip_sources import CITY_NAMES, REGION_NAMES, USA_NAMES


class IPFormatter:
    """Format IP results returned by lookups."""

    # Omit these values entirely if they start with "Unknown"
    OMIT_IF_UNKNOWN: ClassVar[set[str]] = {"region", "isp", "org"}

    def __init__(self, ip_address: str):
        self.ip_address: str = ip_address

    def extract_field_data(
        self, data: dict[str, Any], fields: dict[str, str | tuple[str, Any]]
    ) -> dict[str, str]:
        """Extract and format field data from source response."""
        formatted_data = {}
        for key, value in fields.items():
            if isinstance(value, tuple):
                value, _ = value

            # Get the value from the data
            retrieved_value = data.get(value, "")

            # If empty or starts with "Unknown", set it to an empty string for formatting
            if not retrieved_value or retrieved_value.startswith("Unknown"):
                retrieved_value = (
                    "" if key in self.OMIT_IF_UNKNOWN else f"Unknown {key.capitalize()}"
                )

            formatted_data[key] = retrieved_value

        return formatted_data

    def format_ip_data(
        self, source: str, country: str, region: str, city: str, isp: str, org: str
    ) -> dict[str, str]:
        """Standardizes and formats the IP data."""
        country = self.standardize_country(country)
        region, city = self.standardize_region_and_city(region, city)
        isp_org = self.standardize_isp_and_org(isp, org)

        # Build location string based on available data
        location_parts = []
        if city:
            location_parts.append(city)
        if region:
            location_parts.append(region)
        if country:
            location_parts.append(country)

        location = ", ".join(location_parts) if location_parts else "Unknown Location"

        formatted_data = {"source": source, "location": location}
        if isp_org:
            formatted_data["ISP_Org"] = isp_org

        return formatted_data

    def print_consolidated_results(self, results: list[dict[str, str]]) -> None:
        """Print consolidated results with sources that report the same data grouped together."""
        # Count occurrences of each location
        location_count = Counter()
        for result in results:
            location = result["location"]
            isp_org = result.get("ISP_Org", "")
            line = f"{location}" + (f" ({isp_org})" if isp_org else "")
            location_count[line] += 1

        # Sort by count (descending)
        sorted_locations = sorted(location_count.items(), key=operator.itemgetter(1), reverse=True)

        # Print consolidated results
        for line, count in sorted_locations:
            if count > 1:
                print(f"• {color(f'{count} sources:', 'blue')} {line}")
            else:  # Find the source for this unique result
                source = next(
                    r["source"]
                    for r in results
                    if f"{r['location']}"
                    + (f" ({r.get('ISP_Org', '')})" if r.get("ISP_Org") else "")
                    == line
                )
                print(f"• {color(source + ':', 'blue')} {line}")

    def standardize_country(self, country: str) -> str:
        """Standardize the country name."""
        if len(country) == 2 and country.upper() != "US":
            try:
                country_obj = pycountry.countries.get(alpha_2=country.upper())
                return country_obj.name if country_obj is not None else country
            except (AttributeError, KeyError):
                return country
        return "US" if country.lower() in USA_NAMES else country

    def standardize_region_and_city(self, region: str, city: str) -> tuple[str, str]:
        """Standardize the region and city names."""
        if region.lower() in REGION_NAMES:
            region = "DC"
        if city.lower() in CITY_NAMES:
            city = "Washington" if "washington" in city.lower() else "New York"
        return region, city

    def standardize_isp_and_org(self, isp: str, org: str) -> str | None:
        """Standardize the ISP and organization names."""
        original_isp = isp
        original_org = org

        if "comcast" in isp.lower():
            isp = "Comcast"
        if "comcast" in org.lower():
            org = "Comcast"

        if isp and isp not in {"Unknown ISP", ""}:
            if org and org not in {"Unknown Org", ""}:
                return isp if original_isp.lower() == original_org.lower() else f"{isp} / {org}"
            return isp
        return org if org and org not in {"Unknown Org", ""} else None
