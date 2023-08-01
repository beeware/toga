from importlib import import_module
from unittest.mock import Mock

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE
from toga.style.pack import COLUMN, Pack


def window_probe(app, window):
    module = import_module("tests_backend.window")
    return getattr(module, "WindowProbe")(app, window)


async def test_secondary_window(app):
    """A secondary window can be created"""
    new_window = toga.Window()
    probe = window_probe(app, new_window)

    new_window.show()
    await probe.redraw("New window has been shown")

    assert new_window.app == app
    assert new_window in app.windows

    assert new_window.title == "Toga"
    assert new_window.size == (640, 480)
    assert new_window.position == (100, 100)
    assert probe.is_resizable
    assert probe.is_closeable
    assert probe.is_minimizable

    new_window.close()
    await probe.redraw("New window has been closed")

    assert new_window not in app.windows


async def test_secondary_window_with_args(app):
    """A secondary window can be created with a specific size and position."""
    on_close_handler = Mock(return_value=False)

    new_window = toga.Window(
        title="New Window",
        position=(200, 300),
        size=(300, 200),
        on_close=on_close_handler,
    )
    probe = window_probe(app, new_window)

    new_window.show()
    await probe.redraw("New window has been shown")

    assert new_window.app == app
    assert new_window in app.windows

    assert new_window.title == "New Window"
    assert new_window.size == (300, 200)
    assert new_window.position == (200, 300)

    probe.close()
    await probe.redraw("Attempt to close second window that is rejected")
    on_close_handler.assert_called_once_with(new_window)

    assert new_window in app.windows

    # Reset, and try again, this time allowing the
    on_close_handler.reset_mock()
    on_close_handler.return_value = True

    probe.close()
    await probe.redraw("Attempt to close second window that succeeds")
    on_close_handler.assert_called_once_with(new_window)

    assert new_window not in app.windows


async def test_non_resizable(app):
    """A non-resizable window can be created"""
    new_window = toga.Window(
        title="Not Resizable", resizeable=False, position=(150, 150)
    )

    new_window.show()

    probe = window_probe(app, new_window)
    await probe.redraw("Non resizable window has been shown")

    assert new_window.visible
    assert not probe.is_resizable

    # Clean up
    new_window.close()


async def test_non_closeable(app):
    """A non-closeable window can be created"""
    new_window = toga.Window(
        title="Not Closeable", closeable=False, position=(150, 150)
    )

    new_window.show()

    probe = window_probe(app, new_window)
    await probe.redraw("Non-closeable window has been shown")

    assert new_window.visible
    assert not probe.is_closeable

    # Do a UI close on the window
    probe.close()
    await probe.redraw("Close request was ignored")
    assert new_window.visible

    # Do an explicit close on the window
    new_window.close()
    await probe.redraw("Explicit close was honored")

    assert not new_window.visible


async def test_non_minimizable(app):
    """A non-minimizable window can be created"""
    new_window = toga.Window(
        title="Not Minimizable", minimizable=False, position=(150, 150)
    )

    new_window.show()

    probe = window_probe(app, new_window)
    await probe.redraw("Non-minimizable window has been shown")
    assert new_window.visible
    assert not probe.is_minimizable

    probe.minimize()
    await probe.redraw("Minimize request has been ignored")
    assert not probe.is_minimized

    # Clean up
    new_window.close()


async def test_visibility(app):
    """Visibility of a window can be controlled"""
    new_window = toga.Window(title="New Window", position=(200, 250))
    probe = window_probe(app, new_window)

    new_window.show()
    await probe.redraw("New window has been shown")

    assert new_window.app == app
    assert new_window in app.windows

    assert new_window.visible
    assert new_window.size == (640, 480)
    assert new_window.position == (200, 250)

    new_window.hide()
    await probe.redraw("New window has been hidden")

    assert not new_window.visible

    # Move and resie the window while offscreen
    new_window.size = (250, 200)
    new_window.position = (300, 150)

    new_window.show()
    await probe.redraw("New window has been made visible again")

    assert new_window.visible
    assert new_window.size == (250, 200)
    assert new_window.position == (300, 150)

    probe.minimize()
    # Delay is required to account for "genie" animations
    await probe.redraw("Window has been minimized", delay=0.5)

    assert probe.is_minimized

    probe.unminimize()
    # Delay is required to account for "genie" animations
    await probe.redraw("Window has been unminimized", delay=0.5)

    assert not probe.is_minimized

    probe.close()
    await probe.redraw("New window has been closed")

    assert new_window not in app.windows


async def test_move_and_resize(app):
    """A window can be moved and resized."""
    new_window = toga.Window(title="New Window")
    probe = window_probe(app, new_window)
    new_window.show()
    await probe.redraw("New window has been shown")

    # Determine
    extra_width = new_window.size[0] - probe.content_size[0]
    extra_height = new_window.size[1] - probe.content_size[1]

    new_window.position = (150, 50)
    await probe.redraw("New window has been moved")
    assert new_window.position == (150, 50)

    new_window.size = (200, 150)
    await probe.redraw("New window has been resized")
    assert new_window.size == (200, 150)
    assert probe.content_size == (200 - extra_width, 150 - extra_height)

    box1 = toga.Box(style=Pack(background_color=REBECCAPURPLE, width=10, height=10))
    box2 = toga.Box(style=Pack(background_color=GOLDENROD, width=10, height=200))
    new_window.content = toga.Box(
        children=[box1, box2],
        style=Pack(direction=COLUMN, background_color=CORNFLOWERBLUE),
    )
    await probe.redraw("New window has had height adjusted due to content")
    assert new_window.size == (200 + extra_width, 210 + extra_height)
    assert probe.content_size == (200, 210)

    # Alter the content width to exceed window size
    box1.style.width = 250
    await probe.redraw("New window has had width adjusted due to content")
    assert new_window.size == (250 + extra_width, 210 + extra_height)
    assert probe.content_size == (250, 210)

    # Try to resize to a size less than the content size
    new_window.size = (200, 150)
    await probe.redraw("New window forced resize fails")
    assert new_window.size == (250 + extra_width, 210 + extra_height)
    assert probe.content_size == (250, 210)

    new_window.close()
