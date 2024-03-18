import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
)


class ExampleBackgroundApp(toga.App):
    def startup(self):
        self.main_window = toga.App.BACKGROUND


@pytest.fixture
def background_app(event_loop):
    app = ExampleBackgroundApp(
        "Test App",
        "org.beeware.background-app",
    )
    return app


def test_create(background_app):
    """A background app can be created."""
    # App has been created
    assert background_app._impl.interface == background_app
    assert_action_performed(background_app, "create App")

    # App has no windows
    assert len(background_app.windows) == 0


def test_no_exit_last_window_close(background_app):
    """Windows can be created and closed without closing the app."""
    # App has no windows initially
    assert len(background_app.windows) == 0

    window = toga.Window()
    window.content = toga.Box()
    window.show()

    # App has a window
    assert len(background_app.windows) == 1

    # Close the window
    window.close()

    # Window has been closed, but the app hasn't exited.
    assert len(background_app.windows) == 0
    assert_action_performed(window, "close")
    assert_action_not_performed(background_app, "exit")
