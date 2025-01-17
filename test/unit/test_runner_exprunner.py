"""
Tests for modules/_modules/exprunner.py
"""

import logging
import pytest

from conftest import id_to_fqdn_test_data


import salt.modules.config as config
from modules._modules import expmod
from modules._runners import exprunner

log = logging.getLogger(__name__)


@pytest.fixture
def cachedir(tmp_path):
    return tmp_path / "cache"


@pytest.fixture()
def configure_loader_modules():
    """
    Prepare modules for execution during testing

      exprunner needs access to config.get

      config needs access to __opts__ and __grains__

    """
    return {
        # exprunner needs dunders and access to config.get
        # and expmod.id_to_fqdn
        exprunner: {
            "__opts__": {"cachedir": str(cachedir)},
            "__salt__": {
                "config.get": config.get,
                "expmod.id_to_fqdn": expmod.id_to_fqdn,
            },
        },
        # config needs dunders
        config: {},
    }


# @pytest.mark.parametrize("minion_id, domain, expected_fqdn", id_to_fqdn_test_data)
# def test_id_to_fqdn_via_config(minion_id, domain, expected_fqdn):
#     """
#     Verify expected output from id_to_fqdn when configured via grains
#     """
#     if domain:
#         # Merge fixture content into grains and config opts
#         # when a domain is prsent in test data
#         exprunner.__grains__.update({"id": minion_id})
#         config.__opts__.update({"exprunner": {"domain": domain}})
#     else:
#         # Merge fixture content into grains but skip config opts
#         # when no domain is present in test data
#         exprunner.__grains__.update({"id": minion_id})

#     # Verify the returned fqdn matches the expected fqdn
#     assert exprunner.id_to_fqdn(minion_id) == expected_fqdn


@pytest.mark.parametrize("minion_id, domain, expected_fqdn", id_to_fqdn_test_data)
def test_id_to_fqdn_via_grains(minion_id, domain, expected_fqdn):
    """
    Verify expected output from id_to_fqdn when configured via grains
    """
    if domain:
        # Merge fixture content into grains when a domain is
        # present in test data
        exprunner.__grains__.update({"id": minion_id, "exprunner": {"domain": domain}})
    else:
        # Merge fixture content into grains when no domain is
        # present in test data
        exprunner.__grains__.update({"id": minion_id})

    # Verify the returned fqdn matches the expected fqdn
    assert exprunner.id_to_fqdn(minion_id) == expected_fqdn


# @pytest.mark.parametrize("minion_id, domain, expected_fqdn", id_to_fqdn_test_data)
# def test_id_to_fqdn_via_pillar(minion_id, domain, expected_fqdn):
#     """
#     Verify expected output from id_to_fqdn when configured via pillar
#     """
#     if domain:
#         # Merge fixture content into grains and pillar when a domain is
#         # present in test data
#         exprunner.__grains__.update({"id": minion_id})
#         exprunner.__pillar__.update({"exprunner": {"domain": domain}})
#     else:
#         # Merge fixture content into grains when no domain is
#         # present in test data
#         exprunner.__grains__.update({"id": minion_id})

#     # Verify the returned fqdn matches the expected fqdn
#     assert exprunner.id_to_fqdn(minion_id) == expected_fqdn
