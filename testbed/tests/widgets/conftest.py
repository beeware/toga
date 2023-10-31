from unittest.mock import Mock

from pytest import fixture

import toga
from toga.style.pack import TOP

from .probe import get_probe


@fixture
async def widget():
    raise NotImplementedError("test modules must define a `widget` fixture")


@fixture
async def probe(main_window, widget):
    old_content = main_window.content

    box = toga.Box(children=[widget])
    main_window.content = box
    probe = get_probe(widget)
    await probe.redraw(f"\nConstructing {widget.__class__.__name__} probe")
    probe.assert_container(box)
    yield probe

    main_window.content = old_content


@fixture
async def container_probe(widget):
    return get_probe(widget.parent)


@fixture
async def other(widget):
    """A separate widget that can take focus"""
    other = toga.TextInput()
    widget.parent.add(other)
    return other


@fixture
async def other_probe(other):
    return get_probe(other)


@fixture(params=[True, False])
async def focused(request, widget, other):
    if request.param:
        widget.focus()
    else:
        other.focus()
    return request.param


@fixture
async def on_change(widget):
    on_change = Mock()
    widget.on_change = on_change
    on_change.assert_not_called()
    return on_change


@fixture
def verify_font_sizes():
    """Whether the widget's width and height are affected by font size"""
    return True, True


@fixture
def verify_focus_handlers():
    """Whether the widget has on_gain_focus and on_lose_focus handlers"""
    return False


@fixture
def verify_vertical_alignment():
    """The widget's default vertical alignment"""
    return TOP
