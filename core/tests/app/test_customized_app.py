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

        self._preferences = Mock()

    def preferences(self):
        self._preferences()


class AsyncCustomizedApp(CustomizedApp):
    # A custom app where preferences and document-management commands are user-defined
    # as async handlers.

    async def preferences(self):
        self._preferences()


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

    # About menu item exists and is disabled
    assert toga.Command.ABOUT in custom_app.commands
    assert custom_app.commands[toga.Command.ABOUT].enabled

    # Preferences exist and are enabled
    assert toga.Command.PREFERENCES in custom_app.commands
    assert custom_app.commands[toga.Command.PREFERENCES].enabled

    # A change handler has been added to the MainWindow's toolbar CommandSet
    assert custom_app.main_window.toolbar.on_change is not None


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
    custom_app._preferences.assert_called_once_with()
