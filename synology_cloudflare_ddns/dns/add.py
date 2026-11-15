"""add records"""

from CloudFlare import CloudFlare
from CloudFlare.exceptions import CloudFlareAPIError

from synology_cloudflare_ddns.utils.logger import get_logger

logger = get_logger("dns.add")


def add_record(cf: CloudFlare, zone_id: str, dns_name: str, ip_address_type: str, ip_address: str) -> bool:
    """No existing dns record to update, so create one. Returns True on success."""
    dns_record = {"name": dns_name, "type": ip_address_type, "content": ip_address}
    log_fields = {"dns_name": dns_name, "type": ip_address_type, "content": ip_address}
    try:
        cf.zones.dns_records.post(zone_id, data=dns_record)
    except CloudFlareAPIError as err:
        logger.error(
            "failed to create dns entry",
            extra={**log_fields, "method": "zones.dns_records.post", "err": err},
        )
        return False
    logger.info("DNS record added", extra=log_fields)
    return True
