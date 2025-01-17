# Experimental Salt Modules

This repository contains a simplified mock up of some salt code that I'm having trouble testing.

## Issue

In this repo we have:

  - An execution module named `expmod` with a function named `id_to_fqdn`.
  - A runner module named `exprunner` with a function named `id_to_fqdn`.
  - Associated tests to validate both the module and the runner function output.

The runner function uses the `expmod.id_to_fqdn` execution module function by loading it with `salt.loader.minion_mods`

The tests for `expmod.py` appear to work as intended.

The tests I am attempting to create for the runner module keep giving a KeyError.

I've not been able to figure out the correct syntax to make the `expmod.id_to_fqdn` function available when testing `exprunner.id_to_fqdn`.

I don't see this as a duplicate test because while `exprunner.id_to_fqdn` is a small "wrapper" around `expmod.id_to_fqdn` which is already tested, that wrapper has a tiny bit of logic that looked important to test. Perhaps that's an errant view.

## Module and Runner Execution

The module and runner do appear to work as intended.

- Unconfigured; no config, grains, or pillar `expmod` values we get the default `example.com`

```bash
# expmod w/o minion_id uses local minion_id and returns expected value
oot@salt-labsalt01-lo-local:/srv/salt# salt '*' expmod.id_to_fqdn
salt.labsalt01.lo.local:
    salt.labsalt01.lo.local.example.com

# expmod with a param produces expected value using the param string as minion_id
root@salt-labsalt01-lo-local:/srv/salt# salt '*' expmod.id_to_fqdn svc01
salt.labsalt01.lo.local:
    svc01.example.com

# the exprunner accepts it's parameter and creates the expeced output
root@salt-labsalt01-lo-local:/srv/salt# salt-run exprunner.id_to_fqdn svc01
svc01.example.com

```

- Grains configured with `expmod:domain: grainsdomain.value` as a "domain" to append.

```bash
# Set grains config
root@salt-labsalt01-lo-local:/srv/salt# salt-call grains.set expmod '{"domain": "grainsdomain.value"}'

# expmod w/o minion_id uses local minion_id and returns expected value
root@salt-labsalt01-lo-local:/srv/salt# salt '*' expmod.id_to_fqdn
salt.labsalt01.lo.local:
    salt.labsalt01.lo.local.grainsdomain.value

# expmod with a param produces expected value using the param string as minion_id
root@salt-labsalt01-lo-local:/srv/salt# salt '*' expmod.id_to_fqdn svc01
salt.labsalt01.lo.local:
    svc01.grainsdomain.value

# the exprunner accepts it's parameter and creates the expeced output
root@salt-labsalt01-lo-local:/srv/salt# salt-run exprunner.id_to_fqdn svc01
svc01.grainsdomain.value
```

## Test Output

- [test_module_expmod.py](test/unit/test_module_expmod.py) tests pass with expected outcomes

```console
$ pytest ./test/unit/test_module_expmod.py 
===================================================================================== test session starts ======================================================================================
platform linux -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/repos/github/memblin/salt-modules
configfile: pytest.ini
plugins: skip-markers-1.5.2, helpers-namespace-2021.12.29, system-statistics-1.0.2, shell-utilities-1.9.7, salt-factories-1.0.4, anyio-4.8.0
collected 9 items                                                                                                                                                                              

test/unit/test_module_expmod.py::test_id_to_fqdn_via_config[app-1-None-app-1.example.com] PASSED                                                                                         [ 11%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_config[app-2-example.com-app-2.example.com] PASSED                                                                                  [ 22%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_config[app-3-example.net-app-3.example.net] PASSED                                                                                  [ 33%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_grains[app-1-None-app-1.example.com] PASSED                                                                                         [ 44%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_grains[app-2-example.com-app-2.example.com] PASSED                                                                                  [ 55%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_grains[app-3-example.net-app-3.example.net] PASSED                                                                                  [ 66%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_pillar[app-1-None-app-1.example.com] PASSED                                                                                         [ 77%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_pillar[app-2-example.com-app-2.example.com] PASSED                                                                                  [ 88%]
test/unit/test_module_expmod.py::test_id_to_fqdn_via_pillar[app-3-example.net-app-3.example.net] PASSED                                                                                  [100%]

====================================================================================== 9 passed in 1.08s =======================================================================================
```

- [test_runner_exprunner.py](test/unit/test_runner_exprunner.py) fails with a KeyError and is unable to load `exprunner.id_to_fqdn`

```console
$ pytest ./test/unit/test_runner_exprunner.py 
===================================================================================== test session starts ======================================================================================
platform linux -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/repos/github/memblin/salt-modules
configfile: pytest.ini
plugins: skip-markers-1.5.2, helpers-namespace-2021.12.29, system-statistics-1.0.2, shell-utilities-1.9.7, salt-factories-1.0.4, anyio-4.8.0
collected 3 items                                                                                                                                                                              

test/unit/test_runner_exprunner.py::test_id_to_fqdn_via_grains[app-1-None-app-1.example.com] FAILED                                                                                      [ 33%]
test/unit/test_runner_exprunner.py::test_id_to_fqdn_via_grains[app-2-example.com-app-2.example.com] FAILED                                                                               [ 66%]
test/unit/test_runner_exprunner.py::test_id_to_fqdn_via_grains[app-3-example.net-app-3.example.net] FAILED                                                                               [100%]

=========================================================================================== FAILURES ===========================================================================================
___________________________________________________________________ test_id_to_fqdn_via_grains[app-1-None-app-1.example.com] ___________________________________________________________________

minion_id = 'app-1', domain = None, expected_fqdn = 'app-1.example.com'

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
>       assert exprunner.id_to_fqdn(minion_id) == expected_fqdn

test/unit/test_runner_exprunner.py:82: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
modules/_runners/exprunner.py:21: in id_to_fqdn
    return mods["exprunner.id_to_fqdn"](minion_id)
/home/user/.local/lib/python3.13/site-packages/salt/loader/lazy.py:384: in __getitem__
    _ = super().__getitem__(item)  # try to get the item from the dictionary
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <LazyLoader module='salt.loaded.module'>, key = 'exprunner.id_to_fqdn'

    def __getitem__(self, key):
        """
        Check if the key is ttld out, then do the get
        """
        if self._missing(key):
            raise KeyError(key)
    
        if key not in self._dict and not self.loaded:
            # load the item
            if self._load(key):
                log.debug("LazyLoaded %s", key)
                return self._dict[key]
            else:
                log.debug(
                    "Could not LazyLoad %s: %s", key, self.missing_fun_string(key)
                )
>               raise KeyError(key)
E               KeyError: 'exprunner.id_to_fqdn'

/home/user/.local/lib/python3.13/site-packages/salt/utils/lazy.py:104: KeyError
_______________________________________________________________ test_id_to_fqdn_via_grains[app-2-example.com-app-2.example.com] ________________________________________________________________

minion_id = 'app-2', domain = 'example.com', expected_fqdn = 'app-2.example.com'

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
>       assert exprunner.id_to_fqdn(minion_id) == expected_fqdn

test/unit/test_runner_exprunner.py:82: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
modules/_runners/exprunner.py:21: in id_to_fqdn
    return mods["exprunner.id_to_fqdn"](minion_id)
/home/user/.local/lib/python3.13/site-packages/salt/loader/lazy.py:384: in __getitem__
    _ = super().__getitem__(item)  # try to get the item from the dictionary
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <LazyLoader module='salt.loaded.module'>, key = 'exprunner.id_to_fqdn'

    def __getitem__(self, key):
        """
        Check if the key is ttld out, then do the get
        """
        if self._missing(key):
            raise KeyError(key)
    
        if key not in self._dict and not self.loaded:
            # load the item
            if self._load(key):
                log.debug("LazyLoaded %s", key)
                return self._dict[key]
            else:
                log.debug(
                    "Could not LazyLoad %s: %s", key, self.missing_fun_string(key)
                )
>               raise KeyError(key)
E               KeyError: 'exprunner.id_to_fqdn'

/home/user/.local/lib/python3.13/site-packages/salt/utils/lazy.py:104: KeyError
_______________________________________________________________ test_id_to_fqdn_via_grains[app-3-example.net-app-3.example.net] ________________________________________________________________

minion_id = 'app-3', domain = 'example.net', expected_fqdn = 'app-3.example.net'

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
>       assert exprunner.id_to_fqdn(minion_id) == expected_fqdn

test/unit/test_runner_exprunner.py:82: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
modules/_runners/exprunner.py:21: in id_to_fqdn
    return mods["exprunner.id_to_fqdn"](minion_id)
/home/user/.local/lib/python3.13/site-packages/salt/loader/lazy.py:384: in __getitem__
    _ = super().__getitem__(item)  # try to get the item from the dictionary
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <LazyLoader module='salt.loaded.module'>, key = 'exprunner.id_to_fqdn'

    def __getitem__(self, key):
        """
        Check if the key is ttld out, then do the get
        """
        if self._missing(key):
            raise KeyError(key)
    
        if key not in self._dict and not self.loaded:
            # load the item
            if self._load(key):
                log.debug("LazyLoaded %s", key)
                return self._dict[key]
            else:
                log.debug(
                    "Could not LazyLoad %s: %s", key, self.missing_fun_string(key)
                )
>               raise KeyError(key)
E               KeyError: 'exprunner.id_to_fqdn'

/home/user/.local/lib/python3.13/site-packages/salt/utils/lazy.py:104: KeyError
=================================================================================== short test summary info ====================================================================================
FAILED test/unit/test_runner_exprunner.py::test_id_to_fqdn_via_grains[app-1-None-app-1.example.com] - KeyError: 'exprunner.id_to_fqdn'
FAILED test/unit/test_runner_exprunner.py::test_id_to_fqdn_via_grains[app-2-example.com-app-2.example.com] - KeyError: 'exprunner.id_to_fqdn'
FAILED test/unit/test_runner_exprunner.py::test_id_to_fqdn_via_grains[app-3-example.net-app-3.example.net] - KeyError: 'exprunner.id_to_fqdn'
====================================================================================== 3 failed in 1.11s =======================================================================================
```
