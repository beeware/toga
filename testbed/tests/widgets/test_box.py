import pytest

import toga
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, END, ROW, START

from .conftest import build_cleanup_test
from .probe import get_probe
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
async def widget():
    return toga.Box(style=Pack(width=100, height=200))


test_cleanup = build_cleanup_test(toga.Box)


@pytest.mark.parametrize(
    "direction, alignment, child_size, position",
    [
        (COLUMN, START, (100, 20), (0, 0)),
        (COLUMN, CENTER, (100, 20), (100, 0)),
        (COLUMN, END, (100, 20), (200, 0)),
        (ROW, START, (20, 100), (0, 0)),
        (ROW, CENTER, (20, 100), (0, 100)),
        (ROW, END, (20, 100), (0, 200)),
    ],
)
async def test_explicit_cross_axis_alignment(
    widget,
    probe,
    direction,
    alignment,
    child_size,
    position,
):
    """Children align within the explicit size under an opposite-direction parent."""
    widget.parent.style.direction = ROW if direction == COLUMN else COLUMN
    widget.style.update(
        direction=direction,
        width=300,
        height=300,
        align_items=alignment,
    )
    child = toga.Box(width=child_size[0], height=child_size[1])
    widget.add(child)
    child_probe = get_probe(child)

    await probe.redraw("Child aligned within the explicitly sized box")

    probe.assert_layout(position=(0, 0), size=(300, 300))
    child_probe.assert_layout(position=position, size=child_size)
