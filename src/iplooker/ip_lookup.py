"""Does an IP lookup using multiple sources.

This script is designed to do an IP lookup using multiple sources. It can be used to get
more information about an IP address, including the country, region, city, ISP, and
organization. It collates the information and combines sources that say the same thing.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, ClassVar

import requests
from polykit.cli import PolyArgs, halo_progress, handle_interrupt
from polykit.formatters import color, print_color

from iplooker.ip_formatter import IPFormatter
from iplooker.ip_sources import IP_SOURCES

if TYPE_CHECKING:
    import argparse


class IPLooker:
    """Perform an IP lookup using multiple sources."""

    TIMEOUT: ClassVar[int] = 2
    MAX_RETRIES: ClassVar[int] = 3

    def __init__(self, ip_address: str, do_lookup: bool = True):
        self.ip_address: str = ip_address
        self.formatter: IPFormatter = IPFormatter(ip_address)
        self.missing_sources: list[str] = []

        if do_lookup:
            self.perform_ip_lookup()

    def perform_ip_lookup(self) -> None:
        """Fetch and print IP data from all sources."""
        results = []

        with halo_progress(
            start_message=f"Getting results for {self.ip_address}",
            end_message="Lookup complete!",
            fail_message=f"Failed to get results for {self.ip_address}",
        ) as spinner:
            for source, config in IP_SOURCES.items():
                if spinner:
                    spinner.text = color(f"Querying {source}...", "cyan")

                result = self.process_source(source, config)
                if result:
                    results.append(result)

        self.display_results(results)

    def process_source(self, source: str, config: dict[str, Any]) -> dict[str, str] | None:
        """Process a single IP data source. Returns formatted data or None if no data."""
        result = self.get_ip_info(source)
        if not result:
            self.missing_sources.append(source)
            return None

        data = result
        for key in config["data_path"]:
            data = data.get(key, {})
        if not data:
            self.missing_sources.append(source)
            return None

        formatted_data = self.formatter.extract_field_data(data, config["fields"])
        return self.formatter.format_ip_data(source, **formatted_data)

    def get_ip_info(self, source: str) -> dict[str, Any] | None:
        """Get the IP information from the source."""
        site_url = "https://www.iplocation.net/"
        url = f"{site_url}get-ipdata"
        payload = {"ip": self.ip_address, "source": source, "ipv": 4}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.post(url, data=payload, headers=headers, timeout=self.TIMEOUT)
                if response.status_code == 200:
                    return json.loads(response.text)
            except requests.exceptions.Timeout:
                print(
                    f"\n{color(f'[{source}]', 'blue')} Timeout ({attempt + 1}/{self.MAX_RETRIES})"
                )
            except requests.exceptions.RequestException as e:
                print(
                    f"\n{color(f'[{source}]', 'blue')} {color(f'Failed to get data: {e}', 'red')}"
                )
                break

        return None

    def display_results(self, results: list[dict[str, str]]) -> None:
        """Display the consolidated results and any sources with no data."""
        if not results:
            print_color(
                "\n⚠️  WARNING: No sources returned results. The service may be blocking automated requests.",
                "yellow",
            )
            print_color(
                "You can try again later or visit iplocation.net in your browser in the meantime.",
                "yellow",
            )
            return

        print_color(f"\n{color(f'Results for {self.ip_address}:', 'cyan')}", "blue")
        self.formatter.print_consolidated_results(results)

        if self.missing_sources:
            print_color(f"\nNo data available from: {', '.join(self.missing_sources)}", "blue")

    @staticmethod
    def get_external_ip() -> str | None:
        """Get the external IP address using ipify.org."""
        try:
            response = requests.get("https://api.ipify.org", timeout=IPLooker.TIMEOUT)
            if response.status_code == 200:
                external_ip = response.text
                print_color(f"Your external IP address is: {external_ip}", "blue")
                return external_ip
        except requests.exceptions.RequestException as e:
            print_color(f"Failed to get external IP: {e}", "red")
        return None


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = PolyArgs(description=__doc__, lines=2)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("ip_address", type=str, nargs="?", help="the IP address to look up")
    group.add_argument("-m", "--me", action="store_true", help="get your external IP address")
    group.add_argument("-l", "--lookup", action="store_true", help="get lookup for your IP address")
    return parser.parse_args()


@handle_interrupt()
def main() -> None:
    """Main function."""
    args = parse_args()
    if args.lookup:
        args.me = True

    if args.me:
        ip_address = IPLooker.get_external_ip()
        if not args.lookup:
            return
    else:
        ip_address = args.ip_address or input("Please enter the IP address to look up: ")

    if not ip_address:
        print_color("No IP address provided.", "red")
        return

    IPLooker(ip_address)


if __name__ == "__main__":
    main()
