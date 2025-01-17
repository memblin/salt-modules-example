"""
Tests for modules/_modules/expmod.py
"""

import logging
import pytest

from conftest import id_to_fqdn_test_data

import salt.modules.config as config
from modules._modules import expmod


log = logging.getLogger(__name__)


id_to_fqdn_test_data = [
    # Defaulted domain
    ("app-1", None, "app-1.example.com"),
    # Expected domain set that matches the default
    ("app-2", "example.com", "app-2.example.com"),
    # Expected domain set that does not match the default
    ("app-3", "example.net", "app-3.example.net"),
]


@pytest.fixture()
def configure_loader_modules():
    """
    Prepare modules for execution during testing

      expmod needs access to config.get

      config needs access to __opts__ and __grains__

    """
    return {
        # expmod needs dunders and access to config.get
        expmod: {
            "__salt__": {
                "config.get": config.get,
            },
        },
        # config needs dunders
        config: {},
    }


@pytest.mark.parametrize("minion_id, domain, expected_fqdn", id_to_fqdn_test_data)
def test_id_to_fqdn_via_config(minion_id, domain, expected_fqdn):
    """
    Verify expected output from id_to_fqdn when configured via grains
    """
    if domain:
        # Merge fixture content into grains and config opts
        # when a domain is prsent in test data
        expmod.__grains__.update({"id": minion_id})
        config.__opts__.update({"expmod": {"domain": domain}})
    else:
        # Merge fixture content into grains but skip config opts
        # when no domain is present in test data
        expmod.__grains__.update({"id": minion_id})

    # Verify the returned fqdn matches the expected fqdn
    assert expmod.id_to_fqdn(minion_id) == expected_fqdn


@pytest.mark.parametrize("minion_id, domain, expected_fqdn", id_to_fqdn_test_data)
def test_id_to_fqdn_via_grains(minion_id, domain, expected_fqdn):
    """
    Verify expected output from id_to_fqdn when configured via grains
    """
    if domain:
        # Merge fixture content into grains when a domain is
        # present in test data
        expmod.__grains__.update({"id": minion_id, "expmod": {"domain": domain}})
    else:
        # Merge fixture content into grains when no domain is
        # present in test data
        expmod.__grains__.update({"id": minion_id})

    # Verify the returned fqdn matches the expected fqdn
    assert expmod.id_to_fqdn(minion_id) == expected_fqdn


@pytest.mark.parametrize("minion_id, domain, expected_fqdn", id_to_fqdn_test_data)
def test_id_to_fqdn_via_pillar(minion_id, domain, expected_fqdn):
    """
    Verify expected output from id_to_fqdn when configured via pillar
    """
    if domain:
        # Merge fixture content into grains and pillar when a domain is
        # present in test data
        expmod.__grains__.update({"id": minion_id})
        expmod.__pillar__.update({"expmod": {"domain": domain}})
    else:
        # Merge fixture content into grains when no domain is
        # present in test data
        expmod.__grains__.update({"id": minion_id})

    # Verify the returned fqdn matches the expected fqdn
    assert expmod.id_to_fqdn(minion_id) == expected_fqdn
