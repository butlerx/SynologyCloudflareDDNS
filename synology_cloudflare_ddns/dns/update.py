"""Update DNS records."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

if TYPE_CHECKING:
    from CloudFlare import CloudFlare

logger = get_logger("dns.update")


def update_record(cf: CloudFlare, zone_id: str, existing: dict[str, Any], ip_address: str) -> bool:
    """
    Point an existing record at a new address. Returns True on success.

    Proxy and TTL settings are carried over from the existing record so an
    address change never flips a record between proxied and DNS-only.
    """
    dns_record = {
        "name": existing["name"],
        "type": existing["type"],
        "content": ip_address,
        "proxied": existing.get("proxied", False),
        "ttl": existing.get("ttl", 1),
    }
    log_fields = {
        "dns_name": existing["name"],
        "type": existing["type"],
        "content": ip_address,
        "proxied": dns_record["proxied"],
        "zone_id": zone_id,
        "dns_record_id": existing["id"],
    }
    try:
        cf.zones.dns_records.put(zone_id, existing["id"], data=dns_record)
    except CloudFlareAPIError as err:
        # TRY400: API failures are expected here, so log the error without a traceback.
        logger.error(  # noqa: TRY400
            "failed to update dns record",
            extra={**log_fields, "method": "zones.dns_records.put", "err": err},
        )
        return False
    logger.info("DNS record updated", extra=log_fields)
    return True
