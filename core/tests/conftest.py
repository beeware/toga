import pytest

from toga_dummy.utils import EventLog


@pytest.fixture(autouse=True)
def reset_event_log():
    EventLog.reset()
