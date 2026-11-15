"""lib for getting dns records"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

if TYPE_CHECKING:
    from CloudFlare import CloudFlare

logger = get_logger("dns.get")


def get_dns_records(
    cf: CloudFlare, zone_id: str, dns_name: str, ip_address_type: str
) -> list[dict[str, Any]] | None:
    """Get the records of one type for one hostname. Returns None if the API call failed."""
    try:
        return cf.zones.dns_records.get(
            zone_id, params={"match": "all", "name": dns_name, "type": ip_address_type}
        )
    except CloudFlareAPIError as err:
        logger.error(
            "api call failed",
            extra={
                "err": err,
                "method": "zones.dns_records.get",
                "dns_name": dns_name,
                "ip_address_type": ip_address_type,
                "zone_id": zone_id,
            },
        )
        return None
