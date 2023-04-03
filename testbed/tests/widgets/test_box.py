import pytest

import toga
from toga.colors import BLACK, BLUE, GREEN, RED
from toga.style import Pack

from .probe import get_probe
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
async def widget():
    return toga.Box(style=Pack(width=100, height=200))


async def test_parenting(widget, probe):
    widget.style.background_color = RED
    box = widget.parent

    child = toga.Box(style=Pack(width=50, height=75, background_color=GREEN))
    child_probe = get_probe(child)
    other = toga.Box(style=Pack(width=100, height=200, background_color=BLUE))
    other_probe = get_probe(other)
    other_child = toga.Box(style=Pack(width=25, height=50, background_color=BLACK))
    other.add(other_child)

    # Layout has the test widget, plus other, horizontally laid out.
    # Child isn't in the layout yet.
    box.add(other)
    await probe.redraw()
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_not_contained()

    # Add child to widget.
    widget.add(child)
    await probe.redraw()
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_layout(position=(0, 0), size=(50, 75))

    # Reparent child to other without removing first
    other.add(child)
    await probe.redraw()
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_layout(position=(125, 0), size=(50, 75))

    # Remove child from the layout entirely
    other.remove(child)
    await probe.redraw()
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_not_contained()

    # Insert the child into the root layout
    box.insert(1, child)
    await probe.redraw()
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(150, 0), size=(100, 200))
    child_probe.assert_layout(position=(100, 0), size=(50, 75))
