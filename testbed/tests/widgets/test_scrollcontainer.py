import pytest

import toga
from toga.colors import CORNFLOWERBLUE, REBECCAPURPLE
from toga.style.pack import COLUMN, ROW, Pack

from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
async def content():
    box = toga.Box(
        children=[
            toga.Label(
                f"I am line {i}",
                style=Pack(
                    padding=20,
                    height=20,
                    width=160,
                    background_color=CORNFLOWERBLUE if i % 2 else REBECCAPURPLE,
                ),
            )
            for i in range(0, 100)
        ],
        style=Pack(direction=COLUMN),
    )
    return box


@pytest.fixture
async def small_content():
    box = toga.Box(
        children=[
            toga.Label(
                "I am content",
                style=Pack(
                    padding=20,
                    height=20,
                    width=160,
                    background_color=CORNFLOWERBLUE,
                ),
            )
        ],
        style=Pack(direction=COLUMN),
    )
    return box


@pytest.fixture
async def widget(content):
    return toga.ScrollContainer(content=content, style=Pack(flex=1))


async def test_clear_content(widget, probe, small_content):
    "Widget content can be cleared and reset"
    assert probe.document_width == probe.width
    assert probe.document_height == 6000

    widget.content = None
    await probe.redraw("Widget content has been cleared")
    assert not probe.has_content

    widget.content = None
    await probe.redraw("Widget content has been re-cleared")
    assert not probe.has_content

    widget.content = small_content
    await probe.redraw("Widget content has been restored")
    assert probe.has_content
    assert probe.document_width == probe.width
    assert probe.document_height == probe.height


async def test_enable_horizontal_scrolling(widget, probe, content):
    "Horizontal scrolling can be disabled"
    content.style.direction = ROW

    widget.horizontal = False
    await probe.redraw("Horizontal scrolling is disabled")

    assert widget.horizontal_position is None
    assert widget.max_horizontal_position is None
    with pytest.raises(ValueError):
        widget.horizontal_position = 120

    widget.horizontal = True
    await probe.redraw("Horizontal scrolling is enabled")

    widget.horizontal_position = 120
    await probe.redraw("Horizontal scroll was allowed")
    assert widget.horizontal_position == 120


async def test_enable_vertical_scrolling(widget, probe):
    widget.vertical = False
    await probe.redraw("Vertical scrolling is disabled")

    assert widget.vertical_position is None
    assert widget.max_vertical_position is None
    with pytest.raises(ValueError):
        widget.vertical_position = 120

    widget.vertical = True
    await probe.redraw("Vertical scrolling is enabled")

    widget.vertical_position = 120
    await probe.redraw("Vertical scroll was allowed")
    assert widget.vertical_position == 120


async def test_vertical_scroll(widget, probe):
    "The widget can be scrolled vertically."
    assert probe.document_width == probe.width
    assert probe.document_height == 6000

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 6000 - probe.height

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    widget.vertical_position = probe.height * 3
    await probe.redraw("Scroll down 3 pages")
    assert widget.vertical_position == probe.height * 3

    widget.vertical_position = 0
    await probe.redraw("Scroll back to origin")
    assert widget.vertical_position == 0

    widget.vertical_position = 10000
    await probe.redraw("Scroll past the end")
    assert widget.vertical_position == widget.max_vertical_position

    widget.vertical_position = -100
    await probe.redraw("Scroll past the start")
    assert widget.vertical_position == 0


async def test_vertical_scroll_small_content(widget, probe, small_content):
    "The widget can be scrolled vertically when the content doesn't need scrolling."
    widget.content = small_content

    assert probe.document_width == probe.width
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    widget.vertical_position = probe.height * 3
    await probe.redraw("Scroll down 3 pages")
    assert widget.vertical_position == 0

    widget.vertical_position = 0
    await probe.redraw("Scroll back to origin")
    assert widget.vertical_position == 0


async def test_horizontal_scroll(widget, probe, content):
    "The widget can be scrolled horizontally."
    content.style.direction = ROW

    assert probe.document_width == 20000
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 20000 - probe.width
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    widget.horizontal_position = probe.height * 3
    await probe.redraw("Scroll down 3 pages")
    assert widget.horizontal_position == probe.height * 3

    widget.horizontal_position = 0
    await probe.redraw("Scroll back to origin")
    assert widget.horizontal_position == 0

    widget.horizontal_position = 30000
    await probe.redraw("Scroll past the end")
    assert widget.horizontal_position == widget.max_horizontal_position

    widget.horizontal_position = -100
    await probe.redraw("Scroll past the start")
    assert widget.horizontal_position == 0


async def test_horizontal_scroll_small_content(widget, probe, small_content):
    "The widget can be scrolled horizontally when the content doesn't need scrolling."
    small_content.style.direction = ROW
    widget.content = small_content

    assert probe.document_width == probe.width
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    widget.horizontal_position = probe.height * 3
    await probe.redraw("Scroll down 3 pages")
    assert widget.horizontal_position == 0

    widget.horizontal_position = 0
    await probe.redraw("Scroll back to origin")
    assert widget.horizontal_position == 0
