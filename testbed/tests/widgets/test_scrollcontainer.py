from unittest.mock import Mock

import pytest
from pytest import approx

import toga
from toga.colors import CORNFLOWERBLUE, REBECCAPURPLE, TRANSPARENT
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
        style=Pack(
            direction=COLUMN,
            # Ensure we can see the background of the scroll container
            background_color=TRANSPARENT,
        ),
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
    assert probe.document_width == probe.width - probe.scrollbar_inset
    assert probe.document_height == approx(6000, abs=1)

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


async def test_padding(widget, probe, content):
    "Padding works correctly on the root widget"
    original_width = probe.width
    original_height = probe.height
    original_document_width = probe.document_width
    original_document_height = probe.document_height

    content.style.padding = 21
    await probe.redraw("Add padding")
    assert probe.width == original_width
    assert probe.height == original_height
    assert probe.document_width == original_document_width
    assert probe.document_height == original_document_height + 42

    content.style.padding = 0
    await probe.redraw("Remove padding")
    assert probe.width == original_width
    assert probe.height == original_height
    assert probe.document_width == original_document_width
    assert probe.document_height == original_document_height


async def test_enable_horizontal_scrolling(widget, probe, content, on_scroll):
    "Horizontal scrolling can be disabled"
    # Add some wide content
    content.insert(
        0,
        toga.Label(
            "This is a long label",
            style=Pack(
                width=2000,
                background_color=CORNFLOWERBLUE,
                padding=20,
                height=20,
            ),
        ),
    )

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    # Disable horizontal scrolling
    widget.horizontal = False
    await probe.redraw("Horizontal scrolling is disabled")

    assert widget.horizontal_position == 0
    assert widget.max_horizontal_position == 0

    # Setting *just* the horizontal position is an error
    with pytest.raises(ValueError):
        widget.horizontal_position = 120

    # If setting a *full* position, the horizontal coordinate is ignored.
    widget.position = (120, 200)
    await probe.wait_for_scroll_completion()
    await probe.redraw("Horizontal scroll distance is ignored")

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 200
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    # If horizontal scrolling is disabled, you can still set the vertical position.
    widget.vertical_position = 0
    await probe.wait_for_scroll_completion()
    await probe.redraw("Vertical position has been set")

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.horizontal = True
    await probe.redraw("Horizontal scrolling is enabled")

    widget.horizontal_position = 120
    await probe.wait_for_scroll_completion()
    await probe.redraw("Horizontal scroll was allowed")
    assert widget.horizontal_position == 120
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    # Disabling horizontal scrolling resets horizontal position and emits an event.
    widget.horizontal = False
    await probe.wait_for_scroll_completion()
    await probe.redraw("Horizontal scrolling is disabled again")
    assert widget.horizontal_position == 0
    on_scroll.assert_called_with(widget)


async def test_enable_vertical_scrolling(widget, probe, content, on_scroll):
    "Vertical scrolling can be disabled"
    # Add some wide content
    content.insert(
        0,
        toga.Label(
            "This is a long label",
            style=Pack(
                width=2000,
                background_color=CORNFLOWERBLUE,
                padding=20,
                height=20,
            ),
        ),
    )

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.vertical = False
    await probe.redraw("Vertical scrolling is disabled")

    assert widget.vertical_position == 0
    assert widget.max_vertical_position == 0

    # Setting *just* the vertical position is an error
    with pytest.raises(ValueError):
        widget.vertical_position = 120

    # If setting a *full* position, the vertical coordinate is ignored.
    widget.position = (120, 200)
    await probe.wait_for_scroll_completion()
    await probe.redraw("Vertical scroll distance is ignored")

    assert widget.horizontal_position == 120
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    # If vertical scrolling is disabled, you can still set the horizontal position.
    widget.horizontal_position = 0
    await probe.wait_for_scroll_completion()
    await probe.redraw("Horizontal position has been set")

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.vertical = True
    await probe.redraw("Vertical scrolling is enabled")

    widget.vertical_position = 120
    await probe.wait_for_scroll_completion()
    await probe.redraw("Vertical scroll was allowed")
    assert widget.vertical_position == 120
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.vertical = False
    await probe.wait_for_scroll_completion()
    await probe.redraw("Vertical scrolling is disabled again")
    assert widget.vertical_position == 0
    on_scroll.assert_called_with(widget)


async def test_vertical_scroll(widget, probe, on_scroll):
    "The widget can be scrolled vertically."
    assert probe.document_width == probe.width - probe.scrollbar_inset
    assert probe.document_height > probe.height
    assert probe.document_height == approx(6000, abs=1)

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == approx(
        probe.document_height - probe.height, abs=1
    )
    assert isinstance(widget.max_vertical_position, int)

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


async def test_vertical_scroll_small_content(widget, probe, small_content):
    "When the content doesn't need vertical scrolling, attempts to scroll are ignored"
    widget.content = small_content
    await probe.redraw("Content has been switched for a small document")

    assert probe.document_width == probe.width
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # This doesn't change the position, so whether it calls on_scroll is undefined.
    widget.vertical_position = probe.height * 3
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll down 3 pages")
    assert widget.vertical_position == 0


async def test_horizontal_scroll(widget, probe, content, on_scroll):
    "The widget can be scrolled horizontally."
    content.style.direction = ROW
    await probe.redraw("Content has been switched for a wide document")

    assert probe.document_width > probe.width
    assert probe.document_width == approx(20000, abs=1)
    assert probe.document_height == probe.height - probe.scrollbar_inset

    assert widget.max_horizontal_position == approx(
        probe.document_width - probe.width, abs=1
    )
    assert isinstance(widget.max_horizontal_position, int)
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.horizontal_position = probe.width * 3
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll right a little")
    assert widget.horizontal_position == probe.width * 3
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


async def test_horizontal_scroll_small_content(widget, probe, small_content):
    "When the content doesn't need horizontal scrolling, attempts to scroll are ignored"
    small_content.style.direction = ROW
    widget.content = small_content
    await probe.redraw("Content has been switched for a small wide document")

    assert probe.document_width == probe.width
    assert probe.document_height == probe.height

    assert widget.max_horizontal_position == 0
    assert widget.max_vertical_position == 0

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # This doesn't change the position, so whether it calls on_scroll is undefined.
    widget.horizontal_position = probe.height * 3
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll right 3 pages")
    assert widget.horizontal_position == 0


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
    assert probe.document_height == approx(6060, abs=1)

    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0

    # clear any scroll events caused by setup
    on_scroll.reset_mock()

    widget.position = 1000, 2000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll to mid document")
    assert widget.horizontal_position == 1000
    assert isinstance(widget.horizontal_position, int)
    assert widget.vertical_position == 2000
    assert isinstance(widget.vertical_position, int)
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.position = 0, 20000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll to bottom left")
    assert widget.horizontal_position == 0
    assert widget.vertical_position == approx(
        probe.document_height - probe.height + probe.scrollbar_inset, abs=1
    )
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()

    widget.position = 10000, 20000
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll to bottom right")
    assert widget.horizontal_position == approx(
        probe.document_width - probe.width + probe.scrollbar_inset, abs=1
    )
    assert widget.vertical_position == approx(
        probe.document_height - probe.height + probe.scrollbar_inset, abs=1
    )
    on_scroll.assert_called_with(widget)
    on_scroll.reset_mock()


async def test_manual_scroll(widget, probe, content, on_scroll):
    "The widget can be scrolled manually."
    await probe.scroll()
    await probe.wait_for_scroll_completion()
    await probe.redraw("Widget has been scrolled manually")
    assert widget.horizontal_position == 0

    # We don't care where it's been scrolled to; and there may have been
    # multiple scroll events.
    assert widget.vertical_position > 0
    on_scroll.assert_called_with(widget)

    # Disabling scrolling should scroll back to zero
    widget.vertical = False
    await probe.wait_for_scroll_completion()
    await probe.redraw("Scroll back to origin, and disable scrolling")
    assert widget.vertical_position == 0
    on_scroll.reset_mock()

    # With scrolling disabled, `scroll` method should have no effect.
    await probe.scroll()
    await probe.wait_for_scroll_completion()
    await probe.redraw("Attempted scroll with scrolling disabled")
    assert widget.horizontal_position == 0
    assert widget.vertical_position == 0
    on_scroll.assert_not_called()


async def test_no_content(widget, probe, content):
    "The content of the scroll container can be cleared"
    widget.content = None
    await probe.redraw("Content of the scroll container has been cleared")

    # Force a refresh to see the impact of a set_bounds() when there's
    # no inner content.
    widget.refresh()
    await probe.redraw("Scroll container layout has been refreshed")

    widget.content = content
    await probe.redraw("Content of the scroll container has been restored")

    widget.refresh()
    await probe.redraw("Scroll container layout has been refreshed")
