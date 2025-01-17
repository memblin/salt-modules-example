"""
Experimental Execution Module
"""

import logging


__virtualname__ = "expmod"
log = logging.getLogger(__name__)


def __virtual__():
    return __virtualname__


def id_to_fqdn(minion_id=None):
    """
    Append configured or default domain to minion_id
    """
    if not minion_id:
        minion_id = __grains__["id"]

    # Get first config values found from:
    #  minion config > grains > pillar
    expmod_config = __salt__["config.get"]("expmod", {})
    domain = expmod_config.get("domain", "example.com")

    # Retrun minio_id with domain appended
    return minion_id + "." + domain
