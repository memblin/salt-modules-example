"""
Experimental Utility Module
"""

__virtualname__ = "expmodutil"


def __virtual__():
    return __virtualname__


def id_to_fqdn(minion_id, domain):
    """
    Append supplied domain to supplied minion_id
    """
    # Retrun minio_id with domain appended
    return minion_id + "." + domain
