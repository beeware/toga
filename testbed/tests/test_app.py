from unittest.mock import Mock

import pytest

import toga
from toga.colors import CORNFLOWERBLUE, FIREBRICK, REBECCAPURPLE
from toga.style.pack import Pack

from .test_window import window_probe


@pytest.fixture
def mock_app_exit(monkeypatch, app):
    # We can't actually exit during a test, so monkeypatch the exit met"""
    app_exit = Mock()
    monkeypatch.setattr(toga.App, "exit", app_exit)
    return app_exit


async def test_exit_on_close_main_window(app, main_window_probe, mock_app_exit):
    """An app can be exited by closing the main window"""
    on_exit_handler = Mock(return_value=False)
    app.on_exit = on_exit_handler

    # Close the main window
    main_window_probe.close()
    await main_window_probe.redraw("Main window close requested, but rejected")

    # on_exit_handler was invoked, rejecting the close; so the app won't be closed
    on_exit_handler.assert_called_once_with(app)
    mock_app_exit.assert_not_called()

    # Reset and try again, this time allowing the exit
    on_exit_handler.reset_mock()
    on_exit_handler.return_value = True
    main_window_probe.close()
    await main_window_probe.redraw("Main window close requested, and accepted")

    # on_exit_handler was invoked and accepted, so the mocked exit() was called.
    on_exit_handler.assert_called_once_with(app)
    mock_app_exit.assert_called_once_with()


async def test_main_window_toolbar(app, main_window, main_window_probe):
    """A toolbar can be added to a main window"""
    action = Mock()

    # A command with everything
    group = toga.Group("Other")
    cmd1 = toga.Command(
        action,
        "Full command",
        icon=toga.Icon.DEFAULT_ICON,
        tooltip="A full command definition",
        shortcut=toga.Key.MOD_1 + "1",
        group=group,
    )
    # A command with everything
    cmd2 = toga.Command(
        action,
        "No Tooltip",
        icon=toga.Icon.DEFAULT_ICON,
        shortcut=toga.Key.MOD_1 + "2",
    )
    # A command without an icon
    cmd3 = toga.Command(
        action,
        "No Icon",
        tooltip="A command with no icon",
        shortcut=toga.Key.MOD_1 + "3",
    )

    main_window.toolbar.add(cmd1, cmd2, cmd3)

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

    # Press the first toolbar button
    main_window_probe.press_toolbar_button(0)
    await main_window_probe.redraw("Command 1 invoked")
    action.assert_called_once_with(cmd1)
    action.reset_mock()

    # Disable the first toolbar button
    cmd1.enabled = False
    await main_window_probe.redraw("Command 1 disabled")
    main_window_probe.assert_toolbar_item(
        0,
        label="Full command",
        tooltip="A full command definition",
        has_icon=True,
        enabled=False,
    )

    # Re-enable the first toolbar button
    cmd1.enabled = True
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


async def test_system_menus(app_probe):
    """System-specific menus behave as expected"""
    # Check that the system menus (which can be platform specific) exist.
    app_probe.assert_system_menus()


async def test_menu_exit(app, app_probe, mock_app_exit):
    """An app can be exited by using the menu item"""
    on_exit_handler = Mock(return_value=False)
    app.on_exit = on_exit_handler

    # Close the main window
    app_probe.activate_menu_exit()
    await app_probe.redraw("Exit selected from menu, but rejected")

    # on_exit_handler was invoked, rejecting the close; so the app won't be closed
    on_exit_handler.assert_called_once_with(app)
    mock_app_exit.assert_not_called()

    # Reset and try again, this time allowing the exit
    on_exit_handler.reset_mock()
    on_exit_handler.return_value = True
    app_probe.activate_menu_exit()
    await app_probe.redraw("Exit selected from menu, and accepted")

    # on_exit_handler was invoked and accepted, so the mocked exit() was called.
    on_exit_handler.assert_called_once_with(app)
    mock_app_exit.assert_called_once_with()


async def test_menu_about(monkeypatch, app, app_probe):
    """The about menu can be displayed"""
    app_probe.activate_menu_about()
    await app_probe.redraw("About dialog shown")

    app_probe.close_about_dialog()
    await app_probe.redraw("About dialog destroyed")

    # Make the app definition minimal to verify the dialog still displays
    monkeypatch.setattr(app, "_author", None)
    monkeypatch.setattr(app, "_version", None)

    app_probe.activate_menu_about()
    await app_probe.redraw("About dialog with no details shown")

    app_probe.close_about_dialog()
    await app_probe.redraw("About dialog with no details destroyed")


async def test_menu_visit_homepage(monkeypatch, app, app_probe):
    """The visit homepage menu item can be used"""
    # We don't actually want to open a web browser; just check that the interface method
    # was invoked.
    visit_homepage = Mock()
    monkeypatch.setattr(app, "visit_homepage", visit_homepage)

    app_probe.activate_menu_visit_homepage()

    # Browser opened
    visit_homepage.assert_called_once()


async def test_menu_items(app, app_probe):
    """Menu items can be created, disabled and invoked"""
    action = Mock()

    # A command with everything
    group = toga.Group("Other")
    cmd1 = toga.Command(
        action,
        "Full command",
        icon=toga.Icon.DEFAULT_ICON,
        tooltip="A full command definition",
        shortcut=toga.Key.MOD_1 + "1",
        group=group,
    )
    # A command with everything
    cmd2 = toga.Command(
        action,
        "No Tooltip",
        icon=toga.Icon.DEFAULT_ICON,
        shortcut=toga.Key.MOD_1 + "2",
    )
    # A command without an icon
    cmd3 = toga.Command(
        action,
        "No Icon",
        tooltip="A command with no icon",
        shortcut=toga.Key.MOD_1 + "3",
    )
    # Submenus inside the "other" group
    subgroup1 = toga.Group("Submenu1", section=2, parent=group)
    subgroup1_1 = toga.Group("Submenu1 menu1", parent=subgroup1)
    subgroup2 = toga.Group("Submenu2", section=2, parent=group)

    # Items on submenu1
    # An item that is disabled by default
    disabled_item = toga.Command(action, "Disabled", enabled=False, group=subgroup1)
    # An item that has no action
    no_action = toga.Command(None, "No Action", group=subgroup1)
    # An item deep in a menu
    deep_item = toga.Command(action, "Deep", group=subgroup1_1)

    # Items on submenu2
    cmd4 = toga.Command(action, "Jiggle", group=subgroup2)

    # Add all the commands
    app.commands.add(cmd1, cmd2, cmd3, disabled_item, no_action, deep_item, cmd4)

    app_probe.redraw("App has custom menu items")

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

    # Enabled the disabled items
    disabled_item.enabled = True
    no_action.enabled = True
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

    disabled_item.enabled = False
    no_action.enabled = False
    await app_probe.redraw("Menu item disabled again")
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Disabled"],
        enabled=False,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "No Action"],
        enabled=False,
    )


async def test_menu_close_windows(monkeypatch, app, app_probe, mock_app_exit):
    try:
        window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
        window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
        window2 = toga.Window("Test Window 2", position=(400, 150), size=(200, 200))
        window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        window3 = toga.Window("Test Window 3", position=(300, 400), size=(200, 200))
        window3.content = toga.Box(style=Pack(background_color=FIREBRICK))

        window1.show()
        window2.show()
        window3.show()

        app.current_window = window2

        await app_probe.redraw("Extra windows added")

        app_probe.activate_menu_close_window()
        assert window2 not in app.windows

        await app_probe.redraw("Window 2 closed")

        app_probe.activate_menu_close_all_windows()

        # Close all windows will attempt to close the main window as well.
        # This would be an app exit, but we can't allow that; so, the only
        # window that *actually* remains will be the main window.
        mock_app_exit.assert_called_once_with()
        assert window1 not in app.windows
        assert window2 not in app.windows
        assert window3 not in app.windows

        await app_probe.redraw("Extra windows closed")

        # Now that we've "closed" all the windows, we're in a state where there
        # aren't any windows. Patch get_current_window to reflect this.
        monkeypatch.setattr(app._impl, "get_current_window", Mock(return_value=None))
        app_probe.activate_menu_close_window()
        await app_probe.redraw("No windows; Close Window is a no-op")

        app_probe.activate_menu_minimize()
        await app_probe.redraw("No windows; Minimize is a no-op")

    finally:
        if window1 in app.windows:
            window1.close()
        if window2 in app.windows:
            window2.close()
        if window3 in app.windows:
            window3.close()


async def test_menu_minimize(app, app_probe):
    try:
        window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
        window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
        window1.show()

        window1_probe = window_probe(app, window1)

        app.current_window = window1
        await app_probe.redraw("Extra window added")

        app_probe.activate_menu_minimize()

        await window1_probe.wait_for_window("Extra window minimized", minimize=True)
        assert window1_probe.is_minimized
    finally:
        window1.close()


async def test_beep(app):
    """The machine can go Bing!"""
    # This isn't a very good test. It ensures coverage, which verifies that the method
    # can be invoked without raising an error, but there's no way to verify that the app
    # actually made a noise.
    app.beep()


async def test_current_window(app, app_probe):
    """The current window can be retrieved."""
    try:
        window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
        window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
        window2 = toga.Window("Test Window 2", position=(400, 150), size=(200, 200))
        window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        window3 = toga.Window("Test Window 3", position=(300, 400), size=(200, 200))
        window3.content = toga.Box(style=Pack(background_color=FIREBRICK))

        window1.show()
        window2.show()
        window3.show()

        await app_probe.redraw("Extra windows added")

        app.current_window = window2
        await app_probe.redraw("Window 2 is current")
        assert app.current_window == window2

        app.current_window = window3
        await app_probe.redraw("Window 3 is current")
        assert app.current_window == window3

        # app_probe.platform tests?
    finally:
        window1.close()
        window2.close()
        window3.close()


async def test_full_screen(app, app_probe):
    """Window can be made full screen"""
    try:
        window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
        window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
        window2 = toga.Window("Test Window 2", position=(400, 150), size=(200, 200))
        window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))

        window1.show()
        window2.show()
        await app_probe.redraw("Extra windows are visible")

        assert not app.is_full_screen
        assert not app_probe.is_full_screen(window1)
        assert not app_probe.is_full_screen(window2)
        initial_content1_size = app_probe.content_size(window1)
        initial_content2_size = app_probe.content_size(window2)

        # Make window 2 full screen via the app
        app.set_full_screen(window2)
        await app_probe.redraw("Second extra window is full screen")
        assert app.is_full_screen

        assert not app_probe.is_full_screen(window1)
        assert app_probe.content_size(window1) == initial_content1_size

        assert app_probe.is_full_screen(window2)
        assert app_probe.content_size(window2)[0] > 1000
        assert app_probe.content_size(window2)[1] > 1000

        # Make window 1 full screen via the app, window 2 no longer full screen
        app.set_full_screen(window1)
        # A longer delay to allow for genie animations
        await app_probe.redraw("First extra window is full screen")
        assert app.is_full_screen

        assert app_probe.is_full_screen(window1)
        assert app_probe.content_size(window1)[0] > 1000
        assert app_probe.content_size(window1)[1] > 1000

        assert not app_probe.is_full_screen(window2)
        assert app_probe.content_size(window2) == initial_content2_size

        # Exit full screen
        app.exit_full_screen()
        await app_probe.redraw("No longer full screen", delay=0.1)

        assert not app.is_full_screen

        assert not app_probe.is_full_screen(window1)
        assert app_probe.content_size(window1) == initial_content1_size

        assert not app_probe.is_full_screen(window2)
        assert app_probe.content_size(window2) == initial_content2_size

        # Go full screen again on window 1
        app.set_full_screen(window1)
        # A longer delay to allow for genie animations
        await app_probe.redraw("First extra window is full screen", delay=0.1)
        assert app.is_full_screen

        assert app_probe.is_full_screen(window1)
        assert app_probe.content_size(window1)[0] > 1000
        assert app_probe.content_size(window1)[1] > 1000

        assert not app_probe.is_full_screen(window2)
        assert app_probe.content_size(window2) == initial_content2_size

        # Exit full screen by passing no windows
        app.set_full_screen()

        await app_probe.redraw("App no longer full screen", delay=0.1)
        assert not app.is_full_screen

        assert not app_probe.is_full_screen(window1)
        assert app_probe.content_size(window1) == initial_content1_size

        assert not app_probe.is_full_screen(window2)
        assert app_probe.content_size(window2) == initial_content2_size

    finally:
        window1.close()
        window2.close()


async def test_show_hide_cursor(app, app_probe):
    """The app cursor can be hidden and shown"""
    app.hide_cursor()
    await app_probe.redraw("Cursor is hidden")
    assert not app_probe.is_cursor_visible

    # Hiding again can't make it more hidden
    app.hide_cursor()
    await app_probe.redraw("Cursor is still hidden")
    assert not app_probe.is_cursor_visible

    # Show the cursor again
    app.show_cursor()
    await app_probe.redraw("Cursor is visible")
    assert app_probe.is_cursor_visible

    # Hiding again can't make it more hidden
    app.show_cursor()
    await app_probe.redraw("Cursor is still visible")
    assert app_probe.is_cursor_visible
