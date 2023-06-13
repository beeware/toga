from unittest.mock import Mock

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
async def on_scroll():
    return Mock()


@pytest.fixture
async def widget(content, on_scroll):
    return toga.ScrollContainer(
        content=content, style=Pack(flex=1), on_scroll=on_scroll
    )


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


async def test_enable_horizontal_scrolling(widget, probe, content, on_scroll):
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

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.horizontal_position = 120
    await probe.wait_for_scroll_completion()
    await probe.redraw("Horizontal scroll was allowed")
    assert widget.horizontal_position == 120
    on_scroll.assert_called_with(widget)


async def test_enable_vertical_scrolling(widget, probe, on_scroll):
    widget.vertical = False
    await probe.redraw("Vertical scrolling is disabled")

    assert widget.vertical_position is None
    assert widget.max_vertical_position is None
    with pytest.raises(ValueError):
        widget.vertical_position = 120

    widget.vertical = True
    await probe.redraw("Vertical scrolling is enabled")

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.vertical_position = 120
    await probe.wait_for_scroll_completion()
    await probe.redraw("Vertical scroll was allowed")
    assert widget.vertical_position == 120
    on_scroll.assert_called_with(widget)


async def test_vertical_scroll(widget, probe, on_scroll):
    "The widget can be scrolled vertically."
    assert probe.document_width == probe.width
    assert probe.document_height == 6000

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 6000 - probe.height

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.vertical_position = probe.height * 3
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll down 3 pages")
    assert widget.vertical_position == probe.height * 3
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.vertical_position = 0
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll back to origin")
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.vertical_position = 10000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll past the end")
    assert widget.vertical_position == widget.max_vertical_position
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.vertical_position = -100
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll past the start")
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()


async def test_vertical_scroll_small_content(widget, probe, small_content, on_scroll):
    "The widget can be scrolled vertically when the content doesn't need scrolling."
    widget.content = small_content
    await probe.redraw("Content has been switched for a small document")

    assert probe.document_width == probe.width
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.vertical_position = probe.height * 3
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll down 3 pages")
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.vertical_position = 0
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll back to origin")
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()


async def test_horizontal_scroll(widget, probe, content, on_scroll):
    "The widget can be scrolled horizontally."
    content.style.direction = ROW
    await probe.redraw("Content has been switched for a wide document")

    assert probe.document_width == 20000
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 20000 - probe.width
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.horizontal_position = probe.height * 3
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll down 3 pages")
    assert widget.horizontal_position == probe.height * 3
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.horizontal_position = 0
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll back to origin")
    assert widget.horizontal_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.horizontal_position = 30000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll past the end")
    assert widget.horizontal_position == widget.max_horizontal_position
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.horizontal_position = -100
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll past the start")
    assert widget.horizontal_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()


async def test_horizontal_scroll_small_content(widget, probe, small_content, on_scroll):
    "The widget can be scrolled horizontally when the content doesn't need scrolling."
    small_content.style.direction = ROW
    widget.content = small_content
    await probe.redraw("Content has been switched for a small wide document")

    assert probe.document_width == probe.width
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.horizontal_position = probe.height * 3
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll down 3 pages")
    assert widget.horizontal_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.horizontal_position = 0
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll back to origin")
    assert widget.horizontal_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()


async def test_scroll_both(widget, probe, content, on_scroll):
    "The widget can be scrolled in both axes."
    # Add some wide content
    content.add(
        toga.Label(
            "This is a long label",
            style=Pack(
                width=2000,
                background_color=CORNFLOWERBLUE,
                padding=20,
                height=20,
            ),
        )
    )
    await probe.redraw("Content has been modified to be wide as well as tall")
    assert probe.document_width == 2040
    assert probe.document_height == 6060

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.horizontal_position = 1000
    widget.vertical_position = 2000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll to mid document")
    assert widget.horizontal_position == 1000
    assert widget.vertical_position == 2000
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.horizontal_position = 0
    widget.vertical_position = 20000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll to bottom left")
    assert widget.horizontal_position == 0
    assert widget.vertical_position == 6060 - probe.height
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.horizontal_position = 10000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll to bottom right")
    assert widget.horizontal_position == 2040 - probe.width
    assert widget.vertical_position == 6060 - probe.height
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()


async def test_manual_scroll(widget, probe, content, on_scroll):
    "The widget can be scrolled manually."
    await probe.scroll()
    await probe.wait_for_scroll_completion()
    await probe.redraw("Widget has been manually scrolled manually")
    assert widget.horizontal_position == 0

    # We don't care where it's been scrolled to; and there may have been
    # multiple scroll events.
    assert widget.vertical_position > 0
    on_scroll.assert_called_with(widget)
