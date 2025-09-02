from types import NoneType
from unittest.mock import Mock

import pytest

import toga


async def test_unsupported_widget(app):
    """If a widget isn't implemented, the factory raises NotImplementedError."""
    with pytest.raises(NotImplementedError) as exc:
        _ = app.factory.NoSuchWidget
    assert "backend doesn't implement NoSuchWidget" in str(exc)


async def test_main_window_toolbar(app, main_window, main_window_probe):
    """A toolbar can be added to a main window"""
    # Add some items to show the toolbar
    assert not main_window_probe.has_toolbar()
    main_window.toolbar.add(app.cmd1, app.cmd2)

    # Add some more items to an existing toolbar
    main_window.toolbar.add(app.cmd3, app.cmd4)

    await main_window_probe.redraw("Main window has a toolbar")
    assert main_window_probe.has_toolbar()
    # Ordering is lexicographical for cmd 2 and 3.
    main_window_probe.assert_toolbar_item(
        0,
        label="Full command",
        tooltip="A full command definition",
        has_icon=True,
        enabled=True,
    )
    main_window_probe.assert_is_toolbar_separator(1)
    main_window_probe.assert_toolbar_item(
        2,
        label="No Icon",
        tooltip="A command with no icon",
        has_icon=False,
        enabled=True,
    )
    main_window_probe.assert_toolbar_item(
        3,
        label="No Tooltip",
        tooltip=None,
        has_icon=True,
        enabled=True,
    )
    main_window_probe.assert_is_toolbar_separator(4, section=True)
    main_window_probe.assert_toolbar_item(
        5,
        label="Sectioned",
        tooltip="I'm in another section",
        has_icon=True,
        enabled=True,
    )

    # Press the first toolbar button
    main_window_probe.press_toolbar_button(0)
    await main_window_probe.redraw("Command 1 invoked")
    app.cmd_action.assert_called_once_with(app.cmd1)
    app.cmd_action.reset_mock()

    # Disable the first toolbar button
    app.cmd1.enabled = False
    await main_window_probe.redraw("Command 1 disabled")
    main_window_probe.assert_toolbar_item(
        0,
        label="Full command",
        tooltip="A full command definition",
        has_icon=True,
        enabled=False,
    )

    # Re-enable the first toolbar button
    app.cmd1.enabled = True
    await main_window_probe.redraw("Command 1 re-enabled")
    main_window_probe.assert_toolbar_item(
        0,
        label="Full command",
        tooltip="A full command definition",
        has_icon=True,
        enabled=True,
    )

    # Remove the toolbar
    main_window.toolbar.clear()
    await main_window_probe.redraw("Main window has no toolbar")
    assert not main_window_probe.has_toolbar()

    # Removing it again should have no effect
    main_window.toolbar.clear()
    await main_window_probe.redraw("Main window has no toolbar")
    assert not main_window_probe.has_toolbar()


async def test_system_menus(app_probe):
    """System-specific menus behave as expected"""
    # Check that the system menus (which can be platform specific) exist.
    app_probe.assert_system_menus()


async def test_menu_about(monkeypatch, app, app_probe):
    """The about menu can be displayed"""
    app_probe.activate_menu_about()
    # When in CI, Cocoa needs a little time to guarantee the dialog is displayed.
    await app_probe.redraw("About dialog shown", delay=0.1)

    await app_probe.close_about_dialog()
    await app_probe.redraw("About dialog destroyed")

    # Make the app definition minimal to verify the dialog still displays
    monkeypatch.setattr(app, "_author", None)
    monkeypatch.setattr(app, "_version", None)
    monkeypatch.setattr(app, "_home_page", None)
    monkeypatch.setattr(app, "_description", None)

    app_probe.activate_menu_about()
    # When in CI, Cocoa needs a little time to guarantee the dialog is displayed.
    await app_probe.redraw("About dialog with no details shown", delay=0.1)

    await app_probe.close_about_dialog()
    await app_probe.redraw("About dialog with no details destroyed")


async def test_menu_visit_homepage(monkeypatch, app, app_probe):
    """The visit homepage menu item can be used"""
    # If the backend defines a VISIT_HOMEPAGE command, mock the visit_homepage method,
    # and rebind the visit homepage command to the visit_homepage method.
    visit_homepage = Mock()
    if toga.Command.VISIT_HOMEPAGE in app.commands:
        monkeypatch.setattr(app, "visit_homepage", visit_homepage)
        monkeypatch.setattr(
            app.commands[toga.Command.VISIT_HOMEPAGE], "_action", app.visit_homepage
        )

    app_probe.activate_menu_visit_homepage()

    # Browser opened
    visit_homepage.assert_called_once_with()


async def test_menu_items(app, app_probe):
    """Menu items can be created, disabled and invoked"""

    app_probe.assert_menu_item(
        ["Other", "Full command"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Disabled"],
        enabled=False,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "No Action"],
        enabled=False,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Submenu1 menu1", "Deep"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Other", "Wiggle"],
        enabled=True,
    )

    app_probe.assert_menu_order(
        ["Other"],
        ["Full command", "---", "Submenu1", "Submenu2", "Wiggle"],
    )
    app_probe.assert_menu_order(
        ["Other", "Submenu1"],
        ["Disabled", "No Action", "Submenu1 menu1"],
    )
    app_probe.assert_menu_order(
        ["Other", "Submenu1", "Submenu1 menu1"],
        ["Deep"],
    )
    app_probe.assert_menu_order(
        ["Other", "Submenu2"],
        ["Jiggle"],
    )

    app_probe.assert_menu_item(
        ["Commands", "No Tooltip"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Commands", "No Icon"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Commands", "Sectioned"],
        enabled=True,
    )

    # Enabled the disabled items
    app.disabled_cmd.enabled = True
    app.no_action_cmd.enabled = True
    await app_probe.redraw("Menu items enabled")

    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Disabled"],
        enabled=True,
    )
    # Item has no action - it can't be enabled
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "No Action"],
        enabled=False,
    )

    # Disable the items
    app.disabled_cmd.enabled = False
    app.no_action_cmd.enabled = False

    await app_probe.redraw("Menu item disabled again")
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Disabled"],
        enabled=False,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "No Action"],
        enabled=False,
    )


async def test_beep(app):
    """The machine can go Bing!"""
    # This isn't a very good test. It ensures coverage, which verifies that the method
    # can be invoked without raising an error, but there's no way to verify that the app
    # actually made a noise.
    app.beep()


async def test_screens(app, app_probe):
    """Screens must have unique origins and names, with the primary screen at (0,0)."""

    # Get the origin of screen 0
    assert app.screens[0].origin == (0, 0)

    # Check for unique names
    screen_names = [s.name for s in app.screens]
    unique_names = set(screen_names)
    assert len(screen_names) == len(unique_names)

    # Check that the origin of every other screen is not "0,0"
    origins_not_zero = all(screen.origin != (0, 0) for screen in app.screens[1:])
    assert origins_not_zero is True


async def test_app_icon(app, app_probe):
    """The app icon can be changed."""
    # Icon is initially the default
    app_probe.assert_app_icon(None)

    # Change the icon to an alternate
    app.icon = "resources/alt-icon"
    await app_probe.redraw("Set app icon to alternate")
    app_probe.assert_app_icon("resources/alt-icon")

    # Reset the icon to the default
    app.icon = toga.Icon.APP_ICON
    await app_probe.redraw("Revert app icon to default")
    app_probe.assert_app_icon(None)


async def test_dark_mode_state_read(app, app_probe):
    if app_probe.supports_dark_mode:
        assert isinstance(app.dark_mode, bool)
    else:
        assert isinstance(app.dark_mode, NoneType)
