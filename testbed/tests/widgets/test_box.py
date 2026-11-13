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
        (COLUMN, START, (120, 48), (0, 0)),
        (COLUMN, CENTER, (120, 48), (120, 0)),
        (COLUMN, END, (120, 48), (240, 0)),
        (ROW, START, (40, 120), (0, 0)),
        (ROW, CENTER, (40, 120), (0, 120)),
        (ROW, END, (40, 120), (0, 240)),
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
        width=360,
        height=360,
        align_items=alignment,
    )
    child = toga.Box(width=child_size[0], height=child_size[1])
    widget.add(child)
    child_probe = get_probe(child)

    await probe.redraw("Child aligned within the explicitly sized box")

    probe.assert_layout(position=(0, 0), size=(360, 360))
    child_probe.assert_layout(position=position, size=child_size)
