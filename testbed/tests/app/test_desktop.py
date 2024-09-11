import random
from unittest.mock import Mock

import pytest

import toga
from toga.colors import CORNFLOWERBLUE, FIREBRICK, REBECCAPURPLE
from toga.constants import WindowState
from toga.style.pack import Pack

from ..widgets.probe import get_probe
from ..window.test_window import window_probe

####################################################################################
# Desktop platform tests
####################################################################################
if toga.platform.current_platform not in {"macOS", "windows", "linux"}:
    pytest.skip("Test is specific to desktop platforms", allow_module_level=True)


async def test_exit_on_close_main_window(
    monkeypatch,
    app,
    main_window,
    main_window_probe,
    mock_app_exit,
):
    """An app can be exited by closing the main window"""
    # Add an on_close handler to the main window, initially rejecting close.
    on_close_handler = Mock(return_value=False)
    main_window.on_close = on_close_handler

    # Set an on_exit for the app handler, initially rejecting exit.
    on_exit_handler = Mock(return_value=False)
    monkeypatch.setattr(app, "on_exit", on_exit_handler)

    # Try to close the main window; rejected by window
    main_window_probe.close()
    await main_window_probe.redraw("Main window close requested; rejected by window")

    # on_close_handler was invoked, rejecting the close.
    on_close_handler.assert_called_once_with(main_window)

    # on_exit_handler was not invoked; so the app won't be closed
    on_exit_handler.assert_not_called()
    mock_app_exit.assert_not_called()

    # Reset and try again, this time allowing the close
    on_close_handler.reset_mock()
    on_close_handler.return_value = True
    on_exit_handler.reset_mock()

    # Close the main window; rejected by app
    main_window_probe.close()
    await main_window_probe.redraw("Main window close requested; rejected by app")

    # on_close_handler was invoked, allowing the close
    on_close_handler.assert_called_once_with(main_window)

    # on_exit_handler was invoked, rejecting the close; so the app won't be closed
    on_exit_handler.assert_called_once_with(app)
    mock_app_exit.assert_not_called()

    # Reset and try again, this time allowing the exit
    on_close_handler.reset_mock()
    on_exit_handler.reset_mock()
    on_exit_handler.return_value = True

    # Close the main window; this will succeed
    main_window_probe.close()
    await main_window_probe.redraw("Main window close requested; accepted")

    # on_close_handler was invoked, allowing the close
    on_close_handler.assert_called_once_with(main_window)

    # on_exit_handler was invoked and accepted, so the mocked exit() was called.
    on_exit_handler.assert_called_once_with(app)
    mock_app_exit.assert_called_once_with()


async def test_menu_exit(monkeypatch, app, app_probe, mock_app_exit):
    """An app can be exited by using the menu item"""
    # Rebind the exit command to the on_exit handler.
    on_exit_handler = Mock(return_value=False)
    monkeypatch.setattr(app, "on_exit", on_exit_handler)

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
    """Windows can be closed by a menu item"""
    window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
    window2 = toga.Window("Test Window 2", position=(400, 150), size=(200, 200))
    window3 = toga.Window("Test Window 3", position=(300, 400), size=(200, 200))

    window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
    window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
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


async def test_menu_minimize(app, app_probe):
    """Windows can be minimized by a menu item"""
    window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
    window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
    window1.show()

    window1_probe = window_probe(app, window1)

    app.current_window = window1
    await app_probe.redraw("Extra window added")

    app_probe.activate_menu_minimize()

    await window1_probe.wait_for_window("Extra window minimized", minimize=True)
    assert window1_probe.is_minimized


async def test_presentation_mode(app, app_probe, main_window, main_window_probe):
    """The app can enter presentation mode."""
    try:
        window_information_list = list()
        windows_list = list()
        for i in range(len(app.screens)):
            window = toga.Window(
                title=f"Test Window {i}",
                position=(150 + (10 * i), 150 + (10 * i)),
                size=(200, 200),
            )
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            window_widget = toga.Box(style=Pack(flex=1))
            window.content = toga.Box(
                children=[window_widget],
                style=Pack(background_color=f"#{r:02X}{g:02X}{b:02X}"),
            )
            window.show()
            # Add delay to ensure windows are visible after animation.
            await app_probe.redraw(f"Test Window {i} is visible", delay=0.5)

            window_information = dict()
            window_information["window"] = window
            window_information["window_probe"] = window_probe(app, window)
            window_information["initial_content_size"] = window_information[
                "window_probe"
            ].presentation_content_size
            window_information["widget_probe"] = get_probe(window_widget)
            window_information["initial_widget_size"] = (
                window_information["widget_probe"].width,
                window_information["widget_probe"].height,
            )
            window_information_list.append(window_information)
            windows_list.append(window)

        screen_window_dict = dict()
        for window, screen in zip(windows_list, app.screens):
            screen_window_dict[screen] = window

        # Enter presentation mode with a screen-window dict via the app
        app.enter_presentation_mode(screen_window_dict)
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw("App is in presentation mode", delay=0.5)

        assert app.in_presentation_mode
        # All the windows should be in presentation mode.
        for window_information in window_information_list:
            assert (
                window_information["window"].state == WindowState.PRESENTATION
            ), f"{window_information['window'].title}:"
            assert (
                window_information["window_probe"].presentation_content_size[0] > 1000
            ), f"{window_information['window'].title}:"
            assert (
                window_information["window_probe"].presentation_content_size[1] > 700
            ), f"{window_information['window'].title}:"
            assert (
                window_information["widget_probe"].width
                > window_information["initial_widget_size"][0]
                and window_information["widget_probe"].height
                > window_information["initial_widget_size"][1]
            ), f"{window_information['window'].title}:"

        # Exit presentation mode
        app.exit_presentation_mode()
        await app_probe.redraw("App is no longer in presentation mode", delay=0.5)

        assert not app.in_presentation_mode
        for window_information in window_information_list:
            assert (
                window_information["window"].state == WindowState.NORMAL
            ), f"{window_information['window'].title}:"
            assert (
                window_information["window_probe"].presentation_content_size
                == window_information["initial_content_size"]
            ), f"{window_information['window'].title}:"
            assert (
                window_information["widget_probe"].width
                == window_information["initial_widget_size"][0]
                and window_information["widget_probe"].height
                == window_information["initial_widget_size"][1]
            ), f"{window_information['window'].title}:"

    finally:
        for window in windows_list:
            window.close()
        # After closing the window, the input focus might not be on main_window.
        # Ensure that main_window will be in focus for other tests.
        app.current_window = main_window
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw("main_window is now the current window", delay=0.5)
        assert app.current_window == main_window


@pytest.mark.parametrize(
    "new_window_state",
    [
        WindowState.MINIMIZED,
        WindowState.MAXIMIZED,
        WindowState.FULLSCREEN,
    ],
)
async def test_presentation_mode_exit_on_window_state_change(
    app, app_probe, main_window, main_window_probe, new_window_state
):
    """Changing window state exits presentation mode and sets the new state."""
    if not main_window_probe.supports_minimize:
        pytest.xfail("This backend doesn't reliably support WindowState.MINIMIZED.")

    try:
        window1 = toga.Window(
            title="Test Window 1", position=(150, 150), size=(200, 200)
        )
        window2 = toga.Window(
            title="Test Window 2", position=(160, 160), size=(200, 200)
        )
        window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
        window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        window1.show()
        window2.show()
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw("Test windows are shown", delay=0.5)

        # Enter presentation mode
        app.enter_presentation_mode([window1])
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw("App is in presentation mode", delay=0.5)

        assert app.in_presentation_mode
        assert window1.state == WindowState.PRESENTATION

        # Changing window state of main window should make the app exit presentation mode.
        window1.state = new_window_state
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw(
            "App is not in presentation mode"
            f"\nTest Window 1 is in {new_window_state}",
            delay=0.5,
        )

        assert not app.in_presentation_mode
        assert window1.state == new_window_state

        # Reset window states
        window1.state = WindowState.NORMAL
        window2.state = WindowState.NORMAL
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw("All test windows are in WindowState.NORMAL", delay=1)

        # Enter presentation mode again
        app.enter_presentation_mode([window1])
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw("App is in presentation mode", delay=0.5)
        assert app.in_presentation_mode
        assert window1.state == WindowState.PRESENTATION

        # Changing window state of extra window should make the app exit presentation mode.
        window2.state = new_window_state
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw(
            "App is not in presentation mode"
            f"\nTest Window 1 is in {new_window_state}",
            delay=0.5,
        )

        assert not app.in_presentation_mode
        assert window2.state == new_window_state

        # Reset window states
        window1.state = WindowState.NORMAL
        window2.state = WindowState.NORMAL
        # Add delay for gtk to show the windows
        await app_probe.redraw("All test windows are in WindowState.NORMAL", delay=0.5)

    finally:
        window1.close()
        window2.close()
        # After closing the window, the input focus might not be on main_window.
        # Ensure that main_window will be in focus for other tests.
        app.current_window = main_window
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw("main_window is now the current window", delay=0.5)
        assert app.current_window == main_window


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
    """The current window can be retrieved"""
    try:
        if app_probe.supports_current_window_assignment:
            assert app.current_window == main_window

        # When all windows are hidden, WinForms and Cocoa return None, while GTK
        # returns the last active window.
        main_window.hide()
        assert app.current_window in [None, main_window]

        main_window.show()
        assert app.current_window == main_window
    finally:
        main_window.show()

    window1 = toga.Window("Test Window 1", position=(150, 150), size=(200, 200))
    window2 = toga.Window("Test Window 2", position=(400, 150), size=(200, 200))
    window3 = toga.Window("Test Window 3", position=(300, 400), size=(200, 200))

    window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
    window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
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
    if app_probe.supports_current_window_assignment:
        assert app.current_window == window2

    app.current_window = window3
    await window1_probe.wait_for_window("Window 3 is current")
    if app_probe.supports_current_window_assignment:
        assert app.current_window == window3


async def test_session_based_app(
    monkeypatch,
    app,
    app_probe,
    main_window,
    mock_app_exit,
    mock_main_window_close,
):
    """A desktop app can be converted into a session-based app."""
    # Set an on_exit for the app handler, allowing exit.
    on_exit_handler = Mock(return_value=True)
    monkeypatch.setattr(app, "on_exit", on_exit_handler)

    # Create and show a secondary window
    secondary_window = toga.Window()
    secondary_window.show()

    try:
        # Change the app to a session-based app
        app.main_window = None
        await app_probe.redraw("App converted to session-based app")

        # Try to close the main window. This is monkeypatched, so it
        # will record whether a close was allowed, but won't actually
        # close or remove the window, so the window will still exist.
        main_window.close()
        await app_probe.redraw("Simulate close of main window; app should not exit")

        # The main window will be closed
        mock_main_window_close.assert_called_once()
        mock_main_window_close.reset_mock()

        # The app will *not* have been prompted to exit, because there
        # is still an open window, and this is a session-based app.
        on_exit_handler.assert_not_called()
        on_exit_handler.reset_mock()

        # Close the secondary window.
        secondary_window.close()
        secondary_window = None
        await app_probe.redraw("Secondary window has been closed")

        # Try to close the main window again. This time, the main
        # window is the last open window; the backend's session behavior
        # defines whether the app exits.
        main_window.close()
        if app._impl.CLOSE_ON_LAST_WINDOW:
            await app_probe.redraw("Simulate close of main window; app should exit")

            # The platform closes the session on the last window close.
            # Exit should have been called.
            on_exit_handler.assert_called_once()

            # Main window will not be closed, because that will be
            # superseded by the app exiting.
            mock_main_window_close.assert_not_called()
        else:
            await app_probe.redraw("Simulate close of main window; app should not exit")

            # The platform persists the app when the last window closes.
            # Exit should *not* have been called.
            on_exit_handler.assert_not_called()

            # However, the the main window will be closed
            mock_main_window_close.assert_called_once()

    finally:
        app.main_window = main_window
        await app_probe.restore_standard_app()


async def test_background_app(
    monkeypatch,
    app,
    app_probe,
    main_window,
    mock_app_exit,
    mock_main_window_close,
):
    """A desktop app can be turned into a background app."""
    # Set an on_exit for the app handler, allowing exit.
    on_exit_handler = Mock(return_value=True)
    monkeypatch.setattr(app, "on_exit", on_exit_handler)

    # Create and show a secondary window
    secondary_window = toga.Window()
    secondary_window.show()

    try:
        # Change the app to a background app
        app.main_window = toga.App.BACKGROUND
        await app_probe.redraw("App converted to background app")

        # Try to close the main window. This is monkeypatched, so it
        # will record whether a close was allowed, but won't actually
        # close or remove the window, so the window will still exist.
        main_window.close()
        await app_probe.redraw("Simulate close of main window; app should not exit")

        # The main window will be closed
        mock_main_window_close.assert_called_once()
        mock_main_window_close.reset_mock()

        # The app will *not* have been prompted to exit, because this is a
        # background app, which can exist without windows.
        on_exit_handler.assert_not_called()
        on_exit_handler.reset_mock()

        # Close the secondary window.
        secondary_window.close()
        secondary_window = None
        await app_probe.redraw("Secondary window has been closed")

        # Try to close the main window again. This time, the main window is the last
        # open window; but the app will persist because this is a background app,
        # which doesn't need a window to exist.
        main_window.close()
        await app_probe.redraw("Simulate close of main window; app should not exit")

        # The platform persists the app when the last window closes.
        # Exit should *not* have been called.
        on_exit_handler.assert_not_called()

        # Regardless, the main window will be closed
        mock_main_window_close.assert_called_once()

    finally:
        app.main_window = main_window
        await app_probe.restore_standard_app()
