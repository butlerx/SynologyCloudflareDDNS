"""cli args"""

from argparse import ArgumentParser


def get_args():
    """get command line args"""
    parser = ArgumentParser(
        description="automatically update cloudflare dns on ip change"
    )
    parser.add_argument("email", type=str, help="This is not used.")
    parser.add_argument("api_key", type=str, help="cloudflare api key")
    parser.add_argument("hostname", type=str, help="domain name to update")
    parser.add_argument(
        "ip_address", type=str, help="current IP address to set domain to"
    )
    parser.add_argument("--log-level", default="ERROR", help="logging level")
    return parser.parse_args()
