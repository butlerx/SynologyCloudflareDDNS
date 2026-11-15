"""
Update Cloudflare DNS records to the current IP address.

This code is largely from
https://raw.githubusercontent.com/cloudflare/python-cloudflare/master/examples/example_update_dynamic_dns.py
"""

import logging
import sys

from CloudFlare import CloudFlare

from synology_cloudflare_ddns.utils.logger import get_logger

from . import dns
from .utils import get_args, setup_logger

logger = get_logger("synology_cloudflare_ddns")


def update_records(api_key: str, dns_name: str, ip_address: str) -> int:
    """Point dns_name at ip_address, creating the record if it doesn't exist."""
    ip_address_type = "AAAA" if ":" in ip_address else "A"
    cloudflare = CloudFlare(token=api_key)

    zone = dns.find_zone(cloudflare, dns_name)
    if zone is None:
        return 2
    zone_id = zone["id"]

    dns_records = dns.get_dns_records(cloudflare, zone_id, dns_name, ip_address_type)
    if dns_records is None:
        return 2

    if not dns_records:
        return 0 if dns.add_record(cloudflare, zone_id, dns_name, ip_address_type, ip_address) else 2

    ok = True
    for dns_record in dns_records:
        if dns_record["content"] == ip_address:
            logger.info(
                "no change required",
                extra={"dns_name": dns_name, "type": ip_address_type, "content": ip_address},
            )
            continue
        ok = dns.update_record(cloudflare, zone_id, dns_record, ip_address) and ok
    return 0 if ok else 2


def main() -> None:
    """Parse the command line and run the DNS update."""
    args = get_args()
    setup_logger(getattr(logging, args.log_level), log_format=args.log_format)
    sys.exit(update_records(args.api_key, args.hostname, args.ip_address))


if __name__ == "__main__":
    main()
