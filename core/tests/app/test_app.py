import asyncio
import importlib.metadata
import sys
import webbrowser
from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)

EXPLICIT_FULL_APP_KWARGS = dict(
    formal_name="Explicit App",
    app_id="org.beeware.explicit-app",
    app_name="override-app",
)
EXPLICIT_MIN_APP_KWARGS = dict(
    formal_name="Explicit App",
    app_id="org.beeware.explicit-app",
)
APP_METADATA = {
    "Formal-Name": "Test App",
    "App-ID": "org.beeware.test-app",
    "Name": "test-app",
}


@pytest.mark.parametrize(
    (
        "kwargs, metadata, main_module, expected_formal_name, expected_app_id, "
        "expected_app_name"
    ),
    [
        ###########################################################################
        # Invoking as python my_app.py, or as an interactive prompt
        # This causes a main package of None
        ###########################################################################
        # Explicit app properties, no metadata
        (
            EXPLICIT_FULL_APP_KWARGS,
            None,
            Mock(__package__=None),
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
        # Explicit app properties, but implied distribution name from app_id, no
        # metadata
        (
            EXPLICIT_MIN_APP_KWARGS,
            None,
            Mock(__package__=None),
            "Explicit App",
            "org.beeware.explicit-app",
            "explicit-app",
        ),
        # No app properties, with metadata
        (
            dict(),
            APP_METADATA,
            Mock(__package__=None),
            "Test App",
            "org.beeware.test-app",
            "toga",
        ),
        # Explicit app properties, with metadata. Explicit values take precedence.
        (
            EXPLICIT_FULL_APP_KWARGS,
            APP_METADATA,
            Mock(__package__=None),
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
        ###########################################################################
        # Invoking as python -m my_app, where code is in my_app.py
        # This causes a main module of ""
        ###########################################################################
        # Explicit app properties, no metadata
        (
            EXPLICIT_FULL_APP_KWARGS,
            None,
            Mock(__package__=""),
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
        # Explicit app properties, but implied distribution name from app_id, no metadata
        (
            EXPLICIT_MIN_APP_KWARGS,
            None,
            Mock(__package__=""),
            "Explicit App",
            "org.beeware.explicit-app",
            "explicit-app",
        ),
        # No app properties, with metadata
        (
            dict(),
            APP_METADATA,
            Mock(__package__=""),
            "Test App",
            "org.beeware.test-app",
            "toga",
        ),
        # Explicit app properties, with metadata. Explicit values take precedence.
        (
            EXPLICIT_FULL_APP_KWARGS,
            APP_METADATA,
            Mock(__package__=""),
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
        ###########################################################################
        # Invoking as python -m my_app, where my_app is a folder with a __main__
        # This causes a main module of "my_app"
        ###########################################################################
        # Explicit app properties, no metadata
        (
            EXPLICIT_FULL_APP_KWARGS,
            None,
            Mock(__package__="my_app"),
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
        # Explicit app properties, but implied distribution name from __package__, no
        # metadata
        (
            EXPLICIT_MIN_APP_KWARGS,
            None,
            Mock(__package__="my_app"),
            "Explicit App",
            "org.beeware.explicit-app",
            "my_app",
        ),
        # No app properties, with metadata
        (
            dict(),
            APP_METADATA,
            Mock(__package__="my_app"),
            "Test App",
            "org.beeware.test-app",
            "my_app",
        ),
        # Explicit app properties, with metadata. Explicit values take precedence.
        (
            EXPLICIT_FULL_APP_KWARGS,
            APP_METADATA,
            Mock(__package__="my_app"),
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
        ###########################################################################
        # Invoking in a test harness, where there's no __main__
        ###########################################################################
        # Explicit app properties, no metadata
        (
            EXPLICIT_FULL_APP_KWARGS,
            None,
            None,
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
        # Explicit app properties, but implied distribution name from app_id, no metadata
        (
            EXPLICIT_MIN_APP_KWARGS,
            None,
            None,
            "Explicit App",
            "org.beeware.explicit-app",
            "explicit-app",
        ),
        # No app properties, with metadata
        (
            dict(),
            APP_METADATA,
            None,
            "Test App",
            "org.beeware.test-app",
            "toga",
        ),
        # Explicit app properties, with metadata. Explicit values take precedence.
        (
            EXPLICIT_FULL_APP_KWARGS,
            APP_METADATA,
            None,
            "Explicit App",
            "org.beeware.explicit-app",
            "override-app",
        ),
    ],
)
def test_create(
    monkeypatch,
    kwargs,
    metadata,
    main_module,
    expected_formal_name,
    expected_app_id,
    expected_app_name,
):
    """A simple app can be created"""
    # Monkeypatch the metadata retrieval function
    if metadata:
        metadata_mock = Mock(return_value=metadata)
    else:
        metadata_mock = Mock(
            side_effect=importlib.metadata.PackageNotFoundError(expected_app_name)
        )
    monkeypatch.setattr(importlib.metadata, "metadata", metadata_mock)

    # Monkeypatch the main module
    if main_module is None:
        try:
            monkeypatch.delitem(sys.modules, "__main__")
        except KeyError:
            pass
    else:
        monkeypatch.setitem(sys.modules, "__main__", main_module)

    app = toga.App(**kwargs)

    assert app.formal_name == expected_formal_name
    assert app.app_id == expected_app_id
    assert app.app_name == expected_app_name
    assert app.on_exit._raw is None

    metadata_mock.assert_called_once_with(expected_app_name)


@pytest.mark.parametrize(
    "kwargs, exc_type, message",
    [
        (dict(), RuntimeError, "Toga application must have a formal name"),
        (
            dict(formal_name="Something"),
            RuntimeError,
            "Toga application must have an app ID",
        ),
        (
            dict(windows=()),
            ValueError,
            "The `windows` constructor argument of toga.App has been removed",
        ),
    ],
)
def test_bad_app_creation(kwargs, exc_type, message):
    """Errors are raised"""
    with pytest.raises(exc_type, match=message):
        toga.App(**kwargs)


def test_app_metadata(monkeypatch):
    """An app can load metadata from the .dist-info file"""
    monkeypatch.setattr(
        importlib.metadata,
        "metadata",
        Mock(
            return_value={
                "Formal-Name": "Metadata Name",
                "Name": "metadata",
                "App-ID": "org.beeware.metadata",
                "Author": "Jane Developer",
                "Version": "1.2.3",
                "Home-page": "https://example.com/test-app",
                "Summary": "A test app",
            }
        ),
    )

    # We can't use the app fixture here, because we need the metadata to be loaded as
    # part of app construction.
    app = toga.App(
        formal_name="Test App",
        app_id="org.example.test-app",
    )

    assert app.author == "Jane Developer"
    assert app.version == "1.2.3"
    assert app.home_page == "https://example.com/test-app"
    assert app.description == "A test app"


def test_explicit_app_metadata(monkeypatch):
    """App metadata can be provided explicitly, overriding module-level metadata"""
    monkeypatch.setattr(
        importlib.metadata,
        "metadata",
        Mock(
            return_value={
                "Formal-Name": "Metadata Name",
                "Name": "metadata",
                "App-ID": "org.beeware.metadata",
                "Author": "Alice Metadata",
                "Version": "2.3.4",
                "Home-page": "https://example.com/metadata",
                "Summary": "Metadata description of app",
            }
        ),
    )

    on_exit_handler = Mock()

    app = toga.App(
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


@pytest.mark.parametrize("construct", [True, False])
def test_icon_construction(construct):
    """The app icon can be set during construction"""
    if construct:
        icon = toga.Icon("path/to/icon")
    else:
        icon = "path/to/icon"

    app = toga.App(
        formal_name="Test App",
        app_id="org.example.test",
        icon=icon,
    )
    assert isinstance(app.icon, toga.Icon)
    assert app.icon.path == Path("path/to/icon")


@pytest.mark.parametrize("construct", [True, False])
def test_icon(app, construct):
    """The app icon can be changed"""
    if construct:
        icon = toga.Icon("path/to/icon")
    else:
        icon = "path/to/icon"

    # Default icon matches distribution name
    assert isinstance(app.icon, toga.Icon)
    assert app.icon.path == Path("resources/test-app")

    # Change icon
    app.icon = icon
    assert isinstance(app.icon, toga.Icon)
    assert app.icon.path == Path("path/to/icon")


def test_current_window(app):
    """The current window can be set and changed."""
    other_window = toga.Window()

    # There are two windows - the main window, plus "other"
    assert len(app.windows) == 2
    assert_action_performed_with(app, "set_main_window", window=app.main_window)

    # The initial current window is the main window
    assert app.current_window == app.main_window

    # Change the current window
    app.current_window = other_window
    assert app.current_window == other_window
    assert_action_performed_with(app, "set_current_window", window=other_window)


def test_no_current_window(app):
    """If there's no current window, current_window reflects this"""
    # If all the windows are deleted, and there's no main window (e.g., if it's a document app)
    # there might be no current window.
    app._main_window = None

    # The current window evaluates as None
    assert app.current_window is None


def test_full_screen():
    """The app can be put into full screen mode."""
    window1 = toga.Window()
    window2 = toga.Window()
    app = toga.App(formal_name="Test App", app_id="org.example.test")

    assert not app.is_full_screen

    # If we're not full screen, exiting full screen is a no-op
    app.exit_full_screen()
    assert_action_not_performed(app, "exit_full_screen")

    # Enter full screen with 2 windows
    app.set_full_screen(window2, app.main_window)
    assert app.is_full_screen
    assert_action_performed_with(
        app, "enter_full_screen", windows=(window2, app.main_window)
    )

    # Change the screens that are full screen
    app.set_full_screen(app.main_window, window1)
    assert app.is_full_screen
    assert_action_performed_with(
        app, "enter_full_screen", windows=(app.main_window, window1)
    )

    # Exit full screen mode
    app.exit_full_screen()
    assert not app.is_full_screen
    assert_action_performed_with(
        app, "exit_full_screen", windows=(app.main_window, window1)
    )


def test_set_empty_full_screen_window_list():
    """Setting the full screen window list to [] is an explicit exit"""
    app = toga.App(formal_name="Test App", app_id="org.example.test")
    window1 = toga.Window()
    window2 = toga.Window()

    assert not app.is_full_screen

    # Change the screens that are full screen
    app.set_full_screen(window1, window2)
    assert app.is_full_screen
    assert_action_performed_with(app, "enter_full_screen", windows=(window1, window2))

    # Exit full screen mode by setting no windows full screen
    app.set_full_screen()
    assert not app.is_full_screen
    assert_action_performed_with(app, "exit_full_screen", windows=(window1, window2))


def test_show_hide_cursor(app):
    """The app cursor can be shown and hidden"""
    app.hide_cursor()
    assert_action_performed(app, "hide_cursor")

    app.show_cursor()
    assert_action_performed(app, "show_cursor")


def test_startup_method():
    """If an app provides a startup method, it will be invoked during startup"""
    startup = Mock()
    app = toga.App(
        formal_name="Test App",
        app_id="org.example.test",
        startup=startup,
    )

    startup.assert_called_once_with(app)


def test_startup_subclass():
    """App can be subclassed"""

    class SubclassedApp(toga.App):
        def startup(self):
            self.main_window = toga.MainWindow()

    app = SubclassedApp(formal_name="Test App", app_id="org.example.test")

    # The main window will exist, and will have the app's formal name.
    assert app.main_window.title == "Test App"


def test_startup_subclass_no_main_window():
    """If a subclassed app doesn't define a main window, an error is raised"""

    class SubclassedApp(toga.App):
        def startup(self):
            pass

    with pytest.raises(ValueError, match=r"Application does not have a main window."):
        SubclassedApp(formal_name="Test App", app_id="org.example.test")


def test_about(app):
    """The about dialog for the app can be shown"""
    app.about()
    assert_action_performed(app, "show_about_dialog")


def test_visit_homepage(monkeypatch):
    """The app's homepage can be opened"""
    app = toga.App(
        formal_name="Test App",
        app_id="org.example.test",
        home_page="https://example.com/test-app",
    )
    open_webbrowser = Mock()
    monkeypatch.setattr(webbrowser, "open", open_webbrowser)

    # The app has no homepage by default, so visit is a no-op
    app.visit_homepage()

    open_webbrowser.assert_called_once_with("https://example.com/test-app")


def test_no_homepage(monkeypatch, app):
    """If the app doesn't have a home page, visit_homepage is a no-op"""
    open_webbrowser = Mock()
    monkeypatch.setattr(webbrowser, "open", open_webbrowser)

    # The app has no homepage by default, so visit is a no-op
    app.visit_homepage()

    open_webbrowser.assert_not_called()


def test_beep(app):
    """The machine can go Bing!"""
    app.beep()
    assert_action_performed(app, "beep")


def test_exit_direct(app):
    """An app can be exited directly"""
    on_exit_handler = Mock(return_value=True)
    app.on_exit = on_exit_handler

    # Exit the app directly
    app.exit()

    # App has been exited, but the exit handler has *not* been invoked.
    assert_action_performed(app, "exit")
    on_exit_handler.assert_not_called()


def test_exit_no_handler(app):
    """A app without a exit handler can be exited"""
    # Exit the app
    app._impl.simulate_exit()

    # Window has been exitd, and is no longer in the app's list of windows.
    assert_action_performed(app, "exit")


def test_exit_sucessful_handler(app):
    """An app with a successful exit handler can be exited"""
    on_exit_handler = Mock(return_value=True)
    app.on_exit = on_exit_handler

    # Close the app
    app._impl.simulate_exit()

    # App has been exited
    assert_action_performed(app, "exit")
    on_exit_handler.assert_called_once_with(app)


def test_exit_rejected_handler(app):
    """An app can have a exit handler that rejects the exit"""
    on_exit_handler = Mock(return_value=False)
    app.on_exit = on_exit_handler

    # Close the window
    app._impl.simulate_exit()

    # App has been *not* exited
    assert_action_not_performed(app, "exit")
    on_exit_handler.assert_called_once_with(app)


def test_loop(app, event_loop):
    """The main thread's event loop can be accessed"""
    assert isinstance(app.loop, asyncio.AbstractEventLoop)
    assert app.loop is event_loop


def test_background_task(app):
    """A background task can be queued"""
    canary = Mock()

    async def background(app, **kwargs):
        canary()

    app.add_background_task(background)

    # Create an async task that we can use to start the event loop for a short time.
    async def waiter():
        await asyncio.sleep(0.1)

    app.loop.run_until_complete(waiter())

    # Once the loop has executed, the background task should have executed as well.
    canary.assert_called_once()


def test_deprecated_id():
    """The deprecated `id` constructor argument is ignored, and the property of the same
    name is redirected to `app_id`
    """
    id_warning = r"App.id is deprecated.* Use app_id instead"
    with pytest.warns(DeprecationWarning, match=id_warning):
        app = toga.App("Test App", "org.example.test", id="test_app_id")

    assert app.app_id == "org.example.test"
    with pytest.warns(DeprecationWarning, match=id_warning):
        assert app.id == "org.example.test"


def test_deprecated_name():
    """The deprecated `name` property is redirected to `formal_name`"""
    name_warning = r"App.name is deprecated. Use formal_name instead"
    app = toga.App("Test App", "org.example.test")

    assert app.formal_name == "Test App"
    with pytest.warns(DeprecationWarning, match=name_warning):
        assert app.name == "Test App"
