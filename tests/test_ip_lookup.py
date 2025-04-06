# type: ignore[reportMissingParamType]

import pytest
from unittest.mock import patch, MagicMock
import json

from iplooker.ip_lookup import IPLookup
from iplooker.ip_sources import IP_SOURCES


class TestIPLookup:
    """Tests for the IPLookup class."""

    @pytest.fixture
    def sample_ip(self):
        """Return a sample IP address for testing."""
        return "8.8.8.8"

    @pytest.fixture
    def mock_response(self):
        """Return a mock response for the IP lookup."""
        return {
            "data": {
                "country": "US",
                "region": "California",
                "city": "Mountain View",
                "isp": "Google LLC",
                "org": "Google"
            }
        }

    @patch("iplooker.ip_lookup.requests.post")
    def test_get_ip_info(self, mock_post, sample_ip, mock_response):
        """Test the get_ip_info method."""
        # Setup mock response
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 200
        mock_response_obj.text = json.dumps(mock_response)
        mock_post.return_value = mock_response_obj

        # Create instance with do_lookup=False to avoid actual API calls
        lookup = IPLookup(sample_ip, do_lookup=False)

        # Test the method
        result = lookup.get_ip_info("some_source")

        # Verify results
        assert result == mock_response
        mock_post.assert_called_once()

    def test_standardize_country(self, sample_ip):
        """Test the standardize_country method."""
        lookup = IPLookup(sample_ip, do_lookup=False)

        # Test various country formats
        assert lookup.standardize_country("US") == "US"
        assert lookup.standardize_country("usa") == "US"
        assert lookup.standardize_country("GB") == "United Kingdom"
        assert lookup.standardize_country("Random") == "Random"

    def test_format_ip_data(self, sample_ip):
        """Test the format_ip_data method."""
        lookup = IPLookup(sample_ip, do_lookup=False)

        result = lookup.format_ip_data(
            source="TestSource",
            country="US",
            region="California",
            city="San Francisco",
            isp="Comcast",
            org="Comcast"
        )

        expected = {
            "source": "TestSource",
            "location": "San Francisco, California, US",
            "ISP_Org": "Comcast"
        }

        assert result == expected


    @patch("iplooker.ip_lookup.requests.get")
    def test_get_external_ip(self, mock_get):
        """Test getting the external IP address."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "1.2.3.4"
        mock_get.return_value = mock_response

        # Test the method
        result = IPLookup.get_external_ip()

        # Verify
        assert result == "1.2.3.4"
        mock_get.assert_called_once_with("https://api.ipify.org", timeout=2)

    def test_standardize_isp_and_org(self, sample_ip):
        """Test the ISP and org standardization."""
        lookup = IPLookup(sample_ip, do_lookup=False)

        # Test various combinations
        assert lookup.standardize_isp_and_org("Comcast", "Comcast") == "Comcast"
        assert lookup.standardize_isp_and_org("comcast business", "Comcast") == "Comcast / Comcast"
        assert lookup.standardize_isp_and_org("", "Some Org") == "Some Org"
        assert lookup.standardize_isp_and_org("Unknown ISP", "") is None

    @patch("iplooker.ip_lookup.IPLookup.process_source")
    @patch("iplooker.ip_lookup.IPLookup.display_results")
    @patch("iplooker.ip_lookup.halo_progress")
    def test_perform_ip_lookup(self, mock_halo, mock_display, mock_process, sample_ip):
        """Test the main lookup workflow."""
        # Setup
        lookup = IPLookup(sample_ip, do_lookup=False)

        # Create a fixed result that process_source will return
        result = {"source": "test-source", "location": "New York, US"}

        # Make process_source always return our test result
        mock_process.return_value = result

        # Mock the context manager
        mock_context = MagicMock()
        mock_halo.return_value.__enter__.return_value = mock_context

        # Execute
        lookup.perform_ip_lookup()

        # Verify that display_results was called with a list containing our result
        expected_results = [result] * len(IP_SOURCES)  # One result for each source
        mock_display.assert_called_once_with(expected_results)
