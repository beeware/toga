import pytest

import toga
from toga.style.pack import COLUMN, ROW

from ..conftest import skip_on_platforms


@pytest.fixture
async def widget():
    skip_on_platforms("android", "iOS")
    return toga.Divider()


async def test_directions(widget, probe):
    "The divider has the right size as direction is changed"
    # Widget should be initially horizontal.
    # Container is initially a row box, so the divider will be
    # both narrow and short
    assert widget.direction == toga.Divider.HORIZONTAL
    assert probe.height < 10
    assert probe.width < 10

    # Make the container a column box so the divider will become wide.
    widget.parent.style.direction = COLUMN
    await probe.redraw()

    # The divider will now be wide, but short.
    assert widget.direction == toga.Divider.HORIZONTAL
    assert probe.height < 10
    assert probe.width > 100

    # Make the divider vertical
    widget.direction = toga.Divider.VERTICAL
    await probe.redraw()

    # In a column box, a vertical divider will be narrow and short.
    assert widget.direction == toga.Divider.VERTICAL
    assert probe.height < 10
    assert probe.width < 10

    # Make the container a row box again so the divider will become tall.
    widget.parent.style.direction = ROW
    await probe.redraw()

    # In a row box, a vertical divider will be narrow and tall.
    assert widget.direction == toga.Divider.VERTICAL
    assert probe.height > 100
    assert probe.width < 10
