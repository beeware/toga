from pathlib import Path
from unittest.mock import Mock

import pytest

import toga


class CustomizedApp(toga.App):
    def startup(self):
        self.main_window = toga.Window()

        self._preferences = Mock()

        self._new = Mock()
        self._open = Mock()

        self.allow_save = False
        self._save = Mock()
        self._save_as = Mock()
        self._save_all = Mock()

    def preferences(self):
        self._preferences()

    def can_save(self) -> bool:
        return self.allow_save

    def can_save_all(self) -> bool:
        return self.allow_save

    def new(self, doc_type):
        self._new(doc_type)

    def open(self, path):
        self._open(path)

    def save(self, window):
        self._save(window)

    def save_as(self, window):
        self._save_as(window)

    def save_all(self):
        self._save_all()


class AsyncCustomizedApp(CustomizedApp):
    # A custom app where preferences and document-management commands are user-defined
    # as async handlers.

    async def preferences(self):
        self._preferences()

    async def new(self, doc_type):
        self._new(doc_type)

    async def open(self, path):
        self._open(path)

    async def save(self, window):
        self._save(window)

    async def save_as(self, window):
        self._save_as(window)

    async def save_all(self):
        self._save_all()


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
    assert custom_app.on_exit._raw is None

    # Preferences exist and are enabled
    assert hasattr(custom_app._impl, "preferences_command")
    assert custom_app._impl.preferences_command.enabled

    # Document management commands (except for new) all exist because of overrides
    assert hasattr(custom_app._impl, "new_commands")
    assert hasattr(custom_app._impl, "open_command")
    assert hasattr(custom_app._impl, "save_command")
    assert hasattr(custom_app._impl, "save_as_command")
    assert hasattr(custom_app._impl, "save_all_command")


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

    future = custom_app._impl.preferences_command.action()

    custom_app.loop.run_until_complete(future)
    custom_app._preferences.assert_called_once_with()


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_new_menu(event_loop, AppClass):
    """The custom new method is activated by the new menu item"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    # As there's no document types, and an overridden new, there is
    # a single new command. It uses the "none" document type.
    future = custom_app._impl.new_commands[None].action()

    custom_app.loop.run_until_complete(future)
    custom_app._new.assert_called_once_with(None)


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_open_menu(event_loop, AppClass):
    """The custom open method is activated by the open menu"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    path = Path("/path/to/file.txt")
    custom_app.main_window._impl.dialog_responses["OpenFileDialog"] = [path]

    future = custom_app._impl.open_command.action()

    custom_app.loop.run_until_complete(future)
    custom_app._open.assert_called_once_with(path)


@pytest.mark.parametrize(
    "AppClass",
    [
        CustomizedApp,
        AsyncCustomizedApp,
    ],
)
def test_open_menu_cancelled(event_loop, AppClass):
    """The open action can be cancelled by not selecting a file"""
    custom_app = AppClass("Custom App", "org.beeware.customized-app")

    custom_app.main_window._impl.dialog_responses["OpenFileDialog"] = [None]

    future = custom_app._impl.open_command.action()

    custom_app.loop.run_until_complete(future)
    custom_app._open.assert_not_called()


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

    future = custom_app._impl.save_command.action()
    custom_app.loop.run_until_complete(future)

    # can_save is False; save won't be invoked
    custom_app._save.assert_not_called()

    # Allow saving
    custom_app.allow_save = True

    future = custom_app._impl.save_command.action()
    custom_app.loop.run_until_complete(future)
    custom_app._save.assert_called_once_with(custom_app.main_window)


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

    future = custom_app._impl.save_as_command.action()
    custom_app.loop.run_until_complete(future)

    # can_save is False; save won't be invoked
    custom_app._save_as.assert_not_called()

    # Allow saving
    custom_app.allow_save = True

    future = custom_app._impl.save_as_command.action()
    custom_app.loop.run_until_complete(future)
    custom_app._save_as.assert_called_once_with(custom_app.main_window)


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
    future = custom_app._impl.save_all_command.action()
    custom_app.loop.run_until_complete(future)

    # can_save is False; save won't be invoked
    custom_app._save_all.assert_not_called()

    # Allow saving
    custom_app.allow_save = True

    future = custom_app._impl.save_all_command.action()
    custom_app.loop.run_until_complete(future)
    custom_app._save_all.assert_called_once_with()
