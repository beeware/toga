import gc
import random
import re
import weakref
from importlib import import_module
from unittest.mock import Mock

import pytest

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE
from toga.constants import WindowState
from toga.style.pack import COLUMN, Pack

from ..widgets.probe import get_probe


def window_probe(app, window):
    module = import_module("tests_backend.window")
    return module.WindowProbe(app, window)


@pytest.fixture
async def second_window(second_window_class, second_window_kwargs):
    yield second_window_class(**second_window_kwargs)


@pytest.fixture
async def second_window_probe(app, app_probe, second_window):
    second_window.show()
    probe = window_probe(app, second_window)
    await probe.wait_for_window(f"Window ({second_window.title}) has been created")
    return probe


async def test_title(main_window, main_window_probe):
    """The title of a window can be changed"""
    original_title = main_window.title
    assert original_title == "Toga Testbed"
    await main_window_probe.wait_for_window("Window title can be retrieved")

    try:
        main_window.title = "A Different Title"
        assert main_window.title == "A Different Title"
        await main_window_probe.wait_for_window("Window title can be changed")
    finally:
        main_window.title = original_title
        assert main_window.title == "Toga Testbed"
        await main_window_probe.wait_for_window("Window title can be reverted")


# Mobile platforms have different windowing characteristics, so they have different tests.
if toga.platform.current_platform in {"iOS", "android"}:
    ####################################################################################
    # Mobile platform tests
    ####################################################################################

    async def test_visibility(main_window, main_window_probe):
        """Hide and close are no-ops on mobile"""
        assert main_window.visible

        main_window.hide()
        await main_window_probe.wait_for_window("Window.hide is a no-op")
        assert main_window.visible

        main_window.close()
        await main_window_probe.wait_for_window("Window.close is a no-op")
        assert main_window.visible

    async def test_secondary_window():
        """A secondary window cannot be created"""
        with pytest.raises(
            RuntimeError,
            match=r"Secondary windows cannot be created on .*",
        ):
            toga.Window()

    async def test_move_and_resize(main_window, main_window_probe, capsys):
        """Move and resize are no-ops on mobile."""
        initial_size = main_window.size
        content_size = main_window_probe.content_size
        assert initial_size[0] > 300
        assert initial_size[1] > 500

        assert main_window.position == (0, 0)

        main_window.position = (150, 50)
        await main_window_probe.wait_for_window("Main window can't be moved")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)

        main_window.size = (200, 150)
        await main_window_probe.wait_for_window("Main window cannot be resized")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)

        orig_content = main_window.content

        try:
            box1 = toga.Box(
                style=Pack(background_color=REBECCAPURPLE, width=10, height=10)
            )
            box2 = toga.Box(style=Pack(background_color=GOLDENROD, width=10, height=20))
            main_window.content = toga.Box(
                children=[box1, box2],
                style=Pack(direction=COLUMN, background_color=CORNFLOWERBLUE),
            )
            await main_window_probe.wait_for_window("Main window content has been set")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            # Alter the content width to exceed window width
            box1.style.width = 1000
            await main_window_probe.wait_for_window(
                "Content is too wide for the window"
            )
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            space_warning = (
                r"Warning: Window content \([\d.]+, [\d.]+\) "
                r"exceeds available space \([\d.]+, [\d.]+\)"
            )
            assert re.search(space_warning, capsys.readouterr().out)

            # Resize content to fit
            box1.style.width = 100
            await main_window_probe.wait_for_window("Content fits in window")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size
            assert not re.search(space_warning, capsys.readouterr().out)

            # Alter the content width to exceed window height
            box1.style.height = 2000
            await main_window_probe.wait_for_window(
                "Content is too tall for the window"
            )
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size
            assert re.search(space_warning, capsys.readouterr().out)

        finally:
            main_window.content = orig_content

    @pytest.mark.skipif(
        toga.platform.current_platform == "iOS", reason="Not implemented on iOS"
    )
    @pytest.mark.parametrize(
        "initial_state, final_state",
        [
            # Direct switch from NORMAL:
            (WindowState.NORMAL, WindowState.FULLSCREEN),
            (WindowState.NORMAL, WindowState.PRESENTATION),
            # Direct switch from FULLSCREEN:
            (WindowState.FULLSCREEN, WindowState.NORMAL),
            (WindowState.FULLSCREEN, WindowState.PRESENTATION),
            # Direct switch from PRESENTATION:
            (WindowState.PRESENTATION, WindowState.NORMAL),
            (WindowState.PRESENTATION, WindowState.FULLSCREEN),
        ],
    )
    async def test_window_state_direct_change(
        app, initial_state, final_state, main_window, main_window_probe
    ):
        """Window state can be directly changed to another state."""
        try:
            # Set to initial state
            main_window.state = initial_state
            await main_window_probe.wait_for_window(
                f"Main window is in {initial_state}"
            )

            assert main_window.state == initial_state

            # Set to final state
            main_window.state = final_state
            await main_window_probe.wait_for_window(f"Main window is in {final_state}")

            assert main_window.state == final_state
        finally:
            # Set to NORMAL state
            main_window.state = WindowState.NORMAL
            await main_window_probe.wait_for_window(
                "Main window is in WindowState.NORMAL"
            )

            assert main_window.state == WindowState.NORMAL

    @pytest.mark.skipif(
        toga.platform.current_platform == "iOS", reason="Not implemented on iOS"
    )
    @pytest.mark.parametrize(
        "state",
        [
            WindowState.NORMAL,
            WindowState.FULLSCREEN,
            WindowState.PRESENTATION,
        ],
    )
    async def test_window_state_same_as_current(
        app, main_window, main_window_probe, state
    ):
        """Setting the window state the same as current is a no-op."""
        try:
            # Set the window state:
            main_window.state = state
            await main_window_probe.wait_for_window(f"Secondary window is in {state}")
            assert main_window.state == state

            # Set the window state the same as current:
            main_window.state = state
            assert main_window.state == state

        finally:
            # Restore to NORMAL state.
            main_window.state = WindowState.NORMAL
            await main_window_probe.wait_for_window("Main window is not full screen")
            assert main_window.state == WindowState.NORMAL

    @pytest.mark.skipif(
        toga.platform.current_platform == "iOS", reason="Not implemented on iOS"
    )
    async def test_window_state_fullscreen(main_window, main_window_probe):
        """The window can enter into fullscreen state."""
        try:
            widget = toga.Box(style=Pack(flex=1))
            widget_probe = get_probe(widget)
            main_window.content = toga.Box(children=[widget])
            await main_window_probe.wait_for_window(
                "Test widget has been added to the window"
            )
            widget_initial_size = (widget_probe.width, widget_probe.height)

            # Make main window full screen
            main_window.state = WindowState.FULLSCREEN
            await main_window_probe.wait_for_window("Main window is full screen")
            assert main_window.state == WindowState.FULLSCREEN
            # At least one of the dimensions should have increased.
            assert (
                widget_probe.width > widget_initial_size[0]
                or widget_probe.height > widget_initial_size[1]
            )
        finally:
            # Exit full screen
            main_window.state = WindowState.NORMAL
            await main_window_probe.wait_for_window("Main window is not full screen")
            assert main_window.state == WindowState.NORMAL
            # Both dimensions should be the same.
            assert (
                widget_probe.width == widget_initial_size[0]
                and widget_probe.height == widget_initial_size[1]
            )
            main_window.content.clear()

    @pytest.mark.skipif(
        toga.platform.current_platform == "iOS", reason="Not implemented on iOS"
    )
    async def test_window_state_presentation(main_window, main_window_probe):
        """The window can enter into presentation state."""
        try:
            widget = toga.Box(style=Pack(flex=1))
            widget_probe = get_probe(widget)
            main_window.content = toga.Box(children=[widget])
            await main_window_probe.wait_for_window(
                "Test widget has been added to the window"
            )
            widget_initial_size = (widget_probe.width, widget_probe.height)

            # Enter presentation mode with main window
            main_window.state = WindowState.PRESENTATION
            await main_window_probe.wait_for_window(
                "Main window is in presentation mode"
            )
            assert main_window.state == WindowState.PRESENTATION
            # At least one of the dimensions should have increased.
            assert (
                widget_probe.width > widget_initial_size[0]
                or widget_probe.height > widget_initial_size[1]
            )
        finally:
            # Exit presentation mode
            main_window.state = WindowState.NORMAL
            await main_window_probe.wait_for_window(
                "Main window is not in presentation mode"
            )
            assert main_window.state == WindowState.NORMAL
            # Both dimensions should be the same.
            assert (
                widget_probe.width == widget_initial_size[0]
                and widget_probe.height == widget_initial_size[1]
            )
            main_window.content.clear()

    @pytest.mark.skipif(
        toga.platform.current_platform == "iOS", reason="Not implemented on iOS"
    )
    @pytest.mark.parametrize(
        "state",
        [
            WindowState.MINIMIZED,
            WindowState.MAXIMIZED,
        ],
    )
    async def test_window_state_no_op_states(main_window, main_window_probe, state):
        """MINIMIZED and MAXIMIZED states are no-op on mobile platforms."""
        assert main_window.state == WindowState.NORMAL
        # Assign the no-op state.
        main_window.state = state
        # The state should still be NORMAL:
        assert main_window.state == WindowState.NORMAL

    async def test_screen(main_window, main_window_probe):
        """The window can be relocated to another screen, using both absolute and relative screen positions."""
        assert main_window.screen.origin == (0, 0)
        initial_size = main_window.size
        main_window.position = (150, 50)
        await main_window_probe.wait_for_window("Main window can't be moved")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)
        assert main_window.screen_position == (0, 0)

else:
    ####################################################################################
    # Desktop platform tests
    ####################################################################################

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [(toga.Window, {})],
    )
    async def test_secondary_window(app, second_window, second_window_probe):
        """A secondary window can be created"""
        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.title == "Toga Testbed"
        assert second_window.size == (640, 480)
        # Position should be cascaded; the exact position depends on the platform,
        # and how many windows have been created. As long as it's not at (100,100).
        assert second_window.position != (100, 100)

        assert second_window_probe.is_resizable
        if second_window_probe.supports_closable:
            assert second_window_probe.is_closable
        if second_window_probe.supports_minimizable:
            assert second_window_probe.is_minimizable

        second_window.close()
        await second_window_probe.wait_for_window("Secondary window has been closed")

        assert second_window not in app.windows

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 300), size=(300, 200)),
            )
        ],
    )
    async def test_secondary_window_with_args(app, second_window, second_window_probe):
        """A secondary window can be created with a specific size and position."""
        on_close_handler = Mock(return_value=False)
        second_window.on_close = on_close_handler

        second_window.show()
        await second_window_probe.wait_for_window("Secondary window has been shown")

        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.title == "Secondary Window"
        assert second_window.size == (300, 200)
        if second_window_probe.supports_placement:
            assert second_window.position == (200, 300)

        second_window_probe.close()
        await second_window_probe.wait_for_window(
            "Attempt to close second window that is rejected"
        )
        on_close_handler.assert_called_once_with(second_window)

        assert second_window in app.windows

        # Reset, and try again, this time allowing the
        on_close_handler.reset_mock()
        on_close_handler.return_value = True

        second_window_probe.close()
        await second_window_probe.wait_for_window(
            "Attempt to close second window that succeeds"
        )
        on_close_handler.assert_called_once_with(second_window)

        assert second_window not in app.windows

    async def test_secondary_window_with_content(app):
        """A window can be created with initial content"""
        # Setup the box with something inside it:
        label1 = toga.Label("Hello World")
        content = toga.Box(children=[label1])

        window_with_content = toga.Window(content=content)
        window_with_content_probe = window_probe(app, window_with_content)

        try:
            window_with_content.show()
            await window_with_content_probe.wait_for_window(
                "Create a window with initial content"
            )
            assert window_with_content.content == content
        finally:
            window_with_content.close()

    async def test_secondary_window_cleanup(app_probe):
        """Memory for windows is cleaned up when windows are deleted."""
        # Create and show a window with content. We can't use the second_window fixture
        # because the fixture will retain a reference, preventing garbage collection.
        second_window = toga.Window()
        second_window.content = toga.Box()
        second_window.show()
        await app_probe.redraw("Secondary Window has been created")

        # Retain a weak reference to the window to check garbage collection
        window_ref = weakref.ref(second_window)
        impl_ref = weakref.ref(second_window._impl)

        second_window.close()
        await app_probe.redraw("Secondary window has been closed")

        # Clear the local reference to the window (which should be the last reference),
        # and force a garbage collection pass. This should cause deletion of both the
        # interface and impl of the window.
        del second_window
        gc.collect()

        # Assert that the weak references are now dead.
        assert window_ref() is None
        assert impl_ref() is None

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.MainWindow,
                dict(title="Secondary Window", position=(200, 300), size=(400, 200)),
            )
        ],
    )
    async def test_secondary_window_toolbar(app, second_window, second_window_probe):
        """A toolbar can be added to a secondary window"""
        second_window.toolbar.add(app.cmd1)

        # Window doesn't have content. This is intentional.
        second_window.show()

        assert second_window_probe.has_toolbar()
        await second_window_probe.redraw("Secondary window has a toolbar")

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Not Resizable", resizable=False, position=(200, 150)),
            )
        ],
    )
    async def test_non_resizable(second_window, second_window_probe):
        """A non-resizable window can be created"""
        assert second_window.visible
        assert not second_window_probe.is_resizable

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Not Closeable", closable=False, position=(200, 150)),
            )
        ],
    )
    async def test_non_closable(second_window, second_window_probe):
        """A non-closable window can be created. Backends that don't support this
        natively should implement it by making the close button do nothing."""
        assert second_window.visible

        on_close_handler = Mock(return_value=False)
        second_window.on_close = on_close_handler

        if second_window_probe.supports_closable:
            assert not second_window_probe.is_closable

        # Do a UI close on the window
        second_window_probe.close()
        await second_window_probe.wait_for_window("Close request was ignored")
        on_close_handler.assert_not_called()
        assert second_window.visible

        # Do an explicit close on the window
        second_window.close()
        await second_window_probe.wait_for_window("Explicit close was honored")
        on_close_handler.assert_not_called()
        assert not second_window.visible

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Not Minimizable", minimizable=False, position=(200, 150)),
            )
        ],
    )
    async def test_non_minimizable(second_window, second_window_probe):
        """A non-minimizable window can be created"""
        if not second_window_probe.supports_minimizable:
            pytest.xfail("This backend doesn't support disabling minimization")

        assert second_window.visible
        assert not second_window_probe.is_minimizable

        second_window_probe.minimize()
        await second_window_probe.wait_for_window("Minimize request has been ignored")
        assert not second_window_probe.is_minimized

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_visibility(app, second_window, second_window_probe):
        """Visibility of a window can be controlled"""
        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.visible
        assert second_window.size == (640, 480)
        if second_window_probe.supports_placement:
            assert second_window.position == (200, 150)

        # Move the window
        second_window.position = (250, 200)

        await second_window_probe.wait_for_window("Secondary window has been moved")
        assert second_window.size == (640, 480)
        if second_window_probe.supports_placement:
            assert second_window.position == (250, 200)

        # Resize the window
        second_window.size = (300, 250)

        await second_window_probe.wait_for_window(
            "Secondary window has been resized; position has not changed"
        )

        assert second_window.size == (300, 250)
        # We can't confirm position here, because it may have changed. macOS rescales
        # windows relative to the bottom-left corner, which means the position of the
        # window has changed relative to the Toga coordinate frame.

        second_window.hide()
        await second_window_probe.wait_for_window("Secondary window has been hidden")

        assert not second_window.visible

        # Move and resize the window while offscreen
        second_window.size = (250, 200)
        second_window.position = (300, 150)

        second_window.show()
        await second_window_probe.wait_for_window(
            "Secondary window has been made visible again; window has moved"
        )

        assert second_window.visible
        assert second_window.size == (250, 200)
        if (
            second_window_probe.supports_move_while_hidden
            and second_window_probe.supports_placement
        ):
            assert second_window.position == (300, 150)

        second_window_probe.minimize()
        # Delay is required to account for "genie" animations
        await second_window_probe.wait_for_window(
            "Window has been minimized",
            minimize=True,
        )

        if second_window_probe.supports_minimize:
            assert second_window_probe.is_minimized

        if second_window_probe.supports_unminimize:
            second_window_probe.unminimize()
            # Delay is required to account for "genie" animations
            await second_window_probe.wait_for_window(
                "Window has been unminimized",
                minimize=True,
            )

            assert not second_window_probe.is_minimized

        second_window_probe.close()
        await second_window_probe.wait_for_window("Secondary window has been closed")

        assert second_window not in app.windows

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_move_and_resize(second_window, second_window_probe):
        """A window can be moved and resized."""

        # Determine the extra width consumed by window chrome (e.g., title bars, borders etc)
        extra_width = second_window.size[0] - second_window_probe.content_size[0]
        extra_height = second_window.size[1] - second_window_probe.content_size[1]

        second_window.position = (150, 50)
        await second_window_probe.wait_for_window("Secondary window has been moved")
        if second_window_probe.supports_placement:
            assert second_window.position == (150, 50)

        second_window.size = (200, 150)
        await second_window_probe.wait_for_window("Secondary window has been resized")
        assert second_window.size == (200, 150)
        assert second_window_probe.content_size == (
            200 - extra_width,
            150 - extra_height,
        )

        box1 = toga.Box(style=Pack(background_color=REBECCAPURPLE, width=10, height=10))
        box2 = toga.Box(style=Pack(background_color=GOLDENROD, width=10, height=200))
        second_window.content = toga.Box(
            children=[box1, box2],
            style=Pack(direction=COLUMN, background_color=CORNFLOWERBLUE),
        )
        await second_window_probe.wait_for_window(
            "Secondary window has had height adjusted due to content"
        )
        assert second_window.size == (200, 210 + extra_height)
        assert second_window_probe.content_size == (200 - extra_width, 210)

        # Alter the content width to exceed window size
        box1.style.width = 250
        await second_window_probe.wait_for_window(
            "Secondary window has had width adjusted due to content"
        )
        assert second_window.size == (250 + extra_width, 210 + extra_height)
        assert second_window_probe.content_size == (250, 210)

        # Try to resize to a size less than the content size
        second_window.size = (200, 150)
        await second_window_probe.wait_for_window(
            "Secondary window forced resize fails"
        )
        assert second_window.size == (250 + extra_width, 210 + extra_height)
        assert second_window_probe.content_size == (250, 210)

    @pytest.mark.parametrize(
        "initial_state, final_state",
        [
            # Direct switch from NORMAL:
            (WindowState.NORMAL, WindowState.MINIMIZED),
            (WindowState.NORMAL, WindowState.MAXIMIZED),
            (WindowState.NORMAL, WindowState.FULLSCREEN),
            (WindowState.NORMAL, WindowState.PRESENTATION),
            # Direct switch from MINIMIZED:
            (WindowState.MINIMIZED, WindowState.NORMAL),
            (WindowState.MINIMIZED, WindowState.MAXIMIZED),
            (WindowState.MINIMIZED, WindowState.FULLSCREEN),
            (WindowState.MINIMIZED, WindowState.PRESENTATION),
            # Direct switch from MAXIMIZED:
            (WindowState.MAXIMIZED, WindowState.NORMAL),
            (WindowState.MAXIMIZED, WindowState.MINIMIZED),
            (WindowState.MAXIMIZED, WindowState.FULLSCREEN),
            (WindowState.MAXIMIZED, WindowState.PRESENTATION),
            # Direct switch from FULLSCREEN:
            (WindowState.FULLSCREEN, WindowState.NORMAL),
            (WindowState.FULLSCREEN, WindowState.MINIMIZED),
            (WindowState.FULLSCREEN, WindowState.MAXIMIZED),
            (WindowState.FULLSCREEN, WindowState.PRESENTATION),
            # Direct switch from PRESENTATION:
            (WindowState.PRESENTATION, WindowState.NORMAL),
            (WindowState.PRESENTATION, WindowState.MINIMIZED),
            (WindowState.PRESENTATION, WindowState.MAXIMIZED),
            (WindowState.PRESENTATION, WindowState.FULLSCREEN),
        ],
    )
    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.MainWindow,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_window_state_direct_change(
        app,
        app_probe,
        initial_state,
        final_state,
        second_window,
        second_window_probe,
        intermediate_states=tuple(
            random.sample(
                [
                    WindowState.NORMAL,
                    WindowState.MINIMIZED,
                    WindowState.MAXIMIZED,
                    WindowState.FULLSCREEN,
                    WindowState.PRESENTATION,
                    WindowState.MINIMIZED,
                ],
                6,
            )
        ),
    ):
        """Window state can be directly changed to another state."""
        if (
            WindowState.MINIMIZED in {initial_state, final_state}
            and not second_window_probe.supports_minimize
        ):
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )
        elif (
            WindowState.FULLSCREEN in {initial_state, final_state}
            and not second_window_probe.supports_fullscreen
        ):
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )
        elif (
            WindowState.PRESENTATION in {initial_state, final_state}
            and not second_window_probe.supports_presentation
        ):
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )

        second_window.toolbar.add(app.cmd1)
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()

        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is visible", full_screen=True
        )

        assert second_window.state == WindowState.NORMAL

        # Set to initial state
        second_window.state = initial_state
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {initial_state}", full_screen=True
        )

        assert second_window.state == initial_state

        # Set to the intermediate states but don't wait for the OS delay.
        for state in intermediate_states:
            second_window.state = state

        # Set to final state
        second_window.state = final_state
        # Add delay to ensure windows are visible after animation.
        await app_probe.redraw(f"Secondary window is in {final_state}", delay=1.5)
        assert second_window.state == final_state

    @pytest.mark.parametrize(
        "state",
        [
            WindowState.NORMAL,
            WindowState.MINIMIZED,
            WindowState.MAXIMIZED,
            WindowState.FULLSCREEN,
            WindowState.PRESENTATION,
        ],
    )
    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_window_state_same_as_current(
        app_probe, second_window, second_window_probe, state
    ):
        """Setting window state the same as current is a no-op."""
        if state == WindowState.MINIMIZED and not second_window_probe.supports_minimize:
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )
        elif (
            state == WindowState.FULLSCREEN
            and not second_window_probe.supports_fullscreen
        ):
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )
        elif (
            state == WindowState.PRESENTATION
            and not second_window_probe.supports_presentation
        ):
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )

        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is shown", full_screen=True
        )

        # Set the window state:
        second_window.state = state
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {state}", full_screen=True
        )
        assert second_window.state == state

        # Set the window state the same as current:
        second_window.state = state
        assert second_window.state == state

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_window_state_minimized(second_window, second_window_probe):
        """Window can have minimized window state."""
        if not second_window_probe.supports_minimize:
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )

        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is shown",
        )

        assert second_window.state == WindowState.NORMAL
        if second_window_probe.supports_minimizable:
            assert second_window_probe.is_minimizable

        second_window.state = WindowState.MINIMIZED
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is minimized", minimize=True
        )
        assert second_window.state == WindowState.MINIMIZED

        second_window.state = WindowState.MINIMIZED
        await second_window_probe.wait_for_window("Secondary window is still minimized")
        assert second_window.state == WindowState.MINIMIZED

        second_window.state = WindowState.NORMAL
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is not minimized", minimize=True
        )
        assert second_window.state == WindowState.NORMAL
        if second_window_probe.supports_minimizable:
            assert second_window_probe.is_minimizable

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_window_state_maximized(second_window, second_window_probe):
        """Window can have maximized window state."""
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is shown",
        )

        assert second_window.state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        initial_content_size = second_window_probe.content_size

        second_window.state = WindowState.MAXIMIZED
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is maximized",
        )
        assert second_window.state == WindowState.MAXIMIZED
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.state = WindowState.MAXIMIZED
        await second_window_probe.wait_for_window("Secondary window is still maximized")
        assert second_window.state == WindowState.MAXIMIZED
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.state = WindowState.NORMAL
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is not maximized",
        )
        assert second_window.state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        assert second_window_probe.content_size == initial_content_size

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_window_state_full_screen(second_window, second_window_probe):
        """Window can have full screen window state."""
        if not second_window_probe.supports_fullscreen:
            pytest.xfail(
                "This backend doesn't reliably support fullscreen window state."
            )
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is shown",
        )

        assert second_window.state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        initial_content_size = second_window_probe.content_size

        second_window.state = WindowState.FULLSCREEN
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is full screen", full_screen=True
        )
        assert second_window.state == WindowState.FULLSCREEN
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.state = WindowState.FULLSCREEN
        await second_window_probe.wait_for_window(
            "Secondary window is still full screen", full_screen=True
        )
        assert second_window.state == WindowState.FULLSCREEN
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.state = WindowState.NORMAL
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is not full screen", full_screen=True
        )
        assert second_window.state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        assert second_window_probe.content_size == initial_content_size

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_window_state_presentation(
        second_window, second_window_probe, app_probe
    ):
        """Window can have presentation window state."""
        if not second_window_probe.supports_presentation:
            pytest.xfail(
                "This backend doesn't reliably support presentation window state."
            )
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is shown",
        )

        assert second_window.state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        initial_content_size = second_window_probe.presentation_content_size

        second_window.state = WindowState.PRESENTATION
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is in presentation mode", full_screen=True
        )
        assert second_window.state == WindowState.PRESENTATION
        assert (
            second_window_probe.presentation_content_size[0] > initial_content_size[0]
        )
        assert (
            second_window_probe.presentation_content_size[1] > initial_content_size[1]
        )

        second_window.state = WindowState.PRESENTATION
        await second_window_probe.wait_for_window(
            "Secondary window is still in presentation mode", full_screen=True
        )
        assert second_window.state == WindowState.PRESENTATION
        assert (
            second_window_probe.presentation_content_size[0] > initial_content_size[0]
        )
        assert (
            second_window_probe.presentation_content_size[1] > initial_content_size[1]
        )

        second_window.state = WindowState.NORMAL
        # Add delay to ensure windows are visible after animation.
        await second_window_probe.wait_for_window(
            "Secondary window is not in presentation mode", full_screen=True
        )
        assert second_window.state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        assert second_window_probe.presentation_content_size == initial_content_size

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                dict(title="Secondary Window", position=(200, 150)),
            )
        ],
    )
    async def test_screen(second_window, second_window_probe):
        """The window can be relocated to another screen, using both absolute and relative screen positions."""

        initial_position = second_window.position

        # Move the window using absolute position.
        second_window.position = (200, 200)
        await second_window_probe.wait_for_window("Secondary window has been moved")
        if second_window_probe.supports_placement:
            assert second_window.position != initial_position

        # `position` and `screen_position` will be same as the window will be in primary screen.
        if second_window_probe.supports_placement:
            assert second_window.position == (200, 200)
            assert second_window.screen_position == (200, 200)

        # Move the window between available screens and assert its `screen_position`
        for screen in second_window.app.screens:
            second_window.screen = screen
            await second_window_probe.wait_for_window(
                f"Secondary window has been moved to {screen.name}"
            )
            assert second_window.screen == screen
            assert second_window.screen_position == (
                second_window.position[0] - screen.origin[0],
                second_window.position[1] - screen.origin[1],
            )


async def test_as_image(main_window, main_window_probe):
    """The window can be captured as a screenshot"""

    screenshot = main_window.as_image()
    main_window_probe.assert_image_size(
        screenshot.size,
        main_window_probe.content_size,
        screen=main_window.screen,
    )
