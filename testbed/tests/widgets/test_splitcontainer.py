import pytest
from pytest import approx

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE
from toga.constants import Direction
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

    # Clear content2, but keep the split proportion.
    widget.content = [(None, 2), (content3, 3)]
    await probe.wait_for_split()
    await probe.redraw("Content should have a 40:60 split, but only right content")
    assert content3_probe.width == pytest.approx(probe.width * 3 / 5, abs=20)

    # Bring back content2, and drop content 3
    widget.content = [content2, None]
    await probe.wait_for_split()
    await probe.redraw("Content should have a 50:50 split, but only left content")
    assert content2_probe.width == pytest.approx(probe.width / 2, abs=20)


async def test_set_direction(
    widget,
    probe,
    content1,
    content1_probe,
    content2,
    content2_probe,
):
    """Splitview direction can be changed"""
    two_borders = probe.border_size * 2

    def assert_full_width():
        expected = approx(probe.width - two_borders, abs=1)
        assert content1_probe.width == expected
        assert content2_probe.width == expected

    def assert_full_height():
        expected = approx(probe.height - two_borders, abs=1)
        assert content1_probe.height == expected
        assert content2_probe.height == expected

    def assert_split_width(flex1, flex2):
        total = flex1 + flex2
        assert content1_probe.width == approx(probe.width * flex1 / total, abs=20)
        assert content2_probe.width == approx(probe.width * flex2 / total, abs=20)

    def assert_split_height(flex1, flex2):
        total = flex1 + flex2
        assert content1_probe.height == approx(probe.height * flex1 / total, abs=20)
        assert content2_probe.height == approx(probe.height * flex2 / total, abs=20)

    assert_full_height()
    assert_split_width(1, 1)

    widget.direction = Direction.HORIZONTAL
    await probe.wait_for_split()
    await probe.redraw("Split should now be horizontal")

    assert_full_width()
    if probe.direction_change_preserves_position:
        assert_split_height(1, 1)

    widget.content = [(content1, 3), (content2, 1)]
    await probe.wait_for_split()
    await probe.redraw("Split should be a horizontal 75:25 split")

    assert_full_width()
    assert_split_height(3, 1)

    widget.direction = Direction.VERTICAL
    await probe.wait_for_split()
    await probe.redraw("Split should now be vertical again")

    assert_full_height()
    if probe.direction_change_preserves_position:
        assert_split_width(3, 1)


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
