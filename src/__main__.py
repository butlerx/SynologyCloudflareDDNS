#!/usr/bin/env python3
"""
This code is largely from
https://raw.githubusercontent.com/cloudflare/python-cloudflare/master/examples/example_update_dynamic_dns.py
"""

from structlog import get_logger

from CloudFlare import CloudFlare

from .dns import add_record, get_dns_records, get_zones, update_record
from .utils import get_args, setup_logger


def main(email: str, api_key: str, dns_name: str, ip_address: str):
    """main function"""
    logger = get_logger("main")
    _, zone_name = dns_name.split(".", 1)
    if "." not in zone_name:
        zone_name = dns_name
    ip_address_type = "AAAA" if ":" in ip_address else "A"

    cloudflare = CloudFlare(email=email, token=api_key)

    zones = get_zones(cloudflare, zone_name)

    if not zones:
        logger.info("no zone specified", zones=zones, zone_name=zone_name)
        return 0

    if len(zones) != 1:
        logger.error(
            "api call returned multiple items",
            zone_name=zone_name,
            num_zones=len(zones),
            method="zones.get",
        )
        return 2

    dns_records = get_dns_records(cloudflare, zones[0]["id"], dns_name, ip_address_type)
    if not dns_records:
        return 2

    zone_id: str = zones[0]["id"]
    dns_name: str = zones[0]["name"]
    updated = False
    unchanged = True

    # update the record - unless it's already correct
    for dns_record in dns_records:
        old_ip_address = dns_record["content"]
        old_ip_address_type = dns_record["type"]

        if ip_address_type != old_ip_address_type:
            continue

        if ip_address == old_ip_address:
            updated = True
            continue
        update_record(
            cloudflare, zone_id, dns_record["id"], dns_name, ip_address_type, ip_address
        )
        unchanged = False
        updated = True

    if updated:
        if unchanged:
            logger.info(
                "No Change required",
                name=dns_name,
                type=ip_address_type,
                address=ip_address,
            )
        return 0

    add_record(cloudflare, zone_id, dns_name, ip_address_type, ip_address)
    return 0


if __name__ == "__main__":
    setup_logger()
    ARGS = get_args()
    exit(main(ARGS.email, ARGS.api_key, ARGS.hostname, ARGS.ip_address))
