import gc
import re
import weakref
from importlib import import_module
from unittest.mock import Mock

import pytest
from pytest import approx

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, LIGHTBLUE, REBECCAPURPLE
from toga.constants import WindowState
from toga.style.pack import COLUMN, Pack

from ..assertions import (
    assert_window_gain_focus,
    assert_window_lose_focus,
    assert_window_on_hide,
    assert_window_on_show,
)


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


async def test_title(main_window, app_probe, main_window_probe):
    """The title of a window can be changed"""
    formal_name = getattr(app_probe, "formal_name", "Toga Testbed")
    original_title = main_window.title
    assert original_title == formal_name
    await main_window_probe.wait_for_window("Window title can be retrieved")

    try:
        main_window.title = "A Different Title"
        assert main_window.title == "A Different Title"
        await main_window_probe.wait_for_window("Window title can be changed")
    finally:
        main_window.title = original_title
        assert main_window.title == formal_name
        await main_window_probe.wait_for_window("Window title can be reverted")


# Mobile platforms have different windowing characteristics,
# so they have different tests.
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
    async def test_window_state_change(
        app,
        main_window,
        main_window_probe,
        initial_state,
        final_state,
    ):
        """Window state can be directly changed to another state."""
        if not main_window_probe.supports_fullscreen and WindowState.FULLSCREEN in {
            initial_state,
            final_state,
        }:
            pytest.xfail("This backend doesn't support fullscreen window state.")
        if not main_window_probe.supports_presentation and WindowState.PRESENTATION in {
            initial_state,
            final_state,
        }:
            pytest.xfail("This backend doesn't support presentation window state.")

        # Set to initial state
        main_window.state = initial_state
        # Wait for window animation before assertion.
        await main_window_probe.wait_for_window(
            f"Main window is in {initial_state}", state=initial_state
        )
        assert main_window_probe.instantaneous_state == initial_state

        # Set to final state
        main_window.state = final_state
        # Wait for window animation before assertion.
        await main_window_probe.wait_for_window(
            f"Main window is in {final_state}", state=final_state
        )
        assert main_window_probe.instantaneous_state == final_state

    @pytest.mark.parametrize(
        "state",
        [
            WindowState.NORMAL,
            WindowState.FULLSCREEN,
            WindowState.PRESENTATION,
        ],
    )
    async def test_window_state_same_as_current_without_intermediate_states(
        app, main_window, main_window_probe, state
    ):
        """Setting window state the same as current without any intermediate states is
        a no-op and there should be no expected delay from the OS."""
        if (
            not main_window_probe.supports_fullscreen
            and state == WindowState.FULLSCREEN
        ):
            pytest.xfail("This backend doesn't support fullscreen window state.")
        if (
            not main_window_probe.supports_presentation
            and state == WindowState.PRESENTATION
        ):
            pytest.xfail("This backend doesn't support presentation window state.")

        # Set the window state:
        main_window.state = state
        # Wait for window animation before assertion.
        await main_window_probe.wait_for_window(
            f"Secondary window is in {state}", state=state
        )
        assert main_window_probe.instantaneous_state == state

        # Set the window state the same as current:
        main_window.state = state
        assert main_window_probe.instantaneous_state == state

    @pytest.mark.parametrize(
        "state",
        [
            WindowState.FULLSCREEN,
            WindowState.PRESENTATION,
        ],
    )
    async def test_window_state_content_size_increase(
        app, app_probe, main_window, main_window_probe, state
    ):
        """The size of the window content should increase when the window state is set
        to maximized, fullscreen or presentation."""
        if (
            not main_window_probe.supports_fullscreen
            and state == WindowState.FULLSCREEN
        ):
            pytest.xfail("This backend doesn't support fullscreen window state.")
        if (
            not main_window_probe.supports_presentation
            and state == WindowState.PRESENTATION
        ):
            pytest.xfail("This backend doesn't support presentation window state.")

        main_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        # Wait for window animation before assertion.
        await main_window_probe.wait_for_window("Main window is shown")

        assert main_window_probe.instantaneous_state == WindowState.NORMAL
        initial_content_size = main_window_probe.content_size

        main_window.state = state
        # Add delay to ensure windows are visible after animation.
        await main_window_probe.wait_for_window(
            f"Main window is in {state}", state=state
        )
        assert main_window_probe.instantaneous_state == state
        # At least one of the dimension should have increased.
        assert (
            main_window_probe.content_size[0] > initial_content_size[0]
            or main_window_probe.content_size[1] > initial_content_size[1]
        )

        main_window.state = state
        # Wait for window animation before assertion.
        await main_window_probe.wait_for_window(
            f"Main window is still in {state}", state=state
        )
        assert main_window_probe.instantaneous_state == state
        # At least one of the dimension should have increased.
        assert (
            main_window_probe.content_size[0] > initial_content_size[0]
            or main_window_probe.content_size[1] > initial_content_size[1]
        )

        main_window.state = WindowState.NORMAL
        # Wait for window animation before assertion.
        await main_window_probe.wait_for_window(
            f"Main window is not in {state}", state=WindowState.NORMAL
        )
        assert main_window_probe.instantaneous_state == WindowState.NORMAL
        assert main_window_probe.content_size == initial_content_size

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
        """The window can be relocated to another screen, using both absolute and
        relative screen positions."""
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
    async def test_secondary_window(app, app_probe, second_window, second_window_probe):
        """A secondary window can be created"""
        formal_name = getattr(app_probe, "formal_name", "Toga Testbed")
        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.title == formal_name
        # Qt rendering results in a small change in window size
        assert second_window.size == approx((640, 480), abs=2)
        # Position should be cascaded; the exact position depends on the platform,
        # and how many windows have been created. As long as it's not at (100,100).
        if second_window_probe.supports_placement:
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
                {
                    "title": "Secondary Window",
                    "position": (200, 300),
                    "size": (300, 200),
                },
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
        # Qt rendering can result in a small change in window size
        assert second_window.size == approx((300, 200), abs=2)
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
                {
                    "title": "Secondary Window",
                    "position": (200, 300),
                    "size": (400, 200),
                },
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
                {
                    "title": "Not Resizable",
                    "resizable": False,
                    "position": (200, 150),
                },
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
                {
                    "title": "Not Closeable",
                    "closable": False,
                    "position": (200, 150),
                },
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
                {
                    "title": "Not Minimizable",
                    "minimizable": False,
                    "position": (200, 150),
                },
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
                {
                    "title": "Secondary Window",
                    "position": (200, 150),
                },
            )
        ],
    )
    async def test_visibility(app, second_window, second_window_probe):
        """Visibility of a window can be controlled"""
        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.visible
        # Qt rendering can result in a small change in window size
        assert second_window.size == approx((640, 480), abs=2)
        if second_window_probe.supports_placement:
            assert second_window.position == (200, 150)

        # Move the window
        second_window.position = (250, 200)

        await second_window_probe.wait_for_window("Secondary window has been moved")
        assert second_window.size == approx((640, 480), abs=2)
        if second_window_probe.supports_placement:
            assert second_window.position == (250, 200)

        # Resize the window
        second_window.size = (300, 250)

        await second_window_probe.wait_for_window(
            "Secondary window has been resized; position has not changed"
        )

        assert second_window.size == approx((300, 250), abs=2)
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
        assert second_window.size == approx((250, 200), abs=2)
        if (
            second_window_probe.supports_move_while_hidden
            and second_window_probe.supports_placement
        ):
            assert second_window.position == (300, 150)

        second_window_probe.minimize()
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            "Window has been minimized",
            state=WindowState.MINIMIZED,
        )

        if second_window_probe.supports_minimize:
            assert second_window_probe.is_minimized

        if second_window_probe.supports_unminimize:
            second_window_probe.unminimize()
            # Wait for window animation before assertion.
            await second_window_probe.wait_for_window(
                "Window has been unminimized",
                state=WindowState.NORMAL,
            )

            assert not second_window_probe.is_minimized
            # Window size hasn't changed as a result of min/unmin cycle
            assert second_window.size == approx((250, 200), abs=2)

        second_window_probe.close()
        await second_window_probe.wait_for_window("Secondary window has been closed")

        assert second_window not in app.windows

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                {
                    "title": "Secondary Window",
                    "position": (200, 150),
                },
            )
        ],
    )
    async def test_move_and_resize(second_window, second_window_probe):
        """A window can be moved and resized."""

        # Determine the extra width consumed by window chrome
        # (e.g., title bars, borders etc)
        extra_width = second_window.size[0] - second_window_probe.content_size[0]
        extra_height = second_window.size[1] - second_window_probe.content_size[1]

        second_window.position = (150, 50)
        await second_window_probe.wait_for_window("Secondary window has been moved")
        if second_window_probe.supports_placement:
            assert second_window.position == (150, 50)

        second_window.size = (200, 150)
        await second_window_probe.wait_for_window("Secondary window has been resized")
        # Qt rendering can result in a small change in window size
        assert second_window.size == approx((200, 150), abs=2)
        assert second_window_probe.content_size == approx(
            (
                200 - extra_width,
                150 - extra_height,
            ),
            abs=2,
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
        assert second_window.size == approx((200, 210 + extra_height), abs=2)
        assert second_window_probe.content_size == approx(
            (200 - extra_width, 210), abs=2
        )

        # Alter the content width to exceed window size
        box1.style.width = 250
        await second_window_probe.wait_for_window(
            "Secondary window has had width adjusted due to content"
        )
        assert second_window.size == approx(
            (250 + extra_width, 210 + extra_height), abs=2
        )

        # Alter both height and width to exceed window size at once
        box3 = toga.Box(style=Pack(background_color=LIGHTBLUE, width=300, height=90))
        second_window.content.add(box3)
        await second_window_probe.wait_for_window(
            "Secondary window has had width and height adjusted due to content"
        )
        assert second_window.size == approx(
            (300 + extra_width, 300 + extra_height), abs=2
        )
        assert second_window_probe.content_size == approx((300, 300), abs=2)

        # Try to resize to a size less than the content size
        second_window.size = (200, 150)
        await second_window_probe.wait_for_window(
            "Secondary window forced resize fails"
        )
        assert second_window.size == approx(
            (300 + extra_width, 300 + extra_height), abs=2
        )
        assert second_window_probe.content_size == approx((300, 300), abs=2)

    # FULLSCREEN->MAXIMIZED known to be flaky on x86_64 - see #3897
    @pytest.mark.flaky(retries=5, delay=1)
    @pytest.mark.parametrize(
        "initial_state, final_state",
        [
            # Switch from NORMAL:
            (WindowState.NORMAL, WindowState.MINIMIZED),
            (WindowState.NORMAL, WindowState.MAXIMIZED),
            (WindowState.NORMAL, WindowState.FULLSCREEN),
            (WindowState.NORMAL, WindowState.PRESENTATION),
            (WindowState.NORMAL, WindowState.NORMAL),
            # Switch from MINIMIZED:
            (WindowState.MINIMIZED, WindowState.NORMAL),
            (WindowState.MINIMIZED, WindowState.MAXIMIZED),
            (WindowState.MINIMIZED, WindowState.FULLSCREEN),
            (WindowState.MINIMIZED, WindowState.PRESENTATION),
            (WindowState.MINIMIZED, WindowState.MINIMIZED),
            # Switch from MAXIMIZED:
            (WindowState.MAXIMIZED, WindowState.NORMAL),
            (WindowState.MAXIMIZED, WindowState.MINIMIZED),
            (WindowState.MAXIMIZED, WindowState.FULLSCREEN),
            (WindowState.MAXIMIZED, WindowState.PRESENTATION),
            (WindowState.MAXIMIZED, WindowState.MAXIMIZED),
            # Switch from FULLSCREEN:
            (WindowState.FULLSCREEN, WindowState.NORMAL),
            (WindowState.FULLSCREEN, WindowState.MINIMIZED),
            (WindowState.FULLSCREEN, WindowState.MAXIMIZED),
            (WindowState.FULLSCREEN, WindowState.PRESENTATION),
            (WindowState.FULLSCREEN, WindowState.FULLSCREEN),
            # Switch from PRESENTATION:
            (WindowState.PRESENTATION, WindowState.NORMAL),
            (WindowState.PRESENTATION, WindowState.MINIMIZED),
            (WindowState.PRESENTATION, WindowState.MAXIMIZED),
            (WindowState.PRESENTATION, WindowState.FULLSCREEN),
            (WindowState.PRESENTATION, WindowState.PRESENTATION),
        ],
    )
    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.MainWindow,
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_window_state_change(
        app,
        app_probe,
        second_window,
        second_window_probe,
        initial_state,
        final_state,
    ):
        """Window state can be directly changed to another state."""
        if (
            WindowState.MINIMIZED in {initial_state, final_state}
            and not second_window_probe.supports_minimize
        ):
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )
        second_window.toolbar.add(app.cmd1)
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window("Secondary window is visible")
        assert second_window_probe.instantaneous_state == WindowState.NORMAL

        closure_exception = None

        def check_initial_state_size(window):
            if second_window_probe.instantaneous_state == initial_state:
                assert second_window.size > previous_state_window_size

        def check_final_state_size(window):
            if second_window_probe.instantaneous_state == final_state:
                current_size = second_window.size
                nonlocal closure_exception
                try:
                    if initial_state == WindowState.NORMAL:
                        assert current_size > previous_state_window_size
                    elif initial_state == WindowState.MAXIMIZED:
                        if final_state in {
                            WindowState.FULLSCREEN,
                            WindowState.PRESENTATION,
                        }:
                            if (  # noqa: E501
                                second_window_probe.maximize_fullscreen_presentation_equal_size
                            ):
                                assert current_size == previous_state_window_size
                            else:
                                assert current_size > previous_state_window_size
                        else:
                            assert current_size < previous_state_window_size
                    elif initial_state == WindowState.FULLSCREEN:
                        if final_state == WindowState.PRESENTATION:
                            if second_window_probe.fullscreen_presentation_equal_size:
                                assert current_size == previous_state_window_size
                            else:
                                assert current_size > previous_state_window_size
                        elif final_state == WindowState.MAXIMIZED:
                            if (  # noqa: E501
                                second_window_probe.maximize_fullscreen_presentation_equal_size
                            ):
                                assert current_size == previous_state_window_size
                            else:
                                assert current_size < previous_state_window_size
                        else:
                            assert current_size < previous_state_window_size
                    elif initial_state == WindowState.PRESENTATION:
                        if final_state == WindowState.FULLSCREEN:
                            if second_window_probe.fullscreen_presentation_equal_size:
                                assert current_size == previous_state_window_size
                            else:
                                assert current_size < previous_state_window_size
                        elif final_state == WindowState.MAXIMIZED:
                            if (  # noqa: E501
                                second_window_probe.maximize_fullscreen_presentation_equal_size
                            ):
                                assert current_size == previous_state_window_size
                            else:
                                assert current_size < previous_state_window_size
                        else:
                            assert current_size < previous_state_window_size
                except Exception as e:
                    closure_exception = e

        # Set up event mocks after the test window has been initialized.
        # This prevents unnecessary mock triggers during setup, which could
        # lead to false assertion errors later by incorrectly indicating that
        # the event was triggered.
        second_window.on_show = Mock()
        second_window.on_hide = Mock()
        second_window_on_resize_handler = Mock()
        second_window.on_resize = second_window_on_resize_handler

        previous_state_window_size = second_window.size
        second_window_on_resize_handler.side_effect = check_initial_state_size

        # Set to initial state
        second_window.state = initial_state
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {initial_state}", state=initial_state
        )
        assert second_window_probe.instantaneous_state == initial_state

        # Check and raise exceptions that may have occurred inside closures.
        if closure_exception:
            raise closure_exception

        # Check for resize event notification
        if initial_state in {WindowState.NORMAL, WindowState.MINIMIZED}:
            # on_resize() will not be triggered, as the state change
            # between NORMAL <-> MINIMIZED doesn't resize the window,
            # and state change between NORMAL <-> NORMAL is a no-op.
            second_window_on_resize_handler.assert_not_called()
            second_window_on_resize_handler.reset_mock()
            # Window size should remain the same
            assert second_window.size == previous_state_window_size
        else:
            second_window_on_resize_handler.assert_called_with(second_window)
            second_window_on_resize_handler.reset_mock()

        # Check for visibility event notification
        if initial_state == WindowState.MINIMIZED:
            # on_hide() will be triggered, as it was set to a
            # not-visible-to-user(minimized) state.
            assert_window_on_hide(second_window)
        else:
            # on_show() will not be triggered again, as it was
            # already in a visible-to-user(not hidden) state, and
            # was set to a visible-to-user(not minimized) state.
            assert_window_on_show(second_window, trigger_expected=False)

        previous_state_window_size = second_window.size
        second_window_on_resize_handler.side_effect = check_final_state_size

        # Set to final state
        second_window.state = final_state
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {final_state}", state=final_state
        )

        # Check and raise exceptions that may have occurred inside closures.
        if closure_exception:
            raise closure_exception

        # Check for resize event notification
        # State change between NORMAL <-> MINIMIZED doesn't
        # constitute a window resize operation.
        resize_expected = (initial_state != final_state) and not (
            {initial_state, final_state} == {WindowState.NORMAL, WindowState.MINIMIZED}
        )
        if resize_expected:
            # on_resize() event may be triggered multiple times, depending
            # upon the backend. For example: for a state change between:
            # FULLSCREEN -> MAXIMIZED, the actual window transition would
            # be: FULLSCREEN -> NORMAL -> MAXIMIZED. Therefore, on_resize()
            # would be triggered multiple times. Hence, just assert that the
            # on_resize() event has been called.
            second_window_on_resize_handler.assert_called_with(second_window)
            second_window_on_resize_handler.reset_mock()
        else:
            second_window_on_resize_handler.assert_not_called()
            second_window_on_resize_handler.reset_mock()
            # Window size should remain the same
            assert second_window.size == previous_state_window_size

        # Check for visibility event notification
        if initial_state == WindowState.MINIMIZED:
            if final_state == WindowState.MINIMIZED:
                # on_hide() will not be triggered again, as it was
                # already in a not-visible-to-user(minimized) state.
                assert_window_on_hide(second_window, trigger_expected=False)
            else:
                # on_show() will be triggered, as it was previously
                # in a not-visible-to-user(minimized) state.
                assert_window_on_show(second_window)
        else:
            if final_state == WindowState.MINIMIZED:
                # on_hide() will be triggered, as it was previously
                # in a visible-to-user(not minimized) state.
                assert_window_on_hide(second_window)
            else:
                # on_show() will not be triggered again, as it was
                # already in a visible-to-user(not minimized) state.
                assert_window_on_show(second_window, trigger_expected=False)

    @pytest.mark.flaky(retries=5, delay=1)
    @pytest.mark.parametrize(
        "states",
        [
            # Testing all possible window state change cases would be ideal,
            # but doing so would significantly increase the runtime of the
            # testbed. For practicality we are only testing the most complex
            # cases to ensure full coverage across all platforms.
            #
            # Complex state changes on cocoa:
            (WindowState.MINIMIZED, WindowState.FULLSCREEN),
            (WindowState.FULLSCREEN, WindowState.MINIMIZED),
            # Complex state changes on gtk:
            (WindowState.FULLSCREEN, WindowState.PRESENTATION),
            (WindowState.PRESENTATION, WindowState.NORMAL),
            # Complex state changes on qt:
            (WindowState.FULLSCREEN, WindowState.MAXIMIZED),
            (WindowState.PRESENTATION, WindowState.MAXIMIZED),
            (WindowState.MINIMIZED, WindowState.MAXIMIZED),
        ],
    )
    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.MainWindow,
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_window_state_rapid_assignment(
        app, second_window, second_window_probe, states
    ):
        """The backends can handle rapid assignment of new window states."""
        # Check that the state to be asserted is supported by the backend.
        if (
            WindowState.MINIMIZED in states
            and not second_window_probe.supports_minimize
        ):
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )
        second_window.toolbar.add(app.cmd1)
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window("Secondary window is visible")
        assert second_window_probe.instantaneous_state == WindowState.NORMAL

        # Assign new states without waiting for each transition to complete,
        # to test that the backend can handle rapid window state assignments.
        for state in states:
            second_window.state = state
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {states[-1]}", state=states[-1]
        )

        # Verify that the backend handled rapid assignments by checking if
        # the window reached the correct final window state.
        assert second_window_probe.instantaneous_state == states[-1]

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
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_window_state_same_as_current_without_intermediate_states(
        app_probe, second_window, second_window_probe, state
    ):
        """Setting window state the same as current without any intermediate states is
        a no-op and there should be no expected delay from the OS."""
        if state == WindowState.MINIMIZED and not second_window_probe.supports_minimize:
            pytest.xfail(
                "This backend doesn't reliably support minimized window state."
            )

        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window("Secondary window is shown")

        # Set the window state:
        second_window.state = state
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {state}", state=state
        )
        assert second_window_probe.instantaneous_state == state

        # Set the window state the same as current:
        second_window.state = state
        # No need to wait for OS delay as the above operation should be a no-op.
        assert second_window_probe.instantaneous_state == state

    @pytest.mark.parametrize(
        "state",
        [
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
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_window_state_content_size_increase(
        second_window, second_window_probe, state
    ):
        """The size of the window content should increase when the window state is set
        to maximized, fullscreen or presentation."""
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window("Secondary window is shown")

        assert second_window_probe.instantaneous_state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        initial_content_size = second_window_probe.content_size

        second_window.state = state
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {state}", state=state
        )
        assert second_window_probe.instantaneous_state == state
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.state = state
        await second_window_probe.wait_for_window(
            f"Secondary window is still in {state}", state=state
        )
        assert second_window_probe.instantaneous_state == state
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.state = WindowState.NORMAL
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            f"Secondary window is not in {state}", state=WindowState.NORMAL
        )
        assert second_window_probe.instantaneous_state == WindowState.NORMAL
        assert second_window_probe.is_resizable
        assert second_window_probe.content_size == initial_content_size

    @pytest.mark.parametrize(
        "state",
        [
            WindowState.NORMAL,
            WindowState.MAXIMIZED,
            # Window cannot be hidden while in MINIMIZED, FULLSCREEN or
            # PRESENTATION. So, those states are excluded from this test.
        ],
    )
    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_window_state_when_window_hidden(
        second_window, second_window_probe, state
    ):
        """When a window is hidden using hide(), the window.state getter should
        continue to report the same state as it did when the window was last visible."""
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window("Secondary window is shown")

        second_window.state = state
        # Wait for window animation before assertion.
        await second_window_probe.wait_for_window(
            f"Secondary window is in {state}", state=state
        )
        assert second_window_probe.instantaneous_state == state
        window_state_before_hidden = second_window.state

        second_window.hide()
        await second_window_probe.wait_for_window("Secondary window is hidden")
        assert second_window.state == window_state_before_hidden

        second_window.show()
        await second_window_probe.wait_for_window("Secondary window shown")
        assert second_window.state == window_state_before_hidden

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_focus_events(
        app, main_window, main_window_probe, second_window, second_window_probe
    ):
        """The window can trigger on_gain_focus() and on_lose_focus()
        event handlers, when the window gains or loses input focus."""
        if not main_window_probe.supports_focus:
            pytest.skip("GTK4 doesn't yet support gain and lose focus.")

        main_window.on_gain_focus = Mock()
        main_window.on_lose_focus = Mock()
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        second_window.on_gain_focus = Mock()
        second_window.on_lose_focus = Mock()

        app.current_window = main_window
        await main_window_probe.wait_for_window("Setting main window as current window")
        assert app.current_window == main_window
        assert_window_gain_focus(main_window)
        assert_window_lose_focus(second_window)

        app.current_window = second_window
        await second_window_probe.wait_for_window(
            "Setting second window as current window"
        )
        assert app.current_window == second_window
        assert_window_gain_focus(second_window)
        assert_window_lose_focus(main_window)

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_visibility_events(second_window, second_window_probe):
        """The window can trigger on_show() and on_hide() event handlers,
        when the window is shown or hidden respectively."""
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        second_window.on_show = Mock()
        second_window.on_hide = Mock()

        second_window.hide()
        await second_window_probe.wait_for_window(f"Hiding {second_window.title}")
        assert_window_on_hide(second_window)

        second_window.show()
        await second_window_probe.wait_for_window(f"Showing {second_window.title}")
        assert_window_on_show(second_window)

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_resize_event(second_window, second_window_probe):
        """The window can trigger on_resize() event handler, when the window
        size is changed."""
        second_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        second_window.show()
        expected_window_size = None

        def check_new_size_on_resize(window):
            assert window.size == expected_window_size

        second_window_on_resize_handler = Mock()
        second_window_on_resize_handler.side_effect = check_new_size_on_resize
        # Register the event handler.
        second_window.on_resize = second_window_on_resize_handler
        await second_window_probe.wait_for_window("Second window has been shown")
        initial_size = second_window.size

        # Resize the window, on_resize() will be triggered with the new size.
        expected_window_size = (200, 150)
        second_window.size = (200, 150)
        await second_window_probe.wait_for_window("Second window has been resized")
        assert second_window.size == (200, 150)
        second_window_on_resize_handler.assert_called_with(second_window)
        second_window_on_resize_handler.reset_mock()

        # Resize to initial size, on_resize() will be triggered with the new size.
        expected_window_size = initial_size
        second_window.size = initial_size
        await second_window_probe.wait_for_window("Second window has been resized")
        assert second_window.size == initial_size
        second_window_on_resize_handler.assert_called_with(second_window)
        second_window_on_resize_handler.reset_mock()

        # Again resize to initial size, on_resize() will not be triggered
        second_window.size = initial_size
        await second_window_probe.wait_for_window("Second window has been resized")
        assert second_window.size == initial_size
        second_window_on_resize_handler.assert_not_called()

    @pytest.mark.parametrize(
        "second_window_class, second_window_kwargs",
        [
            (
                toga.Window,
                {"title": "Secondary Window", "position": (200, 150)},
            )
        ],
    )
    async def test_screen(second_window, second_window_probe):
        """The window can be relocated to another screen, using both absolute and
        relative screen positions."""

        if not second_window_probe.supports_placement:
            pytest.xfail("This backend doesn't support window placement.")
        initial_position = second_window.position

        # Move the window using absolute position.
        second_window.position = (200, 200)
        await second_window_probe.wait_for_window("Secondary window has been moved")
        assert second_window.position != initial_position

        # `position` and `screen_position` will be same as the window will be in
        # primary screen. They are also 2-tuples of integers
        assert second_window.position == (200, 200)
        assert all(isinstance(val, int) for val in second_window.position)

        assert second_window.screen_position == (200, 200)
        assert all(isinstance(val, int) for val in second_window.screen_position)

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
            assert all(isinstance(val, int) for val in second_window.screen_position)


async def test_as_image(main_window, main_window_probe):
    """The window can be captured as a screenshot"""

    if main_window_probe.supports_as_image:
        screenshot = main_window.as_image()
        main_window_probe.assert_image_size(
            screenshot.size,
            main_window_probe.content_size,
            screen=main_window.screen,
            window=main_window,
        )
