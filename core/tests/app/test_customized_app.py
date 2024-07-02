import asyncio
from unittest.mock import Mock

import pytest

import toga


class CustomizedApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()
        # Create a secondary simple window as part of app startup to verify
        # that toolbar handling is skipped.
        self.other_window = toga.Window()

        self._mock_new = Mock()
        self._mock_open = Mock()
        self._mock_preferences = Mock()
        self._mock_save = Mock()
        self._mock_save_as = Mock()
        self._mock_save_all = Mock()

    def new(self):
        self._mock_new()

    def open(self, path):
        self._mock_open(path)

    def preferences(self):
        self._mock_preferences()

    def save(self):
        self._mock_save()

    def save_as(self):
        self._mock_save_as()

    def save_all(self):
        self._mock_save_all()


class AsyncCustomizedApp(CustomizedApp):
    # A custom app where preferences and document-management commands are user-defined
    # as async handlers.

    async def preferences(self):
        self._mock_preferences()

    async def save(self):
        self._mock_save()

    async def save_as(self):
        self._mock_save_as()

    async def save_all(self):
        self._mock_save_all()


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_create(event_loop, AppClass):
    """An app with overridden commands can be created"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    assert custom_app.formal_name == "Custom App"
    assert custom_app.app_id == "org.beeware.customized-app"
    assert custom_app.app_name == "customized-app"

    # The default implementations of the on_running and on_exit handlers
    # have been wrapped as simple handlers
    assert custom_app.on_running._raw.__func__ == toga.App.on_running
    assert custom_app.on_exit._raw.__func__ == toga.App.on_exit

    # About menu item exists and is disabled
    assert toga.Command.ABOUT in custom_app.commands
    assert custom_app.commands[toga.Command.ABOUT].enabled

    # Preferences exist and are enabled
    assert toga.Command.PREFERENCES in custom_app.commands
    assert custom_app.commands[toga.Command.PREFERENCES].enabled

    # A change handler has been added to the MainWindow's toolbar CommandSet
    assert custom_app.main_window.toolbar.on_change is not None


def test_new_menu(event_loop):
    """The custom new method is activated by the new menu"""
    custom_app = CustomizedApp("Custom App", "org.beeware.customized-app")

    # Command.NEW is a template.
    result = custom_app.commands[toga.Command.NEW.format(None)].action()
    if asyncio.isfuture(result):
        custom_app.loop.run_until_complete(result)

    # A custom new method, on an app without document types, is invoked without
    # arguments.
    custom_app._mock_new.assert_called_once_with()


def test_open_menu(event_loop):
    """The custom open method is activated by the open menu"""
    custom_app = CustomizedApp("Custom App", "org.beeware.customized-app")

    file_path = Mock()
    custom_app._impl.dialog_responses["OpenFileDialog"] = [file_path]

    result = custom_app.commands[toga.Command.OPEN].action()
    if asyncio.isfuture(result):
        custom_app.loop.run_until_complete(result)
    custom_app._mock_open.assert_called_once_with(file_path)


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_preferences_menu(event_loop, AppClass):
    """The custom preferences method is activated by the preferences menu"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    result = custom_app.commands[toga.Command.PREFERENCES].action()
    if asyncio.isfuture(result):
        custom_app.loop.run_until_complete(result)
    custom_app._mock_preferences.assert_called_once_with()


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_save_menu(event_loop, AppClass):
    """The custom save method is activated by the save menu"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    result = custom_app.commands[toga.Command.SAVE].action()
    if asyncio.isfuture(result):
        custom_app.loop.run_until_complete(result)
    custom_app._mock_save.assert_called_once_with()


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_save_as_menu(event_loop, AppClass):
    """The custom save_as method is activated by the save_as menu"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    result = custom_app.commands[toga.Command.SAVE_AS].action()
    if asyncio.isfuture(result):
        custom_app.loop.run_until_complete(result)
    custom_app._mock_save_as.assert_called_once_with()


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_save_all_menu(event_loop, AppClass):
    """The custom save_all method is activated by the save_all menu"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    result = custom_app.commands[toga.Command.SAVE_ALL].action()
    if asyncio.isfuture(result):
        custom_app.loop.run_until_complete(result)
    custom_app._mock_save_all.assert_called_once_with()


def test_initial_window_from_new(event_loop):
    """If an app doesn't have a main window or doc types, but *does* have a new method,
    that method is used to populate the initial window."""

    class PseudoDocApp(toga.App):
        def startup(self):
            self.main_window = None

        def new(self):
            window = toga.Window(title="Pseudo Document")
            window.show()

    app = PseudoDocApp("Pseudo Doc App", "org.beeware.pseudo-doc-app")

    # The new method was used to create an initial window.
    assert len(app.windows) == 1
    assert list(app.windows)[0].title == "Pseudo Document"
