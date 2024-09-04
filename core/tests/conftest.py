import sys

import pytest

import toga
from toga import window as toga_window
from toga_dummy.utils import EventLog


@pytest.fixture(autouse=True)
def reset_global_state():
    # Clear the testing event log
    EventLog.reset()
    # Reset the global window count
    toga_window._window_count = -1


@pytest.fixture(autouse=True)
def no_dangling_tasks():
    """Ensure any tasks for the test were removed when the test finished."""
    yield
    if toga.App.app:
        tasks = toga.App.app._running_tasks
        assert not tasks, f"the app has dangling tasks: {tasks}"


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
    def startup(self):
        # Ensure that Toga's task factory is tracking all tasks
        toga_task_factory = self.loop.get_task_factory()

        def task_factory(loop, coro, context=None):
            if sys.version_info < (3, 11):
                task = toga_task_factory(loop, coro)
            else:
                task = toga_task_factory(loop, coro, context=context)
            assert task in self._running_tasks, f"missing task reference for {task}"
            return task

        self.loop.set_task_factory(task_factory)
        super().startup()


@pytest.fixture
def app(event_loop):
    # The app icon is cached; purge the app icon cache if it exists
    try:
        del toga.Icon.__APP_ICON
    except AttributeError:
        pass

    return TestApp(formal_name="Test App", app_id="org.beeware.toga.test-app")
