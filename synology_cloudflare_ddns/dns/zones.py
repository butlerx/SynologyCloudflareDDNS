"""zone functions"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

if TYPE_CHECKING:
    from CloudFlare import CloudFlare

logger = get_logger("dns.zones")


def get_zones(cf: CloudFlare, zone_name: str) -> list[dict[str, str]] | None:
    """Look up zones by exact name. Returns None if the API call failed."""
    try:
        return cf.zones.get(params={"name": zone_name})
    except CloudFlareAPIError as err:
        logger.error("api call failed", extra={"method": "zones.get", "zone_name": zone_name, "err": err})
    except Exception as err:
        logger.error("api call failed", extra={"method": "zones.get", "zone_name": zone_name, "err": err})
    return None


def zone_candidates(dns_name: str) -> Iterator[str]:
    """
    Yield every possible zone for a hostname, most specific first.

    The zone can't be derived from the hostname alone (sub.example.co.uk vs
    sub.example.com), so callers try each suffix of at least two labels until
    Cloudflare knows one.
    """
    labels = dns_name.rstrip(".").split(".")
    for start in range(max(len(labels) - 1, 1)):
        yield ".".join(labels[start:])


def find_zone(cf: CloudFlare, dns_name: str) -> dict[str, str] | None:
    """Find the Cloudflare zone that contains dns_name, or None."""
    for candidate in zone_candidates(dns_name):
        zones = get_zones(cf, candidate)
        if zones is None:
            return None
        if zones:
            return zones[0]
    logger.error("no zone found for hostname", extra={"dns_name": dns_name})
    return None
