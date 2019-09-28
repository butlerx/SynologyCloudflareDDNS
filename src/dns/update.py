"""update records"""
from structlog import get_logger

from CloudFlare import CloudFlare
from CloudFlare.exceptions import CloudFlareAPIError


def update_record(
    cf: CloudFlare,
    zone_id: str,
    dns_record_id: str,
    dns_name: str,
    ip_address_type: str,
    ip_address: str,
):
    """Yes, we need to update this record - we know it's the same address type"""
    logger = get_logger("update_record")

    dns_record = {
        "name": dns_name,
        "type": ip_address_type,
        "content": ip_address,
        "proxied": True,
    }
    try:
        cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record)
    except CloudFlareAPIError as err:
        logger.error(
            "failed to update api",
            **dns_record,
            err=err,
            zone_id=zone_id,
            dns_record_id=dns_record_id,
            method="zones.dns_records.put",
        )
    logger.info("DNS record updated", **dns_record)
