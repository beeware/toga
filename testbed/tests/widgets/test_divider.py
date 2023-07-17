import pytest

import toga
from toga.constants import Direction
from toga.style.pack import COLUMN, ROW

from ..conftest import skip_on_platforms
from .properties import (  # noqa: F401
    test_enable_noop,
    test_focus_noop,
)


@pytest.fixture
async def widget():
    skip_on_platforms("android", "iOS")
    return toga.Divider()


async def test_directions(widget, probe):
    "The divider has the right size as direction is changed"
    # Widget should be initially horizontal.
    # Container is initially a row box, so the divider will be
    # both narrow and short
    assert widget.direction == Direction.HORIZONTAL
    assert probe.height < 10
    assert probe.width < 10

    # Make the container a column box so the divider will become wide.
    widget.parent.style.direction = COLUMN
    await probe.redraw("Divider should become wide")

    # The divider will now be wide, but short.
    assert widget.direction == Direction.HORIZONTAL
    assert probe.height < 10
    assert probe.width > 100

    # Make the divider vertical
    widget.direction = Direction.VERTICAL
    await probe.redraw("Divider should be VERTICAL")

    # In a column box, a vertical divider will be narrow and short.
    assert widget.direction == Direction.VERTICAL
    assert probe.height < 10
    assert probe.width < 10

    # Make the container a row box again so the divider will become tall.
    widget.parent.style.direction = ROW
    await probe.redraw("Divider should become tall")

    # In a row box, a vertical divider will be narrow and tall.
    assert widget.direction == Direction.VERTICAL
    assert probe.height > 100
    assert probe.width < 10

    # Make the divider horizontal
    widget.direction = Direction.HORIZONTAL
    await probe.redraw("Divider should be HORIZONTAL")

    # In a row box, a horizontal divider will be narrow and short.
    assert widget.direction == Direction.HORIZONTAL
    assert probe.height < 10
    assert probe.width < 10

    # Make the container a COLUMN box again
    widget.parent.style.direction = COLUMN
    await probe.redraw("Divider should become wide")

    # In a column box, a horizontal divider will be narrow and short.
    assert widget.direction == Direction.HORIZONTAL
    assert probe.height < 10
    assert probe.width > 100
