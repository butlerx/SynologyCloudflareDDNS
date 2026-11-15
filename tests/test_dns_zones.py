"""Tests for DNS zone name parsing."""

import pytest

from synology_cloudflare_ddns.dns import parse_zone_name


@pytest.mark.parametrize(
    ("dns_name", "zone"),
    [
        ("example.com", "example.com"),
        ("www.example.com", "example.com"),
    ],
)
def test_parse_zone_name(dns_name: str, zone: str) -> None:
    assert parse_zone_name(dns_name) == zone
