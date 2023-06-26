from unittest.mock import Mock

import pytest

import toga
from toga.sources import ListSource
from toga.style.pack import Pack

from ..conftest import skip_on_platforms
from .probe import get_probe
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
def on_select_handler():
    return Mock()


@pytest.fixture
def on_activate_handler():
    return Mock()


@pytest.fixture
def source():
    return ListSource(
        accessors=["a", "b", "c", "d", "e"],
        data=[
            {"a": f"A{i}", "b": f"B{i}", "c": f"C{i}", "d": f"D{i}", "e": f"E{i}"}
            for i in range(0, 100)
        ],
    )


@pytest.fixture
async def widget(source, on_select_handler, on_activate_handler):
    skip_on_platforms("iOS")
    return toga.Table(
        ["A", "B", "C"],
        data=source,
        missing_value="MISSING!",
        on_select=on_select_handler,
        on_activate=on_activate_handler,
        style=Pack(flex=1),
    )


@pytest.fixture
def headerless_widget(source, on_select_handler):
    skip_on_platforms("iOS")
    return toga.Table(
        data=source,
        missing_value="MISSING!",
        accessors=["a", "b", "c"],
        on_select=on_select_handler,
        style=Pack(flex=1),
    )


@pytest.fixture
async def headerless_probe(main_window, headerless_widget):
    old_content = main_window.content

    box = toga.Box(children=[headerless_widget])
    main_window.content = box
    probe = get_probe(headerless_widget)
    await probe.redraw("Constructing headerless Table probe")
    probe.assert_container(box)
    yield probe

    main_window.content = old_content


@pytest.fixture
def multiselect_widget(source, on_select_handler):
    skip_on_platforms("iOS")
    return toga.Table(
        ["A", "B", "C"],
        data=source,
        multiple_select=True,
        on_select=on_select_handler,
        style=Pack(flex=1),
    )


@pytest.fixture
async def multiselect_probe(main_window, multiselect_widget):
    old_content = main_window.content

    box = toga.Box(children=[multiselect_widget])
    main_window.content = box
    probe = get_probe(multiselect_widget)
    await probe.redraw("Constructing multiselect Table probe")
    probe.assert_container(box)
    yield probe

    main_window.content = old_content


async def test_scroll(widget, probe):
    """The table can be scrolled"""

    # Due to the interaction of scrolling with the header row, the scroll might be <0.
    assert probe.scroll_position <= 0

    # Scroll to the bottom of the table
    widget.scroll_to_bottom()
    await probe.wait_for_scroll_completion()
    await probe.redraw("Table scrolled to bottom")

    assert probe.scroll_position == probe.max_scroll_position

    # Scroll to the middle of the table
    widget.scroll_to_row(50)
    await probe.wait_for_scroll_completion()
    await probe.redraw("Table scrolled to mid row")

    # Row 50 should be visible. It could be at the top of the table, or the bottom of
    # the table; we don't really care which - as long as it's roughly in the middle of
    # the scroll range, call it a win.
    assert probe.scroll_position == pytest.approx(
        probe.max_scroll_position / 2, abs=250
    )

    # Scroll to the top of the table
    widget.scroll_to_top()
    await probe.wait_for_scroll_completion()
    await probe.redraw("Table scrolled to bottom")

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
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Trying to multi-select only does a single select
    await probe.select_row(2, add=True)
    await probe.redraw("Third row is selected")
    assert widget.selection == source[2]
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()


async def test_activate(
    widget,
    probe,
    source,
    on_select_handler,
    on_activate_handler,
):
    """Rows can be activated"""

    await probe.activate_row(1)
    await probe.redraw("Second row is activated")

    # Activation selects the row.
    assert widget.selection == source[1]
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    on_activate_handler.assert_called_once_with(widget, row=source[1])
    on_activate_handler.reset_mock()


async def test_multiselect(
    multiselect_widget,
    multiselect_probe,
    source,
    on_select_handler,
):
    """A table can be set up for multi-select"""
    await multiselect_probe.redraw("No row is selected in multiselect table")

    # Initial selection is empty
    assert multiselect_widget.selection == []
    on_select_handler.assert_not_called()

    # A single row can be selected
    await multiselect_probe.select_row(1)
    assert multiselect_widget.selection == [source[1]]
    await multiselect_probe.redraw("One row is selected in multiselect table")
    on_select_handler.assert_called_once_with(multiselect_widget)
    on_select_handler.reset_mock()

    # A row can be added to the selection
    await multiselect_probe.select_row(2, add=True)
    await multiselect_probe.redraw("Two rows are selected in multiselect table")
    assert multiselect_widget.selection == [source[1], source[2]]
    on_select_handler.assert_called_once_with(multiselect_widget)
    on_select_handler.reset_mock()

    # A row can be removed from the selection
    await multiselect_probe.select_row(1, add=True)
    await multiselect_probe.redraw("First row has been removed from the selection")
    assert multiselect_widget.selection == [source[2]]
    on_select_handler.assert_called_once_with(multiselect_widget)
    on_select_handler.reset_mock()


class MyData:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"<data {self.value}>"


async def _row_change_test(widget, probe):
    """Meta test for adding and removing data to the table"""

    # Change the data source for something smaller
    widget.data = [{"a": f"A{i}", "b": i, "c": MyData(i)} for i in range(0, 5)]
    await probe.redraw("Data source has been changed")

    assert probe.row_count == 5
    # All cell contents are strings
    probe.assert_cell_content(4, 0, "A4")
    probe.assert_cell_content(4, 1, "4")
    probe.assert_cell_content(4, 2, "<data 4>")

    # Append a row to the table
    widget.data.append({"a": "AX", "b": "BX", "c": "CX"})
    await probe.redraw("Full row has been appended")

    assert probe.row_count == 6
    probe.assert_cell_content(4, 0, "A4")
    probe.assert_cell_content(5, 0, "AX")

    # Insert a row into the middle of the table;
    # Row is missing a B accessor
    widget.data.insert(2, {"a": "AY", "c": "CY"})
    await probe.redraw("Partial row has been appended")

    assert probe.row_count == 7
    probe.assert_cell_content(2, 0, "AY")
    probe.assert_cell_content(5, 0, "A4")
    probe.assert_cell_content(6, 0, "AX")

    # Missing value has been populated
    probe.assert_cell_content(2, 1, "MISSING!")

    # Change content on the partial row
    widget.data[2].a = "ANEW"
    widget.data[2].b = "BNEW"
    await probe.redraw("Partial row has been updated")

    assert probe.row_count == 7
    probe.assert_cell_content(2, 0, "ANEW")
    probe.assert_cell_content(5, 0, "A4")
    probe.assert_cell_content(6, 0, "AX")

    # Missing value has the default empty string
    probe.assert_cell_content(2, 1, "BNEW")

    # Delete a row
    del widget.data[3]
    await probe.redraw("Row has been removed")
    assert probe.row_count == 6
    probe.assert_cell_content(2, 0, "ANEW")
    probe.assert_cell_content(4, 0, "A4")
    probe.assert_cell_content(5, 0, "AX")

    # Clear the table
    widget.data.clear()
    await probe.redraw("Data has been cleared")
    assert probe.row_count == 0


async def test_row_changes(widget, probe):
    """Rows can be added and removed"""
    # Header is visible
    assert probe.header_height > 10
    await _row_change_test(widget, probe)


async def test_headerless_row_changes(headerless_widget, headerless_probe):
    """Rows can be added and removed to a headerless table"""
    # Header doesn't exist
    assert headerless_probe.header_height == 0
    await _row_change_test(headerless_widget, headerless_probe)


async def _column_change_test(widget, probe):
    """Meta test for adding and removing columns"""
    # Initially 3 columns; Cell 0,2 contains C1
    assert probe.column_count == 3
    probe.assert_cell_content(0, 2, "C0")

    widget.append_column("E", accessor="e")
    await probe.redraw("E column appended")

    # 4 columns; the new content on row 0 is "E1"
    assert probe.column_count == 4
    probe.assert_cell_content(0, 2, "C0")
    probe.assert_cell_content(0, 3, "E0")

    widget.insert_column(3, "D", accessor="d")
    await probe.redraw("E column appended")

    # 5 columns; the new content on row 0 is "D1", between C1 and E1
    assert probe.column_count == 5
    probe.assert_cell_content(0, 2, "C0")
    probe.assert_cell_content(0, 3, "D0")
    probe.assert_cell_content(0, 4, "E0")

    widget.remove_column(2)
    await probe.redraw("C column removed")

    # 4 columns; C1 has gone
    assert probe.column_count == 4
    probe.assert_cell_content(0, 2, "D0")
    probe.assert_cell_content(0, 3, "E0")


async def test_column_changes(widget, probe):
    """Columns can be added and removed"""
    await _column_change_test(widget, probe)


async def test_headerless_column_changes(headerless_widget, headerless_probe):
    """Columns can be added and removed to a headerless table"""
    await _column_change_test(headerless_widget, headerless_probe)


class MyIconData:
    def __init__(self, text, icon):
        self.text = text
        self.icon = icon

    def __str__(self):
        return f"<icondata {self.text}>"


async def test_cell_icon(widget, probe):
    "An icon can be used as a cell value"
    red = toga.Icon("resources/icons/red")
    green = toga.Icon("resources/icons/green")
    widget.data = [
        {
            # Normal text,
            "a": f"A{i}",
            # A tuple
            "b": ({0: None, 1: red, 2: green}[i % 3], f"B{i}"),
            # An object with an icon attribute.
            "c": MyIconData(f"C{i}", {0: red, 1: green, 2: None}[i % 3]),
        }
        for i in range(0, 50)
    ]
    await probe.redraw("Table has data with icons")

    probe.assert_cell_content(0, 0, "A0")
    probe.assert_cell_content(0, 1, "B0", icon=None)
    probe.assert_cell_content(0, 2, "<icondata C0>", icon=red)

    probe.assert_cell_content(1, 0, "A1")
    probe.assert_cell_content(1, 1, "B1", icon=red)
    probe.assert_cell_content(1, 2, "<icondata C1>", icon=green)

    probe.assert_cell_content(2, 0, "A2")
    probe.assert_cell_content(2, 1, "B2", icon=green)
    probe.assert_cell_content(2, 2, "<icondata C2>", icon=None)


async def test_cell_widget(widget, probe):
    "A widget can be used as a cell value"
    widget.data = [
        {
            # Normal text,
            "a": f"A{i}",
            "b": f"B{i}",
            # Toga widgets.
            "c": toga.Button(f"C{i}")
            if i % 2 == 0
            else toga.TextInput(value=f"edit C{i}"),
        }
        for i in range(0, 50)
    ]
    await probe.redraw("Table has data with widgets")

    probe.assert_cell_content(0, 0, "A0")
    probe.assert_cell_content(0, 1, "B0")
    probe.assert_cell_content(0, 2, widget=widget.data[0].c)

    probe.assert_cell_content(1, 0, "A1")
    probe.assert_cell_content(1, 1, "B1")
    probe.assert_cell_content(1, 2, widget=widget.data[1].c)
