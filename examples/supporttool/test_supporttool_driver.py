import pytest
from labgrid.driver.supporttool_driver import SupportToolDriver

class DummySupt:
    port = 60000

class DummyTarget:
    name = "dummy"

@pytest.fixture
def driver(monkeypatch):
    # Patch out the labgrid binding logic
    monkeypatch.setattr(SupportToolDriver, "__attrs_post_init__", lambda self: None)

    target = DummyTarget()
    d = SupportToolDriver(target=target, name=target.name)
    d.supt = DummySupt()
    return d

def test_api_running(driver):
    assert driver.check_rest_api_running() is True

def test_supporttool_activated(driver):
    assert driver.check_supporttool_activated() is True
