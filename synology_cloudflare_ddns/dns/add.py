"""Create DNS records."""

from CloudFlare import CloudFlare
from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

logger = get_logger("dns.add")


def add_record(cf: CloudFlare, zone_id: str, dns_name: str, ip_address_type: str, ip_address: str) -> None:
    """Create a DNS record for a name that has no existing record to update."""
    dns_record = {"name": dns_name, "type": ip_address_type, "content": ip_address}
    try:
        cf.zones.dns_records.post(zone_id, data=dns_record)
    except CloudFlareAPIError as err:
        # TRY400: API failures are expected here, so log the error without a traceback.
        logger.error(  # noqa: TRY400
            "failed to create dns entry",
            method="zones.dns_records.post",
            **dns_record,
            err=err,
        )
    logger.info("DNS record added", **dns_record)
