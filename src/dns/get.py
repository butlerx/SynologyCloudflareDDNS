"""lib for getting dns records"""
from typing import List

from structlog import get_logger

from CloudFlare import CloudFlare
from CloudFlare.exceptions import CloudFlareAPIError


def get_dns_records(
    cf: CloudFlare, zone_id: str, dns_name: str, ip_address_type: str
) -> List[str]:
    """get dns record"""
    logger = get_logger("dns_update")
    try:
        return cf.zones.dns_records.get(
            zone_id, params={"name": dns_name, "match": "all", "type": ip_address_type}
        )
    except CloudFlareAPIError as err:
        logger.error(
            "api call failed",
            dns_name=dns_name,
            err=err,
            method="zones.dns_records",
            ip_address_type=ip_address_type,
            zone_id=zone_id,
        )
        return []
