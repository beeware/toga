from unittest.mock import Mock

import pytest

import toga
from toga.colors import WHITE


@pytest.fixture
def on_resize_handler():
    return Mock()


@pytest.fixture
def on_press_handler():
    return Mock()


@pytest.fixture
def on_drag_handler():
    return Mock()


@pytest.fixture
def on_release_handler():
    return Mock()


@pytest.fixture
def on_activate_handler():
    return Mock()


@pytest.fixture
def on_alt_press_handler():
    return Mock()


@pytest.fixture
def on_alt_drag_handler():
    return Mock()


@pytest.fixture
def on_alt_release_handler():
    return Mock()


@pytest.fixture
async def widget(
    on_resize_handler,
    on_press_handler,
    on_activate_handler,
    on_release_handler,
    on_drag_handler,
    on_alt_press_handler,
    on_alt_release_handler,
    on_alt_drag_handler,
):
    return toga.Canvas(
        on_resize=on_resize_handler,
        on_press=on_press_handler,
        on_activate=on_activate_handler,
        on_release=on_release_handler,
        on_drag=on_drag_handler,
        on_alt_press=on_alt_press_handler,
        on_alt_release=on_alt_release_handler,
        on_alt_drag=on_alt_drag_handler,
        flex=1,
    )


@pytest.fixture
async def canvas(widget, probe, on_resize_handler):
    # Modify the base canvas fixture to make it more useful for drawing tests.
    widget.style.background_color = WHITE
    widget.style.width = 200
    widget.style.height = 200
    return widget
