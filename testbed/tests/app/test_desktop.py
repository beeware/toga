import itertools
from functools import partial
from unittest.mock import Mock

import pytest

import toga
from toga import Position, Size
from toga.colors import CORNFLOWERBLUE, FIREBRICK, GOLDENROD, REBECCAPURPLE
from toga.constants import WindowState
from toga.style.pack import Pack

from ..assertions import assert_window_on_hide, assert_window_on_show
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
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        "Extra window minimized", state=WindowState.MINIMIZED
    )
    assert window1_probe.is_minimized


async def test_app_level_menu_hide(app, app_probe, main_window, main_window_probe):
    """The app can be hidden from the global app menu option, thereby hiding all
    the windows of the app."""
    initially_visible_window = toga.Window(
        title="Initially Visible Window",
        size=(200, 200),
        content=toga.Box(style=Pack(background_color=CORNFLOWERBLUE)),
    )
    initially_visible_window.show()

    initially_hidden_window = toga.Window(
        title="Initially Hidden Window",
        size=(200, 200),
        content=toga.Box(style=Pack(background_color=REBECCAPURPLE)),
    )
    initially_hidden_window.hide()

    initially_minimized_window = toga.Window(
        title="Initially Minimized Window",
        size=(200, 200),
        content=toga.Box(style=Pack(background_color=GOLDENROD)),
    )
    initially_minimized_window.show()
    initially_minimized_window.state = WindowState.MINIMIZED

    await window_probe(app, initially_minimized_window).wait_for_window(
        "Test windows have been setup", state=WindowState.MINIMIZED
    )

    # Setup event mocks after test windows' setup to prevent false positive triggering.
    initially_visible_window.on_show = Mock()
    initially_visible_window.on_hide = Mock()

    initially_hidden_window.on_show = Mock()
    initially_hidden_window.on_hide = Mock()

    initially_minimized_window.on_show = Mock()
    initially_minimized_window.on_hide = Mock()

    # Confirm the initial window state
    assert initially_visible_window.visible
    assert not initially_hidden_window.visible
    assert initially_minimized_window.visible

    # Test using the "Hide" option from the global app menu.
    app_probe.activate_menu_hide()
    await main_window_probe.wait_for_window("Hide selected from menu, and accepted")
    assert not initially_visible_window.visible
    assert not initially_hidden_window.visible
    assert not initially_minimized_window.visible

    assert_window_on_hide(initially_visible_window)
    assert_window_on_hide(initially_hidden_window, trigger_expected=False)
    assert_window_on_hide(initially_minimized_window, trigger_expected=False)

    # Make the app visible again
    app_probe.unhide()
    await main_window_probe.wait_for_window("App level unhide has been activated")
    assert initially_visible_window.visible
    assert not initially_hidden_window.visible
    assert initially_minimized_window.visible

    assert_window_on_show(initially_visible_window)
    assert_window_on_show(initially_hidden_window, trigger_expected=False)
    assert_window_on_show(initially_minimized_window, trigger_expected=False)


async def test_presentation_mode(app, app_probe, main_window, main_window_probe):
    """The app can enter presentation mode."""
    bg_colors = (CORNFLOWERBLUE, FIREBRICK, REBECCAPURPLE, GOLDENROD)
    color_cycle = itertools.cycle(bg_colors)
    window_information_list = []
    screen_window_dict = {}
    for i in range(len(app.screens)):
        window = toga.Window(title=f"Test Window {i}", size=(200, 200))
        window_widget = toga.Box(style=Pack(flex=1, background_color=next(color_cycle)))
        window.content = window_widget
        window.show()

        window_information = {}
        window_information["window"] = window
        window_information["window_probe"] = window_probe(app, window)
        window_information["initial_screen"] = window_information["window"].screen
        window_information["paired_screen"] = app.screens[i]
        window_information["initial_content_size"] = window_information[
            "window_probe"
        ].content_size
        window_information["widget_probe"] = get_probe(window_widget)
        window_information["initial_widget_size"] = (
            window_information["widget_probe"].width,
            window_information["widget_probe"].height,
        )
        window_information_list.append(window_information)
        screen_window_dict[window_information["paired_screen"]] = window_information[
            "window"
        ]
    # Wait for window animation before assertion.
    await main_window_probe.wait_for_window("All Test Windows are visible")

    # Enter presentation mode with a screen-window dict via the app
    app.enter_presentation_mode(screen_window_dict)
    # Add delay to ensure windows are visible after animation.
    await main_window_probe.wait_for_window("App is in presentation mode")
    # All the windows should be in presentation mode.
    for window_information in window_information_list:
        # Wait for window animation before assertion.
        await window_information["window_probe"].wait_for_window(
            "App is in presentation mode", state=WindowState.PRESENTATION
        )
        assert (
            window_information["window_probe"].instantaneous_state
            == WindowState.PRESENTATION
        ), f"{window_information['window'].title}:"
        # 1000x700 is bigger than the original window size,
        # while being smaller than any likely screen.
        assert window_information["window_probe"].content_size[0] > 1000, (
            f"{window_information['window'].title}:"
        )
        assert window_information["window_probe"].content_size[1] > 700, (
            f"{window_information['window'].title}:"
        )
        assert (
            window_information["widget_probe"].width
            > window_information["initial_widget_size"][0]
            and window_information["widget_probe"].height
            > window_information["initial_widget_size"][1]
        ), f"{window_information['window'].title}:"
        assert (
            window_information["window"].screen == window_information["paired_screen"]
        ), f"{window_information['window'].title}:"

    assert app.in_presentation_mode

    # Exit presentation mode
    app.exit_presentation_mode()

    # All the windows should have exited presentation mode.
    for window_information in window_information_list:
        # Wait for window animation before assertion.
        await window_information["window_probe"].wait_for_window(
            "App is not in presentation mode", state=WindowState.NORMAL
        )
        assert not app.in_presentation_mode
        assert (
            window_information["window_probe"].instantaneous_state == WindowState.NORMAL
        ), f"{window_information['window'].title}:"
        assert (
            window_information["window_probe"].content_size
            == window_information["initial_content_size"]
        ), f"{window_information['window'].title}:"
        assert (
            window_information["widget_probe"].width
            == window_information["initial_widget_size"][0]
            and window_information["widget_probe"].height
            == window_information["initial_widget_size"][1]
        ), f"{window_information['window'].title}:"
        assert (
            window_information["window"].screen == window_information["initial_screen"]
        ), f"{window_information['window'].title}:"


async def test_window_presentation_exit_on_another_window_presentation(
    app, main_window_probe
):
    window1 = toga.Window(title="Test Window 1", size=(200, 200))
    window2 = toga.Window(title="Test Window 2", size=(200, 200))
    window1_probe = window_probe(app, window1)
    window2_probe = window_probe(app, window2)
    window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
    window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
    window1.show()
    window2.show()
    # Wait for window animation before assertion.
    await main_window_probe.wait_for_window("Test windows are shown")

    assert not app.in_presentation_mode
    assert window1_probe.instantaneous_state != WindowState.PRESENTATION
    assert window2_probe.instantaneous_state != WindowState.PRESENTATION

    # Enter presentation mode with window2
    app.enter_presentation_mode([window2])
    # Wait for window animation before assertion.
    await window2_probe.wait_for_window(
        "App is in presentation mode", state=WindowState.PRESENTATION
    )
    assert app.in_presentation_mode
    assert window2_probe.instantaneous_state == WindowState.PRESENTATION
    assert window1_probe.instantaneous_state != WindowState.PRESENTATION

    # Enter presentation mode with window1, window2 no longer in presentation
    app.enter_presentation_mode([window1])
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        "App is in presentation mode", state=WindowState.PRESENTATION
    )
    assert app.in_presentation_mode
    assert window1_probe.instantaneous_state == WindowState.PRESENTATION
    assert window2_probe.instantaneous_state != WindowState.PRESENTATION

    # Exit presentation mode
    app.exit_presentation_mode()
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        "App is not in presentation mode", state=WindowState.NORMAL
    )
    assert not app.in_presentation_mode
    assert window1_probe.instantaneous_state != WindowState.PRESENTATION
    assert window2_probe.instantaneous_state != WindowState.PRESENTATION

    # Enter presentation mode again with window1
    app.enter_presentation_mode([window1])
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        "App is in presentation mode", state=WindowState.PRESENTATION
    )
    assert app.in_presentation_mode
    assert window1_probe.instantaneous_state == WindowState.PRESENTATION
    assert window2_probe.instantaneous_state != WindowState.PRESENTATION

    # Exit presentation mode
    app.exit_presentation_mode()
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        "App is not in presentation mode", state=WindowState.NORMAL
    )
    assert not app.in_presentation_mode
    assert window1_probe.instantaneous_state != WindowState.PRESENTATION
    assert window2_probe.instantaneous_state != WindowState.PRESENTATION


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
    if (new_window_state == WindowState.MINIMIZED) and (
        not main_window_probe.supports_minimize
    ):
        pytest.xfail("This backend doesn't reliably support WindowState.MINIMIZED.")

    window1 = toga.Window(title="Test Window 1", size=(200, 200))
    window2 = toga.Window(title="Test Window 2", size=(200, 200))
    window1_probe = window_probe(app, window1)
    window2_probe = window_probe(app, window2)
    window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
    window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
    window1.show()
    window2.show()
    # Wait for window animation before assertion.
    await main_window_probe.wait_for_window("Test windows are shown")

    # Enter presentation mode
    app.enter_presentation_mode([window1])
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        "App is in presentation mode", state=WindowState.PRESENTATION
    )

    assert app.in_presentation_mode
    assert window1_probe.instantaneous_state == WindowState.PRESENTATION

    # Changing window state of main window should make the app exit presentation mode.
    window1.state = new_window_state
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        f"App is not in presentation mode\nTest Window 1 is in {new_window_state}",
        state=new_window_state,
    )

    assert not app.in_presentation_mode
    assert window1_probe.instantaneous_state == new_window_state

    # Reset window states
    window1.state = WindowState.NORMAL
    window2.state = WindowState.NORMAL
    # Wait for windows animation before assertion.
    await window1_probe.wait_for_window(
        "All test windows are in WindowState.NORMAL", state=WindowState.NORMAL
    )
    await window2_probe.wait_for_window(
        "All test windows are in WindowState.NORMAL", state=WindowState.NORMAL
    )
    assert window1_probe.instantaneous_state == WindowState.NORMAL
    assert window2_probe.instantaneous_state == WindowState.NORMAL

    # Enter presentation mode again
    app.enter_presentation_mode([window1])
    # Wait for window animation before assertion.
    await window1_probe.wait_for_window(
        "App is in presentation mode", state=WindowState.PRESENTATION
    )
    assert app.in_presentation_mode
    assert window1_probe.instantaneous_state == WindowState.PRESENTATION

    # Changing window state of extra window should make the app exit presentation mode.
    window2.state = new_window_state
    # Wait for window animation before assertion.
    await window2_probe.wait_for_window(
        f"App is not in presentation mode\nTest Window 2 is in {new_window_state}",
        state=new_window_state,
    )

    assert not app.in_presentation_mode
    assert window2_probe.instantaneous_state == new_window_state

    # Reset window states
    window1.state = WindowState.NORMAL
    window2.state = WindowState.NORMAL
    # Wait for windows animation before assertion.
    await window1_probe.wait_for_window(
        "All test windows are in WindowState.NORMAL", state=WindowState.NORMAL
    )
    await window2_probe.wait_for_window(
        "All test windows are in WindowState.NORMAL", state=WindowState.NORMAL
    )
    assert window1_probe.instantaneous_state == WindowState.NORMAL
    assert window2_probe.instantaneous_state == WindowState.NORMAL


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


async def test_current_window(app, app_probe, main_window, main_window_probe):
    """The current window can be retrieved"""
    try:
        if app_probe.supports_current_window_assignment:
            assert app.current_window == main_window

        main_window.hide()
        await main_window_probe.wait_for_window("Hiding main window")
        assert app.current_window is None

        main_window.show()
        await main_window_probe.wait_for_window("Showing main window")
        assert app.current_window == main_window
    finally:
        main_window.show()

    window1 = toga.Window(title="Test Window 1", position=(150, 150), size=(200, 200))
    window2 = toga.Window(title="Test Window 2", position=(400, 150), size=(200, 200))
    window3 = toga.Window(title="Test Window 3", position=(300, 400), size=(200, 200))

    window1.content = toga.Box(style=Pack(background_color=REBECCAPURPLE))
    window2.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
    window3.content = toga.Box(style=Pack(background_color=FIREBRICK))

    window1.show()
    window2.show()
    window3.show()

    await main_window_probe.wait_for_window("Extra windows added")

    # When a window without any dialog is made the current_window,
    # then `app.current_window` should return the specified window.
    app.current_window = window2
    await main_window_probe.wait_for_window("Window 2 is current")
    if app_probe.supports_current_window_assignment:
        assert app.current_window == window2

    app.current_window = window3
    await main_window_probe.wait_for_window("Window 3 is current")
    if app_probe.supports_current_window_assignment:
        assert app.current_window == window3

    # When a dialog is in focus, app.current_window should return the
    # previously active window.
    def test_current_window_in_presence_of_dialog(dialog):
        app_probe.assert_dialog_in_focus(dialog)

        # Accessing current_window in presence of dialog shouldn't raise any exceptions.
        _ = app.current_window

    # Test in presence of window modal dialog
    window_modal_info_dialog = toga.InfoDialog("Window Modal Dialog Info", "Some info")
    main_window_probe.setup_info_dialog_result(
        window_modal_info_dialog,
        pre_close_test_method=test_current_window_in_presence_of_dialog,
    )
    await main_window_probe.wait_for_window("Display window1 modal info dialog")
    await window1.dialog(window_modal_info_dialog)

    # Test in presence of app modal dialog
    app_modal_info_dialog = toga.InfoDialog("App Modal Dialog Info", "Some info")
    app_probe.setup_info_dialog_result(
        app_modal_info_dialog,
        pre_close_test_method=test_current_window_in_presence_of_dialog,
    )
    await main_window_probe.wait_for_window("Display app modal info dialog")
    await app.dialog(app_modal_info_dialog)


@pytest.mark.parametrize(
    "event_path",
    [
        "SystemEvents.DisplaySettingsChanged",
        "Form.LocationChanged",
        "Form.Resize",
    ],
)
@pytest.mark.parametrize("mock_scale", [1.0, 1.25, 1.5, 1.75, 2.0])
async def test_system_dpi_change(
    main_window, main_window_probe, event_path, mock_scale
):
    if toga.platform.current_platform != "windows":
        pytest.xfail("This test is winforms backend specific")

    from toga_winforms.libs import shcore

    real_scale = main_window_probe.scale_factor
    if real_scale == mock_scale:
        pytest.skip("mock scale and real scale are the same")
    scale_change = mock_scale / real_scale
    client_size = main_window_probe.client_size

    original_content = main_window.content
    GetScaleFactorForMonitor_original = shcore.GetScaleFactorForMonitor
    dpi_change_event = find_event(event_path, main_window_probe)

    try:
        main_window.toolbar.add(toga.Command(None, "Test command"))

        # Include widgets which are sized in different ways, with margin and fixed
        # sizes in both dimensions.
        main_window.content = toga.Box(
            style=Pack(direction="row"),
            children=[
                toga.Label(
                    "fixed",
                    id="fixed",
                    style=Pack(background_color="yellow", margin_left=20, width=100),
                ),
                toga.Label(
                    "minimal",  # Shrink to fit content
                    id="minimal",
                    style=Pack(background_color="cyan", font_size=16),
                ),
                toga.Label(
                    "flex",
                    id="flex",
                    style=Pack(
                        background_color="pink", flex=1, margin_top=15, height=50
                    ),
                ),
            ],
        )
        await main_window_probe.redraw("main_window is ready for testing")

        widget_ids = ["fixed", "minimal", "flex"]
        probes = {id: get_probe(main_window.widgets[id]) for id in widget_ids}

        decor_ids = ["menubar", "toolbar", "container"]
        probes.update(
            {id: getattr(main_window_probe, f"{id}_probe") for id in decor_ids}
        )
        ids = widget_ids + decor_ids

        def get_metrics():
            return (
                {id: Position(probes[id].x, probes[id].y) for id in ids},
                {id: Size(probes[id].width, probes[id].height) for id in ids},
                {id: probes[id].font_size for id in ids},
            )

        positions, sizes, font_sizes = get_metrics()

        # Because of hinting, font size changes can have non-linear effects on pixel
        # sizes.
        approx_fixed = partial(pytest.approx, abs=1)
        approx_font = partial(pytest.approx, rel=0.25)

        # Positions of the menubar, toolbar and top-level container are relative to the
        # window client area.
        assert font_sizes["menubar"] == 9
        assert positions["menubar"] == approx_fixed((0, 0))
        assert sizes["menubar"].width == approx_fixed(client_size.width)

        assert font_sizes["toolbar"] == 9
        assert positions["toolbar"] == approx_fixed((0, sizes["menubar"].height))
        assert sizes["toolbar"].width == approx_fixed(client_size.width)

        # Container has no text, so its font doesn't matter.
        assert positions["container"] == approx_fixed(
            (0, positions["toolbar"].y + sizes["toolbar"].height)
        )
        assert sizes["container"] == approx_fixed(
            (client_size.width, client_size.height - positions["container"].y)
        )

        # Positions of widgets are relative to the top-level container.
        assert font_sizes["fixed"] == 9  # Default font size on Windows
        assert positions["fixed"] == approx_fixed((20, 0))
        assert sizes["fixed"].width == approx_fixed(100)

        assert font_sizes["minimal"] == 16
        assert positions["minimal"] == approx_fixed((120, 0))
        assert sizes["minimal"].height == approx_font(sizes["fixed"].height * 16 / 9)

        assert font_sizes["flex"] == 9
        assert positions["flex"] == approx_fixed((120 + sizes["minimal"].width, 15))
        assert sizes["flex"] == approx_fixed(
            (client_size.width - positions["flex"].x, 50)
        )

        # Mock the function Toga uses to get the scale factor.
        def GetScaleFactorForMonitor_mock(hMonitor, pScale):
            pScale.value = int(mock_scale * 100)

        # Set and Trigger dpi change event with the specified dpi scale
        shcore.GetScaleFactorForMonitor = GetScaleFactorForMonitor_mock
        dpi_change_event(None)
        await main_window_probe.redraw(
            f"Triggered dpi change event with {mock_scale} dpi scale"
        )

        # Check Widget size DPI scaling
        positions_scaled, sizes_scaled, font_sizes_scaled = get_metrics()
        for id in ids:
            if id != "container":
                assert font_sizes_scaled[id] == approx_fixed(
                    font_sizes[id] * scale_change
                )

        assert positions_scaled["menubar"] == approx_fixed((0, 0))
        assert sizes_scaled["menubar"] == (
            approx_fixed(client_size.width),
            approx_font(sizes["menubar"].height * scale_change),
        )

        assert positions_scaled["toolbar"] == approx_fixed(
            (0, sizes_scaled["menubar"].height)
        )
        assert sizes_scaled["toolbar"] == (
            approx_fixed(client_size.width),
            approx_font(sizes["toolbar"].height * scale_change),
        )

        assert positions_scaled["container"] == approx_fixed(
            (0, positions_scaled["toolbar"].y + sizes_scaled["toolbar"].height)
        )
        assert sizes_scaled["container"] == approx_fixed(
            (client_size.width, client_size.height - positions_scaled["container"].y)
        )

        assert positions_scaled["fixed"] == approx_fixed(Position(20, 0) * scale_change)
        assert sizes_scaled["fixed"] == (
            approx_fixed(100 * scale_change),
            approx_font(sizes["fixed"].height * scale_change),
        )

        assert positions_scaled["minimal"] == approx_fixed(
            Position(120, 0) * scale_change
        )
        assert sizes_scaled["minimal"] == approx_font(sizes["minimal"] * scale_change)

        assert positions_scaled["flex"] == approx_fixed(
            (
                positions_scaled["minimal"].x + sizes_scaled["minimal"].width,
                15 * scale_change,
            )
        )
        assert sizes_scaled["flex"] == approx_fixed(
            (
                client_size.width - positions_scaled["flex"].x,
                50 * scale_change,
            )
        )

    finally:
        shcore.GetScaleFactorForMonitor = GetScaleFactorForMonitor_original
        dpi_change_event(None)
        await main_window_probe.redraw("Restored original state of main_window")
        assert get_metrics() == (positions, sizes, font_sizes)

        main_window.toolbar.clear()
        main_window.content = original_content


def find_event(event_path, main_window_probe):
    from Microsoft.Win32 import SystemEvents
    from System import Array, Object
    from System.Reflection import BindingFlags

    event_class, event_name = event_path.split(".")
    if event_class == "Form":
        return getattr(main_window_probe.native, f"On{event_name}")

    elif event_class == "SystemEvents":
        # There are no "On" methods in this class, so we need to use reflection.
        SystemEvents_type = SystemEvents().GetType()
        binding_flags = BindingFlags.Static | BindingFlags.NonPublic
        RaiseEvent = [
            method
            for method in SystemEvents_type.GetMethods(binding_flags)
            if method.Name == "RaiseEvent" and len(method.GetParameters()) == 2
        ][0]

        event_key = SystemEvents_type.GetField(
            f"On{event_name}Event", binding_flags
        ).GetValue(None)

        return lambda event_args: RaiseEvent.Invoke(
            None, [event_key, Array[Object]([None, event_args])]
        )

    else:
        raise AssertionError(f"unknown event class {event_class}")


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
