"""
Tests for modules/_modules/exprunner.py
"""

import pytest

from conftest import id_to_fqdn_test_data

import salt.runners.config as config
from modules._utils import expmodutil
from modules._runners import exprunner


@pytest.fixture()
def configure_loader_modules():
    """
    Prepare modules for execution during testing
    """
    return {
        # exprunner needs dunders and access to config.get
        # and expmod.id_to_fqdn
        exprunner: {
            "__salt__": {
                "config.get": config.get,
                "expmodutil.id_to_fqdn": expmodutil.id_to_fqdn,
            },
        },
        # config needs dunders
        config: {},
    }


@pytest.mark.parametrize("minion_id, domain, expected_fqdn", id_to_fqdn_test_data)
def test_id_to_fqdn_via_config(minion_id, domain, expected_fqdn):
    """
    Verify expected output from id_to_fqdn when configured via config options
    """
    if domain:
        # Merge fixture content into grains and config opts
        # when a domain is prsent in test data
        config.__opts__.update({"expmod": {"domain": domain}})

    # Verify the returned fqdn matches the expected fqdn
    assert exprunner.id_to_fqdn(minion_id) == expected_fqdn

