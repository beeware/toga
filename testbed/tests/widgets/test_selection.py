from unittest.mock import Mock

import pytest

import toga
from toga.constants import CENTER
from toga.sources import ListSource

from .properties import (  # noqa: F401
    test_alignment,
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
    test_font,
    test_font_attrs,
)

# FIXME: 2023-05-31 GTK's focus APIs are completely broken for GTK.ComboBox. The
# widget *can* accept focus, but invoking `grab_focus()` doesn't trigger any of
# the usual focus infrastructure, it doesn't send focus-in/out-event even when
# focus *is* obtained, and `has_focus()` always returns false. As best as I can
# make out, there's an internal private widget that actually gets the focus, but
# that widget isn't visible to GObject. We can't use test_focus_noop because
# the textinput *does* lose focus when focus() is invoked on selection.
if toga.platform.current_platform == "linux":
    pass
elif toga.platform.current_platform == "android":
    # This widget can't be given focus on Android.
    from .properties import test_focus_noop  # noqa: F401
else:
    from .properties import test_focus  # noqa: F401


@pytest.fixture
async def widget():
    return toga.Selection(items=["first", "second", "third"])


@pytest.fixture
def verify_font_sizes():
    # Font size does not affect the width of this widget.
    return False, True


@pytest.fixture
def verify_vertical_alignment():
    return CENTER


async def test_item_titles(widget, probe):
    """The selection is able to build display titles from a range of data types"""
    on_change_handler = Mock()
    widget.on_change = on_change_handler

    for index, (items, display, selection, selected_title) in enumerate(
        [
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
        ],
        start=1,
    ):
        widget.items = items
        await probe.redraw(f"Item list has been updated (pass {index})")

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

    # Change the selection programmatically
    assert widget.value == "first"
    widget.value = "third"

    await probe.redraw("Selected item has been changed programmatically")
    on_change_handler.assert_called_once_with(widget)
    on_change_handler.reset_mock()

    assert widget.value == "third"

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
    assert selected_item.name == "first"

    # Append a new item
    source.append(dict(name="new 1", value=999))
    await probe.redraw("New item has been appended to selection")

    assert probe.titles == ["first", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name == "first"
    on_change_handler.assert_not_called()

    # Insert a new item
    source.insert(0, dict(name="new 2", value=888))
    await probe.redraw("New item has been inserted into selection")

    assert probe.titles == ["new 2", "first", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name == "first"
    on_change_handler.assert_not_called()

    # Change the selected item
    source[1].name = "updated"
    await probe.redraw("Value of selected item has been changed")

    assert probe.titles == ["new 2", "updated", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name == "updated"
    on_change_handler.assert_not_called()

    # Change a non-selected item
    source[0].name = "revised"
    await probe.redraw("Value of non-selected item has been changed")

    assert probe.titles == ["revised", "updated", "second", "third", "new 1"]
    assert probe.selected_title == selected_item.name == "updated"
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

    # Insert a new item (the first in the data)
    source.insert(0, dict(name="new 3", value=777))
    await probe.redraw("New item has been inserted into empty selection")

    assert probe.titles == ["new 3"]
    assert probe.selected_title == "new 3"
    selected = source[0]
    assert widget.value == selected
    on_change_handler.assert_called_once_with(widget)
    on_change_handler.reset_mock()

    # Remove the only item
    source.remove(selected)
    await probe.redraw("Last item has been removed")

    assert probe.titles == []
    assert probe.selected_title is None
    assert widget.value is None
    on_change_handler.assert_called_once_with(widget)
    on_change_handler.reset_mock()


async def test_resize_on_content_change(widget, probe):
    """The size of the widget adapts to the longest element."""
    # This test will be an xfail on some platforms.
    probe.assert_resizes_on_content_change()

    original_width = probe.width

    LONG_LABEL = "this is a very long item that should be quite wide"
    widget.items = ["first", "second", LONG_LABEL]
    await probe.redraw("A long item has been added to the list")
    assert probe.width > original_width * 2

    widget.value = LONG_LABEL
    await probe.redraw("The long item has been selected")
    assert probe.width > original_width * 2

    widget.items = ["first", "second", "third"]
    await probe.redraw("The list no longer has a long item")
    if probe.shrink_on_resize:
        assert probe.width == original_width

    widget.items = ["first", "second", LONG_LABEL]
    await probe.redraw("A long item has been added to the list again")
    assert probe.width > original_width * 2

    widget._items[2].value = "third"
    await probe.redraw("The long item has been renamed")
    if probe.shrink_on_resize:
        assert probe.width == original_width
