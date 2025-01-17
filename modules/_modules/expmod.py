"""
Experimental Execution Module
"""

import expmodutil

__virtualname__ = "expmod"


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
    # using salt.modules.config
    expmod_config = __salt__["config.get"]("expmod", {})
    domain = expmod_config.get("domain", "example.com")

    # Return minion_id with domain appended
    return expmodutil.id_to_fqdn(minion_id, domain)
