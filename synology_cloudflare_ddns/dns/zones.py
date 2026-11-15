"""Look up Cloudflare zones."""

from __future__ import annotations

from typing import TYPE_CHECKING

from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

if TYPE_CHECKING:
    from CloudFlare import CloudFlare

logger = get_logger("dns.zones")


def get_zones(cf: CloudFlare, zone_name: str) -> list[dict[str, str]]:
    """Look up the zones matching a zone name."""
    try:
        return cf.zones.get(params={"name": zone_name})
    except CloudFlareAPIError as err:
        # TRY400: API failures are expected here, so log the error without a traceback.
        logger.error("bad authentication", method="zones.get", zone_name=zone_name, err=err)  # noqa: TRY400
    except Exception as err:  # noqa: BLE001 - any failure talking to the API is logged and treated as no zones
        logger.error("api call failed", method="zones.get", zone_name=zone_name, err=err)  # noqa: TRY400
    return []


def parse_zone_name(dns_name: str) -> str:
    """Return the zone name that a DNS name belongs to."""
    _, zone_name = dns_name.split(".", 1)
    if "." not in zone_name:
        return dns_name
    return zone_name
