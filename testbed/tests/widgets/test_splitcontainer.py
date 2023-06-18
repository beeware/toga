import pytest

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE
from toga.style.pack import Pack

from ..conftest import xfail_on_platforms
from .probe import get_probe
from .properties import (  # noqa: F401
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
async def content1():
    return toga.Box(
        children=[toga.Label("Box 1 content", style=Pack(flex=1))],
        style=Pack(background_color=REBECCAPURPLE),
    )


@pytest.fixture
async def content2():
    return toga.Box(
        children=[toga.Label("Box 2 content", style=Pack(flex=1))],
        style=Pack(background_color=CORNFLOWERBLUE),
    )


@pytest.fixture
async def content3():
    return toga.Box(
        children=[toga.Label("Box 3 content", style=Pack(flex=1))],
        style=Pack(background_color=GOLDENROD),
    )


@pytest.fixture
async def content1_probe(content1):
    return get_probe(content1)


@pytest.fixture
async def content2_probe(content2):
    return get_probe(content2)


@pytest.fixture
async def content3_probe(content3):
    return get_probe(content3)


@pytest.fixture
async def widget(content1, content2):
    xfail_on_platforms("android", "iOS")
    return toga.SplitContainer(content=[content1, content2], style=Pack(flex=1))


async def test_set_content(
    widget,
    probe,
    content1_probe,
    content2,
    content2_probe,
    content3,
    content3_probe,
):
    """Splitview content can be changed"""
    # Both widgets are initially within 20px of an even split
    assert content1_probe.width == pytest.approx(probe.width / 2, abs=20)
    assert content2_probe.width == pytest.approx(probe.width / 2, abs=20)

    # Move content2 to the first panel, replace the second panel with content3
    # and apply an uneven content split.
    widget.content = [(content2, 2), (content3, 3)]
    await probe.wait_for_split()
    await probe.redraw("Content should have a 40:60 split")
    assert content2_probe.width == pytest.approx(probe.width * 2 / 5, abs=20)
    assert content3_probe.width == pytest.approx(probe.width * 3 / 5, abs=20)


async def test_set_direction(
    widget,
    probe,
    content1,
    content1_probe,
    content2,
    content2_probe,
):
    """Splitview direction can be changed"""
    # Both widgets are initially within 20px of an even split horizontally
    assert content1_probe.width == pytest.approx(probe.width / 2, abs=20)
    assert content2_probe.width == pytest.approx(probe.width / 2, abs=20)

    # Both widgets are the height of the outer container
    assert content1_probe.height == probe.height
    assert content2_probe.height == probe.height

    widget.direction = toga.SplitContainer.HORIZONTAL
    await probe.wait_for_split()
    await probe.redraw("Split should now be horizontal")

    # Both widgets are the width of the outer container
    assert content1_probe.width == probe.width
    assert content2_probe.width == probe.width
    # Widget height is not determinate

    widget.content = [(content1, 3), (content2, 1)]
    await probe.wait_for_split()
    await probe.redraw("Split should be a horizontal 75:25 split")

    # Both widgets are the width of the outer container
    assert content1_probe.width == probe.width
    assert content2_probe.width == probe.width

    # The heights have a 75/25 split
    assert content1_probe.height == pytest.approx(probe.height * 3 / 4, abs=20)
    assert content2_probe.height == pytest.approx(probe.height * 1 / 4, abs=20)

    widget.direction = toga.SplitContainer.VERTICAL
    await probe.wait_for_split()
    await probe.redraw("Split should now be vertical again")

    # Widget width is not determinate
    # Both widgets are the height of the outer container
    assert content1_probe.height == probe.height
    assert content2_probe.height == probe.height


async def test_move_splitter(
    widget,
    probe,
    content1_probe,
    content2_probe,
):
    """Splitview position can be manually changed"""
    # Both widgets are initially within 20px of an even split horizontally
    assert content1_probe.width == pytest.approx(probe.width / 2, abs=20)
    assert content2_probe.width == pytest.approx(probe.width / 2, abs=20)

    probe.move_split(400)
    await probe.wait_for_split()
    await probe.redraw("Split has been moved right")

    # Content1 is now 400 pixels wide.
    assert content1_probe.width == pytest.approx(400, abs=20)
    assert content2_probe.width == pytest.approx(probe.width - 400, abs=20)

    # Try to move the splitter to the very end.
    probe.move_split(probe.width)
    await probe.wait_for_split()
    await probe.redraw("Split has been moved past the minimum size limit")

    # Content2 is not 0 sized.
    assert content2_probe.width > 50
