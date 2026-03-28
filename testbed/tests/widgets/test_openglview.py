from unittest.mock import Mock

import pytest

import toga

# from .probe import get_probe
from .properties import (  # noqa: F401
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
def renderer():
    renderer = Mock()
    return renderer


# Widget fixture must be async to force OpenGL to be
# initialized on the main thread
@pytest.fixture
async def widget(renderer):
    return toga.OpenGLView(renderer, flex=1)


async def test_callbacks(probe, widget, renderer):
    renderer.on_init.assert_called_once_with(widget)
    await probe.redraw("OpenGlView widget initialized", 0.1)

    # different backends render different numbers of times with
    # different arguments
    renderer.on_render.assert_called()
    assert renderer.on_render.call_args[0] == (widget,)
    assert "size" in renderer.on_render.call_args[1]
    assert isinstance(renderer.on_render.call_args[1]["size"], tuple)
    assert len(renderer.on_render.call_args[1]["size"]) == 2

    renderer.reset_mock()

    widget.redraw()
    await probe.redraw("OpenGlView widget redraw requested", 0.1)
    renderer.on_render.assert_called()
    assert renderer.on_render.call_args[0] == (widget,)
    assert "size" in renderer.on_render.call_args[1]
    assert isinstance(renderer.on_render.call_args[1]["size"], tuple)
    assert len(renderer.on_render.call_args[1]["size"]) == 2
