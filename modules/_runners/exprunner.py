"""
Experimental Runner Functions
"""

import expmodutil


def id_to_fqdn(minion_id):
    """
     Append configured or default domain to minion_id
    """
    # Get first config values from salt-master config
    expmod_config = __salt__["config.get"]("expmod", {})
    domain = expmod_config.get("domain", "example.com")

    # Return minion_id with domain appended
    return expmodutil.id_to_fqdn(minion_id, domain)
