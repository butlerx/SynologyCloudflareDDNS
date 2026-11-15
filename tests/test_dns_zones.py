"""Tests for finding the zone a hostname belongs to."""

import pytest

from synology_cloudflare_ddns.dns import zone_candidates


@pytest.mark.parametrize(
    ("dns_name", "candidates"),
    [
        ("example.com", ["example.com"]),
        ("www.example.com", ["www.example.com", "example.com"]),
        ("a.b.example.com", ["a.b.example.com", "b.example.com", "example.com"]),
        ("nas.example.co.uk", ["nas.example.co.uk", "example.co.uk", "co.uk"]),
        ("www.example.com.", ["www.example.com", "example.com"]),
    ],
)
def test_zone_candidates(dns_name: str, candidates: list) -> None:
    assert list(zone_candidates(dns_name)) == candidates
