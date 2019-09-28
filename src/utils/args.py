"""cli args"""

from argparse import ArgumentParser


def get_args():
    """get command line args"""
    parser = ArgumentParser(
        prog="cloudflareDDNS",
        description="automatically update cloudflare dns on ip change",
    )
    parser.add_argument(
        "email", action="store", type=str, help="account login for cloudflare"
    )
    parser.add_argument("api_key", action="store", type=str, help="cloudflare api key")
    parser.add_argument(
        "hostname", action="store", type=str, help="domain name to update"
    )
    parser.add_argument(
        "ip_address",
        action="store",
        type=str,
        help="current IP address to set domain to",
    )
    return parser.parse_args()
