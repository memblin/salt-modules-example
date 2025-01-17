"""
Experimental Runner Functions
"""

import logging

import salt.loader


log = logging.getLogger(__name__)


def id_to_fqdn(minion_id):
    """
    Use the expmod.id_to_fqdn function to convert a minion_id into an fqdn.
    """
    # Load our grains into __grains__ so we can add them to our __opts__
    # making them available to the execution modules we are loading.
    __grains__ = salt.loader.grains(__opts__)
    __opts__["grains"] = __grains__
    mods = salt.loader.minion_mods(__opts__)
    return mods["exprunner.id_to_fqdn"](minion_id)
