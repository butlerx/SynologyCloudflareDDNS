"""Look up DNS records."""

from __future__ import annotations

from typing import TYPE_CHECKING

from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

if TYPE_CHECKING:
    from CloudFlare import CloudFlare

logger = get_logger("dns.get")


def get_dns_records(cf: CloudFlare, zone_id: str, ip_address_type: str) -> list[dict[str, str]]:
    """Fetch the DNS records of one address type for a zone."""
    try:
        return cf.zones.dns_records.get(zone_id, params={"match": "all", "type": ip_address_type})
    except CloudFlareAPIError as err:
        # TRY400: API failures are expected here, so log the error without a traceback.
        logger.error(  # noqa: TRY400
            "api call failed",
            err=err,
            method="zones.dns_records",
            ip_address_type=ip_address_type,
            zone_id=zone_id,
        )
        return []
