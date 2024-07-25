import pytest

import toga
from toga.constants import WindowState

####################################################################################
# Mobile platform tests
####################################################################################
if toga.platform.current_platform not in {"iOS", "android"}:
    pytest.skip("Test is specific to desktop platforms", allow_module_level=True)


async def test_show_hide_cursor(app):
    """The app cursor methods can be invoked"""
    # Invoke the methods to verify the endpoints exist. However, they're no-ops,
    # so there's nothing to test.
    app.show_cursor()
    app.hide_cursor()


async def test_presentation_mode(app, app_probe, main_window, main_window_probe):
    """The app can enter into presentation mode"""
    assert not app.is_presentation_mode
    assert main_window_probe.get_window_state() != WindowState.PRESENTATION

    # Enter presentation mode with main window via the app
    app.enter_presentation_mode([main_window])
    await main_window_probe.wait_for_window(
        "Main window is in presentation mode", full_screen=True
    )

    assert app.is_presentation_mode
    assert main_window_probe.get_window_state() == WindowState.PRESENTATION

    # Exit presentation mode
    app.exit_presentation_mode()
    await main_window_probe.wait_for_window(
        "Main window is no longer in presentation mode",
        full_screen=True,
    )

    assert not app.is_presentation_mode
    assert main_window_probe.get_window_state() == WindowState.NORMAL

    # Enter presentation mode with a screen-window dict via the app
    app.enter_presentation_mode({app.screens[0]: main_window})
    await main_window_probe.wait_for_window(
        "Main window is in presentation mode", full_screen=True
    )

    assert app.is_presentation_mode
    assert main_window_probe.get_window_state() == WindowState.PRESENTATION

    # Exit presentation mode
    app.exit_presentation_mode()
    await main_window_probe.wait_for_window(
        "Main window is no longer in presentation mode",
        full_screen=True,
    )

    assert not app.is_presentation_mode
    assert main_window_probe.get_window_state() == WindowState.NORMAL


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


async def test_session_based_app(app):
    """A mobile app can't be turned into a session-based app"""
    with pytest.raises(
        ValueError,
        match=r"Apps without main windows are not supported on .*",
    ):
        app.main_window = None


async def test_background_app(app):
    """A mobile app can't be turned into a background app"""
    with pytest.raises(
        ValueError,
        match=r"Apps without main windows are not supported on .*",
    ):
        app.main_window = toga.App.BACKGROUND
