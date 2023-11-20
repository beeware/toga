from unittest.mock import Mock

import toga
from toga_dummy.utils import assert_action_performed


def test_windowless_app():
    """A WindowlessApp could be created"""
    on_exit_handler = Mock()

    app = toga.WindowlessApp(
        formal_name="Test App",
        app_id="org.example.test-app",
        author="Jane Developer",
        version="1.2.3",
        home_page="https://example.com/test-app",
        description="A test app",
        on_exit=on_exit_handler,
    )

    assert app.author == "Jane Developer"
    assert app.version == "1.2.3"
    assert app.home_page == "https://example.com/test-app"
    assert app.description == "A test app"

    assert app.on_exit._raw == on_exit_handler

    # A windowless app was created.
    assert_action_performed(app, "create Windowless App")
