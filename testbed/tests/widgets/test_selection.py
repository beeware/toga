from unittest.mock import Mock

import pytest

import toga
from toga.sources import ListSource

from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
    test_focus,
    test_font,
    test_font_attrs,
)


@pytest.fixture
async def widget():
    return toga.Selection(items=["first", "second", "third"])


async def test_item_titles(widget, probe):
    """The selection is able to build display titles from a range of data types"""
    on_change_handler = Mock()
    widget.on_change = on_change_handler

    for items, display, selection, selected_title in [
        # Empty list
        ([], [], None, None),
        # List of strings
        (
            ["first", "second", "third"],
            ["first", "second", "third"],
            "first",
            "first",
        ),
        # List of ints, converted to string
        ([111, 222, 333], ["111", "222", "333"], 111, "111"),
        # List of tuples; first item is taken
        (
            [
                ("first", 111),
                ("second", 222),
                ("third", 333),
            ],
            ["first", "second", "third"],
            "first",
            "first",
        ),
        # List of dicts with a "value" ley
        (
            [
                {"name": "first", "value": 111},
                {"name": "second", "value": 222},
                {"name": "third", "value": 333},
            ],
            ["111", "222", "333"],
            111,
            "111",
        ),
    ]:
        widget.items = items
        await probe.redraw("Item list has been updated")

        # List of displayed items is as expected,
        # and the first item has been selected.
        assert probe.titles == display
        assert widget.value == selection
        assert probe.selected_title == selected_title

        on_change_handler.assert_called_once_with(widget)
        on_change_handler.reset_mock()

    # This isn't a documented API, but we can use it for testing purposes.
    widget._accessor = "name"
    widget.items = ListSource(
        accessors=["name", "value"],
        data=[
            {"name": "first", "value": 111},
            {"name": "second", "value": 222},
            {"name": "third", "value": 333},
        ],
    )
    await probe.redraw("Item list has been updated to use a source")

    assert probe.titles == ["first", "second", "third"]
    assert widget.value.name == "first"
    assert widget.value.value == 111
    assert probe.selected_title == "first"

    on_change_handler.assert_called_once_with(widget)


async def test_selection_change(widget, probe):
    """The selection can be changed."""
    on_change_handler = Mock()
    widget.on_change = on_change_handler

    # Change the selection programatically
    widget.value = "first"

    await probe.redraw("Selected item has been changed programmatically")
    on_change_handler.assert_called_once_with(widget)
    on_change_handler.reset_mock()

    assert widget.value == "first"

    # Change the selection via GUI action
    await probe.select_item()
    await probe.redraw("Selected item has been changed by user interaction")

    assert widget.value == "second"
    on_change_handler.assert_called_once_with(widget)


async def test_source_changes(widget, probe):
    """The selection responds to changes in the source."""
    on_change_handler = Mock()
    widget.on_change = on_change_handler

    # This isn't a documented API, but we can use it for testing purposes.
    # Set the widget to use a full source
    widget._accessor = "name"
    source = ListSource(
        accessors=["name", "value"],
        data=[
            {"name": "first", "value": 111},
            {"name": "second", "value": 222},
            {"name": "third", "value": 333},
        ],
    )
    widget.items = source
    await probe.redraw("Item list has been updated to use a source")
    # This triggers a change
    on_change_handler.assert_called_once_with(widget)
    on_change_handler.reset_mock()

    # Store the original selection
    selected_item = widget.value

    # Append a new item
    source.append(name="new 1", value=999)
    await probe.redraw("New item has been appended to selection")

    assert probe.titles == ["first", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name
    on_change_handler.assert_not_called()

    # Insert a new item
    source.insert(0, name="new 2", value=888)
    await probe.redraw("New item has been inserted into selection")

    assert probe.titles == ["new 2", "first", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name
    on_change_handler.assert_not_called()

    # Change the selected item
    source[1].name = "updated"
    await probe.redraw("Value of selected item has been changed")

    assert probe.titles == ["new 2", "updated", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name
    on_change_handler.assert_not_called()

    # Change a non-selected item
    source[0].name = "revised"
    await probe.redraw("Value of non-selected item has been changed")

    assert probe.titles == ["revised", "updated", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name
    on_change_handler.assert_not_called()

    # Remove the selected item
    source.remove(selected_item)
    await probe.redraw("Selected item has been removed from selection")

    assert probe.titles == ["revised", "second", "third", "new 1"]
    assert probe.selected_title == "revised"

    selected = source[0]
    assert widget.value == selected
    on_change_handler.assert_called_once_with(widget)
    on_change_handler.reset_mock()

    # Remove a non-selected item
    source.remove(source[2])
    await probe.redraw("Non-selected item has been removed from selection")

    assert probe.titles == ["revised", "second", "new 1"]
    assert probe.selected_title == "revised"
    assert widget.value == selected
    on_change_handler.assert_not_called()

    # Clear the source
    source.clear()
    await probe.redraw("Source has been cleared")

    assert probe.titles == []
    assert probe.selected_title is None
    assert widget.value is None
    on_change_handler.assert_called_once_with(widget)
    on_change_handler.reset_mock()


# def test_clear_source(widget, source, on_change_handler):
#     "If the source is cleared, the selection is cleared"
#     # Clear the source
#     source.clear()

#     # The widget has been cleared
#     assert_action_performed(widget, "clear")

#     # The widget must have cleared it's selection
#     on_change_handler.assert_called_with(widget)
#     assert widget.value is None


# def test_change_source_empty(widget, on_change_handler):
#     """If the source is changed to an empty source, the selection is reset"""
#     # Clear the event history
#     EventLog.reset()

#     widget.items = []

#     # The widget source has changed
#     assert_action_performed(widget, "change source")

#     # The widget must have cleared it's selection
#     on_change_handler.assert_called_with(widget)
#     assert widget.value is None


# def test_change_source(widget, on_change_handler):
#     """If the source is changed, the selection is set to the first item"""
#     # Clear the event history
#     EventLog.reset()

#     # Change the source of the data
#     widget.items = ["new 1", "new 2"]

#     # The widget source has changed
#     assert_action_performed(widget, "change source")

#     # The widget must have cleared it's selection
#     on_change_handler.assert_called_with(widget)
#     assert widget.value.key == "new 1"
