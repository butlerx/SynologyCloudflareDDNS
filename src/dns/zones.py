"""zone functions"""
from typing import List

from structlog import get_logger

from CloudFlare import CloudFlare
from CloudFlare.exceptions import CloudFlareAPIError


def get_zones(cf: CloudFlare, zone_name: str) -> List[dict]:
    """ grab the zone identifier"""
    logger = get_logger("get_zones")
    try:
        return cf.zones.get(params={"name": zone_name})
    except CloudFlareAPIError as err:
        logger.error(
            "bad authentication", method="zones.get", zone_name=zone_name, err=err
        )
        return []
    except Exception as err:
        logger.error(
            "api call failed", method="zones.get", zone_name=zone_name, err=err
        )
        return []
