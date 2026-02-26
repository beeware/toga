from unittest.mock import Mock

import pytest

import toga
from toga.sources import ListListener, ListSource
from toga.style.pack import Pack

from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
def on_select_handler():
    return Mock()


@pytest.fixture
def on_refresh_handler():
    return Mock()


@pytest.fixture
def on_primary_action_handler():
    return Mock()


@pytest.fixture
def on_secondary_action_handler():
    return Mock()


@pytest.fixture
def source():
    red = toga.Icon("resources/icons/red")
    green = toga.Icon("resources/icons/green")

    return ListSource(
        accessors=["a", "b", "c", "d"],
        data=[
            {
                "a": f"A{i}",
                "b": f"B{i}",
                "c": {0: None, 1: red, 2: green}[i % 3],
                "d": f"C{i}",
            }
            for i in range(100)
        ],
    )


@pytest.fixture
async def widget(
    source,
    on_select_handler,
    on_refresh_handler,
    on_primary_action_handler,
    on_secondary_action_handler,
):
    return toga.DetailedList(
        data=source,
        accessors=("a", "b", "c"),
        missing_value="MISSING!",
        on_select=on_select_handler,
        on_refresh=on_refresh_handler,
        primary_action="Twist",
        on_primary_action=on_primary_action_handler,
        secondary_action="Shout",
        on_secondary_action=on_secondary_action_handler,
        style=Pack(flex=1),
    )


test_cleanup = build_cleanup_test(toga.DetailedList)


async def test_scroll(widget, probe):
    """The detailedList can be scrolled"""

    # Due to the interaction of scrolling with the header row, the scroll might be <0.
    assert probe.scroll_position <= 0
    # Refresh is available at the top of the page.
    if probe.supports_refresh:
        assert probe.refresh_available()

    # Scroll to the bottom of the detailedList
    widget.scroll_to_bottom()
    await probe.wait_for_scroll_completion()
    await probe.redraw("DetailedList scrolled to bottom")
    # Refresh is not available when we're not at the top of the page.
    if probe.supports_refresh:
        assert not probe.refresh_available()

    # max_scroll_position is not perfectly accurate on Winforms.
    assert probe.scroll_position == pytest.approx(probe.max_scroll_position, abs=15)

    # Scroll to the middle of the detailedList
    widget.scroll_to_row(50)
    await probe.wait_for_scroll_completion()
    await probe.redraw("DetailedList scrolled to mid row")
    if probe.supports_refresh:
        assert not probe.refresh_available()

    # Row 50 should be visible. It could be at the top of the screen, or the bottom of
    # the screen; we don't really care which - as long as it's roughly in the middle of
    # the scroll range, call it a win.
    assert probe.scroll_position == pytest.approx(
        probe.max_scroll_position / 2, abs=400
    )

    # Scroll to the top of the detailedList
    widget.scroll_to_top()
    await probe.wait_for_scroll_completion()
    await probe.redraw("DetailedList scrolled to bottom")
    if probe.supports_refresh:
        assert probe.refresh_available()

    # Due to the interaction of scrolling with the header row, the scroll might be <0.
    assert probe.scroll_position <= 0


async def test_select(widget, probe, source, on_select_handler):
    """Rows can be selected"""
    # Initial selection is empty
    assert widget.selection is None
    await probe.redraw("No row is selected")
    on_select_handler.assert_not_called()

    # A single row can be selected
    await probe.select_row(1)
    await probe.redraw("Second row is selected")
    assert widget.selection == source[1]

    # Winforms generates two events, first removing the old selection and then adding
    # the new one.
    on_select_handler.assert_called_with(widget)
    on_select_handler.reset_mock()

    # Trying to multi-select only does a single select
    await probe.select_row(2, add=True)
    await probe.redraw("Third row is selected")
    assert widget.selection == source[2]
    on_select_handler.assert_called_with(widget)
    on_select_handler.reset_mock()


class MyData:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"<data {self.text}>"


async def test_row_changes(widget, probe):
    """Meta test for adding and removing data to the detailedList"""
    red = toga.Icon("resources/icons/red")
    green = toga.Icon("resources/icons/green")

    # Change the data source for something smaller
    widget.data = [
        {
            "a": MyData(i),
            "b": i,
            "c": {0: None, 1: red}[i % 2],
        }
        for i in range(5)
    ]
    await probe.redraw("Data source has been changed")

    assert probe.row_count == 5
    # All cell contents are strings
    probe.assert_cell_content(4, "<data 4>", "4", icon=None)

    # Append a row to the detailedList
    widget.data.append({"a": "AX", "b": "BX", "c": green})
    await probe.redraw("Full row has been appended")

    assert probe.row_count == 6
    probe.assert_cell_content(4, "<data 4>", "4", icon=None)
    probe.assert_cell_content(5, "AX", "BX", icon=green)

    # Insert a row into the middle of the detailedList;
    # All text values are None; icon doesn't exist
    widget.data.insert(2, {"a": None, "b": None, "c": None})
    await probe.redraw("Empty row has been inserted")

    assert probe.row_count == 7
    # Missing value has been populated
    probe.assert_cell_content(2, "MISSING!", "MISSING!", icon=None)
    probe.assert_cell_content(5, "<data 4>", "4", icon=None)
    probe.assert_cell_content(6, "AX", "BX", icon=green)

    # Change content on the partial row
    widget.data[2].a = "ANEW"
    widget.data[2].b = MyData("NEW")
    widget.data[2].c = red
    await probe.redraw("Empty row has been updated")

    assert probe.row_count == 7
    probe.assert_cell_content(2, "ANEW", "<data NEW>", icon=red)
    probe.assert_cell_content(5, "<data 4>", "4", icon=None)
    probe.assert_cell_content(6, "AX", "BX", icon=green)

    # Remove all text attributes from the new row
    del widget.data[2].a
    del widget.data[2].b
    del widget.data[2].c
    await probe.redraw("Empty row has had data attributes removed")

    assert probe.row_count == 7
    probe.assert_cell_content(2, "MISSING!", "MISSING!", icon=None)
    probe.assert_cell_content(5, "<data 4>", "4", icon=None)
    probe.assert_cell_content(6, "AX", "BX", icon=green)

    # Delete a row
    del widget.data[3]
    await probe.redraw("Row has been removed")
    assert probe.row_count == 6
    probe.assert_cell_content(2, "MISSING!", "MISSING!", icon=None)
    probe.assert_cell_content(4, "<data 4>", "4", icon=None)
    probe.assert_cell_content(5, "AX", "BX", icon=green)

    # Clear the detailedList
    widget.data.clear()
    await probe.redraw("Data has been cleared")
    assert probe.row_count == 0


async def test_refresh(widget, probe):
    "Refresh can be triggered"
    if not probe.supports_refresh:
        pytest.skip("This backend doesn't support the refresh action")

    # Set a refresh handler that simulates a reload altering data.
    def add_row(event_widget, **kwargs):
        assert event_widget == widget
        assert kwargs == {}
        widget.data.insert(0, {"a": "NEW A", "b": "NEW B"})

    widget.on_refresh = add_row

    # A partial pull-to-refresh doesn't reload data.
    await probe.non_refresh_action()
    await probe.redraw("A non-refresh action has occurred")
    assert len(widget.data) == 100

    await probe.refresh_action()
    # It can take a couple of cycles for the refresh handler to fully execute;
    # impose a small delay to ensure it's been processed.
    await probe.redraw("A refresh action has occurred", delay=0.2)
    # New data has been added
    assert len(widget.data) == 101

    # Disable refresh
    widget.on_refresh = None

    # A non-refresh action still doesn't reload data.
    await probe.non_refresh_action()
    await probe.redraw("A non-refresh action has occurred")
    assert len(widget.data) == 101

    # Disable refresh a second time, ensuring it's a no-op
    widget.on_refresh = None

    # A full refresh action doesn't reload data
    await probe.refresh_action(active=False)
    await probe.redraw("A refresh action was performed without triggering refresh")
    assert len(widget.data) == 101


async def test_actions(
    widget,
    probe,
    on_primary_action_handler,
    on_secondary_action_handler,
):
    "Actions can be performed on detailed list items"
    if not probe.supports_actions:
        pytest.skip("This backend doesn't support primary or secondary actions")

    await probe.perform_primary_action(3)
    await probe.redraw("A primary action was performed on row 3")
    on_primary_action_handler.assert_called_once_with(widget, row=widget.data[3])
    on_primary_action_handler.reset_mock()

    await probe.perform_secondary_action(4)
    await probe.redraw("A secondary action was performed on row 4")
    on_secondary_action_handler.assert_called_once_with(widget, row=widget.data[4])
    on_secondary_action_handler.reset_mock()

    await probe.redraw("Before perform")

    # Disable secondary action
    widget.on_secondary_action = None
    await probe.perform_secondary_action(5, active=False)
    await probe.redraw("An attempt at a secondary action was made")
    on_secondary_action_handler.assert_not_called()

    # Disable primary action
    widget.on_primary_action = None
    await probe.perform_primary_action(5, active=False)
    await probe.redraw("An attempt at a primary action was made")
    on_primary_action_handler.assert_not_called()

    # Enable secondary action again
    widget.on_secondary_action = on_secondary_action_handler
    await probe.perform_secondary_action(5)
    await probe.redraw("A secondary action was performed on row 5")
    on_secondary_action_handler.assert_called_once_with(widget, row=widget.data[5])
    on_secondary_action_handler.reset_mock()

    # Enable primary action again
    widget.on_primary_action = on_primary_action_handler
    await probe.perform_primary_action(6)
    await probe.redraw("A primary action was performed on row 6")
    on_primary_action_handler.assert_called_once_with(widget, row=widget.data[6])
    on_primary_action_handler.reset_mock()


def test_list_listener(widget):
    """Does the widget implement the ListListener API"""
    assert isinstance(widget._impl, ListListener)
