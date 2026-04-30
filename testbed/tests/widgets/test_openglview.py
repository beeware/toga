from itertools import chain, combinations
from unittest.mock import Mock

import pytest

import toga

from ..conftest import skip_on_platforms
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
    skip_on_platforms("windows")
    return toga.OpenGLView(renderer, flex=1)


async def test_callbacks(probe, widget, renderer):
    await probe.redraw("OpenGLView widget created", 0.1)
    renderer.on_init.assert_called_once_with(widget)
    await probe.redraw("OpenGLView widget initialized", 0.1)

    # different backends render different numbers of times
    renderer.on_render.assert_called()
    assert renderer.on_render.call_args[0] == (widget,)
    assert "size" in renderer.on_render.call_args[1]
    assert isinstance(renderer.on_render.call_args[1]["size"], tuple)
    assert len(renderer.on_render.call_args[1]["size"]) == 2
    assert "pointer" in renderer.on_render.call_args[1]
    if renderer.on_render.call_args[1]["pointer"] is not None:
        assert isinstance(renderer.on_render.call_args[1]["pointer"], tuple)
        assert len(renderer.on_render.call_args[1]["pointer"]) == 2
    assert "buttons" in renderer.on_render.call_args[1]
    assert renderer.on_render.call_args[1]["buttons"] == frozenset()

    renderer.reset_mock()

    widget.redraw()
    await probe.redraw("OpenGLView widget redraw requested", 0.1)
    renderer.on_render.assert_called()
    assert renderer.on_render.call_args[0] == (widget,)
    assert "size" in renderer.on_render.call_args[1]
    assert isinstance(renderer.on_render.call_args[1]["size"], tuple)
    assert len(renderer.on_render.call_args[1]["size"]) == 2
    assert "pointer" in renderer.on_render.call_args[1]
    if renderer.on_render.call_args[1]["pointer"] is not None:
        assert isinstance(renderer.on_render.call_args[1]["pointer"], tuple)
        assert len(renderer.on_render.call_args[1]["pointer"]) == 2
    assert "buttons" in renderer.on_render.call_args[1]
    assert renderer.on_render.call_args[1]["buttons"] == frozenset()


async def test_buttons(probe, widget, renderer):
    if not probe.buttons:
        pytest.skip("Backend does not support buttons.")

    await probe.redraw("OpenGLView widget initialized", 0.1)

    button_states = [
        frozenset(combination)
        for combination in chain.from_iterable(
            combinations(probe.buttons, r) for r in range(len(probe.buttons) + 1)
        )
    ]
    for buttons in button_states:
        await probe.reset_buttons()
        await probe.redraw("Reset buttons", 0.01)
        renderer.on_render.reset_mock()

        await probe.button_state(buttons)
        await probe.redraw(f"Mouse events sent {buttons}", 0.01)
        widget.redraw()
        await probe.redraw("OpenGLView widget redraw requested", 0.1)

        assert renderer.on_render.call_args[0] == (widget,)
        assert "size" in renderer.on_render.call_args[1]
        assert isinstance(renderer.on_render.call_args[1]["size"], tuple)
        assert len(renderer.on_render.call_args[1]["size"]) == 2

        assert "buttons" in renderer.on_render.call_args[1]
        assert isinstance(renderer.on_render.call_args[1]["buttons"], frozenset)
        assert renderer.on_render.call_args[1]["buttons"] == buttons

        assert "pointer" in renderer.on_render.call_args[1]
        assert renderer.on_render.call_args[1]["pointer"] == (0, 0)


async def test_pointer(probe, widget, renderer):
    if not probe.buttons:
        pytest.skip("Backend does not support buttons.")

    await probe.redraw("OpenGLView widget initialized", 0.1)

    # generate a pointer move event
    await probe.position_change(10, 10)
    await probe.redraw("Pointer changed", 0.01)

    # redraw the view
    widget.redraw()
    await probe.redraw("OpenGLView widget redraw requested", 0.1)

    # pointer should reflect the new position
    assert renderer.on_render.call_args[0] == (widget,)
    assert "pointer" in renderer.on_render.call_args[1]
    assert renderer.on_render.call_args[1]["pointer"] == (0, 0)
