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


# Mobile platforms have different windowing characterics, so they have different tests.
if toga.platform.current_platform in {"iOS", "android"}:
    ####################################################################################
    # Mobile platform tests
    ####################################################################################

    async def test_show_hide_cursor(app):
        """The app cursor methods can be invoked"""
        # Invoke the methods to verify the endpoints exist. However, they're no-ops,
        # so there's nothing to test.
        app.show_cursor()
        app.hide_cursor()

    async def test_full_screen(app):
        """Window can be made full screen"""
        # Invoke the methods to verify the endpoints exist. However, they're no-ops,
        # so there's nothing to test.
        app.set_full_screen(app.current_window)
        app.exit_full_screen()

    async def test_current_window(app, main_window, main_window_probe):
        """The current window can be retrieved"""
        assert app.current_window == main_window

        # Explicitly set the current window
        app.current_window = main_window
        await main_window_probe.wait_for_window("Main window is still current")
        assert app.current_window == main_window

    async def test_app_lifecycle(app, app_probe):
        """Application lifecycle can be exercised"""
        app_probe.enter_background()
        await app_probe.redraw("App pre-background logic has been invoked")

        app_probe.enter_foreground()
        await app_probe.redraw("App restoration logic has been invoked")

        app_probe.terminate()
        await app_probe.redraw("App pre-termination logic has been invoked")

    async def test_device_rotation(app, app_probe):
        """App responds to device rotation"""
        app_probe.rotate()
        await app_probe.redraw("Device has been rotated")

else:
    ####################################################################################
    # Desktop platform tests
    ####################################################################################

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
            await app_probe.redraw("Window 2 closed")

            assert window2 not in app.windows

            app_probe.activate_menu_close_all_windows()
            await app_probe.redraw("All windows closed")

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
            monkeypatch.setattr(
                app._impl,
                "get_current_window",
                Mock(return_value=None),
            )
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

    async def test_full_screen(app, app_probe):
        """Window can be made full screen"""
        try:
            window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
            window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
            window2 = toga.Window("Test Window 2", position=(400, 150), size=(200, 200))
            window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
            window1_probe = window_probe(app, window1)
            window2_probe = window_probe(app, window2)

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
            await window2_probe.wait_for_window(
                "Second extra window is full screen",
                full_screen=True,
            )
            assert app.is_full_screen

            assert not app_probe.is_full_screen(window1)
            assert app_probe.content_size(window1) == initial_content1_size

            assert app_probe.is_full_screen(window2)
            assert app_probe.content_size(window2)[0] > 1000
            assert app_probe.content_size(window2)[1] > 700

            # Make window 1 full screen via the app, window 2 no longer full screen
            app.set_full_screen(window1)
            await window1_probe.wait_for_window(
                "First extra window is full screen",
                full_screen=True,
            )
            assert app.is_full_screen

            assert app_probe.is_full_screen(window1)
            assert app_probe.content_size(window1)[0] > 1000
            assert app_probe.content_size(window1)[1] > 700

            assert not app_probe.is_full_screen(window2)
            assert app_probe.content_size(window2) == initial_content2_size

            # Exit full screen
            app.exit_full_screen()
            await window1_probe.wait_for_window(
                "No longer full screen",
                full_screen=True,
            )

            assert not app.is_full_screen

            assert not app_probe.is_full_screen(window1)
            assert app_probe.content_size(window1) == initial_content1_size

            assert not app_probe.is_full_screen(window2)
            assert app_probe.content_size(window2) == initial_content2_size

            # Go full screen again on window 1
            app.set_full_screen(window1)
            # A longer delay to allow for genie animations
            await window1_probe.wait_for_window(
                "First extra window is full screen",
                full_screen=True,
            )
            assert app.is_full_screen

            assert app_probe.is_full_screen(window1)
            assert app_probe.content_size(window1)[0] > 1000
            assert app_probe.content_size(window1)[1] > 700

            assert not app_probe.is_full_screen(window2)
            assert app_probe.content_size(window2) == initial_content2_size

            # Exit full screen by passing no windows
            app.set_full_screen()

            await window1_probe.wait_for_window(
                "No longer full screen",
                full_screen=True,
            )
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
        assert app_probe.is_cursor_visible
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

        # Showing again can't make it more visible
        app.show_cursor()
        await app_probe.redraw("Cursor is still visible")
        assert app_probe.is_cursor_visible

    async def test_current_window(app, app_probe, main_window):
        """The current window can be retrieved."""
        try:
            assert app.current_window == main_window

            # When all windows are hidden, WinForms and Cocoa return None, while GTK
            # returns the last active window.
            main_window.hide()
            assert app.current_window in [None, main_window]

            main_window.show()
            assert app.current_window == main_window
        finally:
            main_window.show()

        try:
            window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
            window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
            window2 = toga.Window("Test Window 2", position=(400, 150), size=(200, 200))
            window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
            window3 = toga.Window("Test Window 3", position=(300, 400), size=(200, 200))
            window3.content = toga.Box(style=Pack(background_color=FIREBRICK))

            # We don't need to probe anything window specific; we just need
            # a window probe to enforce appropriate delays.
            window1_probe = window_probe(app, window1)

            window1.show()
            window2.show()
            window3.show()

            await window1_probe.wait_for_window("Extra windows added")

            app.current_window = window2
            await window1_probe.wait_for_window("Window 2 is current")
            assert app.current_window == window2

            app.current_window = window3
            await window1_probe.wait_for_window("Window 3 is current")
            assert app.current_window == window3

            # app_probe.platform tests?
        finally:
            window1.close()
            window2.close()
            window3.close()


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
    # We don't actually want to open a web browser; just check that the interface method
    # was invoked.
    visit_homepage = Mock()
    monkeypatch.setattr(app, "visit_homepage", visit_homepage)

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

    # Dislble the items
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
