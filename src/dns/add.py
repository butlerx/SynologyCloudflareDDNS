"""add records"""
from structlog import get_logger

from CloudFlare import CloudFlare
from CloudFlare.exceptions import CloudFlareAPIError


def add_record(
    cf: CloudFlare, zone_id: str, dns_name: str, ip_address_type: str, ip_address: str
):
    """ no exsiting dns record to update - so create dns record"""
    logger = get_logger("add_record")
    dns_record = {"name": dns_name, "type": ip_address_type, "content": ip_address}
    try:
        cf.zones.dns_records.post(zone_id, data=dns_record)
    except CloudFlareAPIError as err:
        logger.error(
            "failed to create dns entry",
            method="zones.dns_records.post",
            **dns_record,
            err=err,
        )
    logger.info("DNS record added", **dns_record)
