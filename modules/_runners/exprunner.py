"""
Experimental Runner Functions
"""
import expmodutil
import salt.client


def id_to_fqdn_original(minion_id):
    """
    Append configured or default domain to minion_id

    Get config options from the master config with salt.runners.config
    """
    # Get first config values from salt-master config
    expmod_config = __salt__["config.get"]("expmod", {})
    domain = expmod_config.get("domain", "example.com")

    # Return minion_id with domain appended
    return expmodutil.id_to_fqdn(minion_id, domain)


def id_to_fqdn(minion_id):
    """
    Append configured or default domain to minion_id

    Get config options from the minion with salt.modules.config
    """
    local = salt.client.LocalClient()
    expmod_config = local.cmd(minion_id, "config.get", ["expmod"], default={}).get(minion_id, {})
    domain = expmod_config.get("domain", "example.com")

    # Return minion_id with domain appended
    return expmodutil.id_to_fqdn(minion_id, domain)
