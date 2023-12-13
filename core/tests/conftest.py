import sys

import pytest

import toga
from toga_dummy.utils import EventLog


@pytest.fixture(autouse=True)
def reset_event_log():
    EventLog.reset()


@pytest.fixture(autouse=True)
def clear_sys_modules(monkeypatch):
    try:
        # App startup is influenced by things like the state of sys.modules, and the
        # presence of __main__ in particular. Pytest doesn't need __main__ to work;
        # so if it exists, delete it for the purposes of each test.
        monkeypatch.delitem(sys.modules, "__main__")
    except KeyError:
        pass


class TestApp(toga.App):
    pass


@pytest.fixture
def app(event_loop):
    return TestApp(formal_name="Test App", app_id="org.beeware.toga.test-app")
