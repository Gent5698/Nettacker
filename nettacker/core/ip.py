import json

import netaddr
import requests


def generate_ip_range(ip_range):
    """
    IP range to CIDR and IPNetwork type

    Args:
        ip_range: IP range

    Returns:
        an array with CIDRs
    """
    if "/" in ip_range:
        return [ip.format() for ip in [cidr for cidr in netaddr.IPNetwork(ip_range)]]
    else:
        ips = []
        for generator_ip_range in [
            cidr.iter_hosts() for cidr in netaddr.iprange_to_cidrs(*ip_range.rsplit("-"))
        ]:
            for ip in generator_ip_range:
                ips.append(ip.format())
        return ips


def get_ip_range(ip):
    """
    get IPv4 range from RIPE online database

    Args:
        ip: IP address

    Returns:
        IP Range
    """
    try:
        return generate_ip_range(
            json.loads(
                requests.get(
                    f"https://rest.db.ripe.net/search.json?query-string={ip}&flags=no-filtering"
                ).content
            )["objects"]["object"][0]["primary-key"]["attribute"][0]["value"].replace(" ", "")
        )
    except Exception:
        return [ip]


def is_single_ipv4(ip):
    """
    to check a value if its IPv4 address

    Args:
        ip: the value to check if its IPv4

    Returns:
         True if it's IPv4 otherwise False
    """
    return netaddr.valid_ipv4(str(ip))


def is_ipv4_range(ip_range):
    try:
        return (
            "/" in ip_range
            and "." in ip_range
            and "-" not in ip_range
            and bool(netaddr.IPNetwork(ip_range))
        )
    except Exception:
        return False


def is_ipv4_cidr(ip_range):
    try:
        return (
            "/" not in ip_range
            and "." in ip_range
            and "-" in ip_range
            and bool(netaddr.iprange_to_cidrs(*ip_range.split("-")))
        )
    except Exception:
        return False


def is_single_ipv6(ip):
    """
    to check a value if its IPv6 address

    Args:
        ip: the value to check if its IPv6

    Returns:
         True if it's IPv6 otherwise False
    """
    return netaddr.valid_ipv6(ip)


def is_ipv6_range(ip_range):
    try:
        return (
            "/" not in ip_range
            and ":" in ip_range
            and "-" in ip_range
            and bool(netaddr.iprange_to_cidrs(*ip_range.split("-")))
        )
    except Exception:
        return False


def is_ipv6_cidr(ip_range):
    try:
        return (
            "/" in ip_range
            and ":" in ip_range
            and "-" not in ip_range
            and bool(netaddr.IPNetwork(ip_range))
        )
    except Exception:
        return False
