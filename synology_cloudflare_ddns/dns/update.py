"""Update DNS records."""

from __future__ import annotations

from typing import TYPE_CHECKING

from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

if TYPE_CHECKING:
    from CloudFlare import CloudFlare

logger = get_logger("dns.update")


def update_record(
    cf: CloudFlare,
    zone_id: str,
    dns_record: dict[str, str],
    ip_address_type: str,
    ip_address: str,
) -> None:
    """Point an existing DNS record at a new address of the same type."""
    dns_record_id = dns_record["id"]
    payload = {
        "name": dns_record["name"],
        "type": ip_address_type,
        "content": ip_address,
        "proxied": True,
    }
    try:
        cf.zones.dns_records.put(zone_id, dns_record_id, data=payload)
    except CloudFlareAPIError as err:
        # TRY400: API failures are expected here, so log the error without a traceback.
        logger.error(  # noqa: TRY400
            "failed to update api",
            **payload,
            err=err,
            zone_id=zone_id,
            dns_record_id=dns_record_id,
            method="zones.dns_records.put",
        )
    logger.info("DNS record updated", **payload)
