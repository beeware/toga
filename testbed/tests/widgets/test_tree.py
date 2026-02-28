import contextlib
from unittest.mock import Mock

import pytest

import toga
from toga.sources import ListListener, TreeListener, TreeSource
from toga.style.pack import Pack

from ..conftest import skip_on_platforms
from .conftest import build_cleanup_test
from .probe import get_probe
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_enable_noop,
    test_flex_widget_size,
    test_focus,
    test_font,
)

# flag for collapse/expand preservation when changing tree structure
COLLAPSE_ON_INSERT_DELETE = "collapse_on_insert_delete"

# flag for selection preservation when changing tree structure
SELECTION_CLEARED_ON_INSERT_DELETE = "selection_cleared_on_insert_delete"


@pytest.fixture
def verify_font_sizes():
    # We can't verify font sizes inside the Tree
    return False, False


@pytest.fixture
def on_select_handler():
    return Mock()


@pytest.fixture
def on_activate_handler():
    return Mock()


@pytest.fixture
def source():
    return TreeSource(
        accessors=["a", "b", "c", "d", "e"],
        data=[
            (
                {
                    "a": f"A{x}",
                    "b": f"B{x}",
                    "c": f"C{x}",
                    "d": f"D{x}",
                    "e": f"E{x}",
                },
                [
                    (
                        {
                            "a": f"A{x}0",
                            "b": f"B{x}0",
                            "c": f"C{x}0",
                            "d": f"D{x}0",
                            "e": f"E{x}0",
                        },
                        None,
                    ),
                    (
                        {
                            "a": f"A{x}1",
                            "b": f"B{x}1",
                            "c": f"C{x}1",
                            "d": f"D{x}1",
                            "e": f"E{x}1",
                        },
                        [],
                    ),
                    (
                        {
                            "a": f"A{x}2",
                            "b": f"B{x}2",
                            "c": f"C{x}2",
                            "d": f"D{x}2",
                            "e": f"E{x}2",
                        },
                        [
                            (
                                {
                                    "a": f"A{x}2{y}",
                                    "b": f"B{x}2{y}",
                                    "c": f"C{x}2{y}",
                                    "d": f"D{x}2{y}",
                                    "e": f"E{x}2{y}",
                                },
                                None,
                            )
                            for y in range(3)
                        ],
                    ),
                ],
            )
            for x in range(10)
        ],
    )


@pytest.fixture
async def widget(source, on_select_handler, on_activate_handler):
    skip_on_platforms("iOS", "android", "windows")
    return toga.Tree(
        ["A", "B", "C"],
        data=source,
        missing_value="MISSING!",
        on_select=on_select_handler,
        on_activate=on_activate_handler,
        style=Pack(flex=1),
    )


@pytest.fixture
async def headerless_widget(source, on_select_handler):
    skip_on_platforms("iOS", "android", "windows")
    return toga.Tree(
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
    await probe.redraw("Constructing headerless Tree probe")
    probe.assert_container(box)
    yield probe

    main_window.content = old_content


@pytest.fixture
async def multiselect_widget(source, on_select_handler):
    # Although Android *has* a table implementation, it needs to be rebuilt.
    skip_on_platforms("iOS", "android", "windows")
    return toga.Tree(
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
    await probe.redraw("Constructing multiselect Tree probe")
    probe.assert_container(box)
    yield probe

    main_window.content = old_content


test_cleanup = build_cleanup_test(
    toga.Tree,
    kwargs={"headings": ["A", "B", "C"]},
    skip_platforms=(
        "iOS",
        "android",
        "windows",
    ),
)


async def test_select(widget, probe, source, on_select_handler):
    """Rows can be selected"""
    # Initial selection is empty
    assert widget.selection is None
    await probe.redraw("No row is selected")
    on_select_handler.assert_not_called()

    await probe.expand_tree()

    # A single row can be selected
    await probe.select_row((0, 0))
    await probe.redraw("Second row is selected")
    assert widget.selection == source[0][0]
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Trying to multi-select only does a single select
    await probe.select_row((0, 1), add=True)
    await probe.redraw("Third row is selected")
    assert widget.selection == source[0][1]
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # A deeper row can be selected
    await probe.select_row((1, 2, 0))
    await probe.redraw("Deep row in second group is selected")
    assert widget.selection == source[1][2][0]
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    if probe.supports_keyboard_shortcuts:
        # Keyboard responds to selectAll
        await probe.select_all()
        await probe.redraw("Select all keyboard shortcut is ignored")
        assert widget.selection == source[1][2][0]

        # Other keystrokes are ignored
        await probe.type_character("x")
        await probe.redraw("A non-shortcut key was pressed")
        assert widget.selection == source[1][2][0]


async def test_expand_collapse(widget, probe, source):
    """Nodes can be expanded and collapsed"""

    # Initially unexpanded
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    assert not probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Expanding/collapsing nodes when tree is not expanded
    # Expand a single root node
    widget.expand(source[1])
    await probe.redraw("Root Node 1 has been expanded")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Expand a single root node again
    widget.expand(source[1])
    await probe.redraw("Root Node 1 is still expanded")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Expand a single child node
    widget.expand(source[1][2])
    await probe.redraw("Child Node 1:2 has been expanded")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Expand the same child node again
    widget.expand(source[1][2])
    await probe.redraw("Child Node 1:2 is still expanded")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Attempt to collapse a leaf node
    widget.collapse(source[1][2][1])
    await probe.redraw("Leaf node collapse is a no-op")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Attempt to expand a leaf node
    widget.expand(source[1][2][1])
    await probe.redraw("Leaf node expansion is a no-op")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Fully collapse the tree
    widget.collapse()
    await probe.redraw("All nodes have been collapsed")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    assert not probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Fully collapse when already fully collapsed
    widget.collapse()
    await probe.redraw("All nodes are still collapsed")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    assert not probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Fully expand the tree
    widget.expand()
    await probe.redraw("All nodes have been expanded")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Fully expand when already fully expanded
    widget.expand()
    await probe.redraw("All nodes are still expanded")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Collapse a single root node
    widget.collapse(source[1])
    await probe.redraw("Root Node 1 has been collapsed")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    # State of source[1][2] is ambiguous
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Collapse the same single root node again
    widget.collapse(source[1])
    await probe.redraw("Root Node 1 is still collapsed")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    # State of source[1][2] is ambiguous
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Collapse a single child node
    widget.collapse(source[0][2])
    await probe.redraw("Child Node 0:2 has been collapsed")
    assert probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    # State of source[1][2] is ambiguous
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Collapse the same child node
    widget.collapse(source[0][2])
    await probe.redraw("Child Node 0:2 is still collapsed")
    assert probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    # State of source[1][2] is ambiguous
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Expand a single root node
    widget.expand(source[1])
    await probe.redraw("Root Node 1 has been expanded")
    assert probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])  # Restores previous expansion state
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Expand a single root node again
    widget.expand(source[1])
    await probe.redraw("Root Node 1 is still expanded")
    assert probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Expand a single child node
    widget.expand(source[0][2])
    await probe.redraw("Child Node 0:2 has been expanded")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Expand the same child node again
    widget.expand(source[0][2])
    await probe.redraw("Child Node 0:2 is still expanded")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Attempt to collapse a leaf node
    widget.collapse(source[0][2][1])
    await probe.redraw("Leaf node collapse is a no-op")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Attempt to collapse a leaf node again
    widget.collapse(source[0][2][1])
    await probe.redraw("Leaf node collapse is a no-op")
    assert probe.is_expanded(source[0])
    assert probe.is_expanded(source[0][2])
    assert probe.is_expanded(source[1])
    assert probe.is_expanded(source[1][2])
    assert probe.is_expanded(source[2])
    assert probe.is_expanded(source[2][2])

    # Fully collapse the tree
    widget.collapse()
    await probe.redraw("All nodes have been collapsed")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    assert not probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])

    # Fully collapse when already fully collapsed
    widget.collapse()
    await probe.redraw("All nodes are still collapsed")
    assert not probe.is_expanded(source[0])
    assert not probe.is_expanded(source[0][2])
    assert not probe.is_expanded(source[1])
    assert not probe.is_expanded(source[1][2])
    assert not probe.is_expanded(source[2])
    assert not probe.is_expanded(source[2][2])


async def test_activate(
    widget,
    probe,
    source,
    on_select_handler,
    on_activate_handler,
):
    """Rows can be activated"""
    await probe.expand_tree()

    await probe.activate_row((0, 0))
    await probe.redraw("Second row is activated")

    # Activation selects the row.
    assert widget.selection == source[0][0]
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    on_activate_handler.assert_called_once_with(widget, node=source[0][0])
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

    await multiselect_probe.expand_tree()

    # A single row can be selected
    await multiselect_probe.select_row((0, 0))
    assert multiselect_widget.selection == [source[0][0]]
    await multiselect_probe.redraw("One row is selected in multiselect table")
    on_select_handler.assert_called_once_with(multiselect_widget)
    on_select_handler.reset_mock()

    # A row can be added to the selection
    await multiselect_probe.select_row((0, 1), add=True)
    await multiselect_probe.redraw("Two rows are selected in multiselect table")
    assert multiselect_widget.selection == [source[0][0], source[0][1]]
    on_select_handler.assert_called_once_with(multiselect_widget)
    on_select_handler.reset_mock()

    # A deeper row can be added to the selection
    await multiselect_probe.select_row((1, 2, 0), add=True)
    await multiselect_probe.redraw("Three rows are selected in multiselect table")
    assert multiselect_widget.selection == [source[0][0], source[0][1], source[1][2][0]]
    on_select_handler.assert_called_once_with(multiselect_widget)
    on_select_handler.reset_mock()

    # A row can be removed from the selection
    await multiselect_probe.select_row((0, 0), add=True)
    await multiselect_probe.redraw("First row has been removed from the selection")
    assert multiselect_widget.selection == [source[0][1], source[1][2][0]]
    on_select_handler.assert_called_once_with(multiselect_widget)
    on_select_handler.reset_mock()

    if multiselect_probe.supports_keyboard_shortcuts:
        # Keyboard responds to selectAll
        await multiselect_probe.select_all()
        await multiselect_probe.redraw("All rows selected by keyboard")
        assert len(multiselect_widget.selection) == 70


class MyData:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"<data {self.text}>"


async def _row_change_test(widget, probe):
    """Meta test for adding and removing data to the table"""

    # Change the data source for something smaller
    small_data = [
        (
            {"a": "A0", "b": "", "c": ""},
            [({"a": f"A{i}", "b": i, "c": MyData(i)}, None) for i in range(5)],
        )
    ]

    widget.data = small_data

    assert probe.child_count() == 1
    assert probe.child_count((0,)) == 5

    # All cell contents are strings
    probe.assert_cell_content((0, 4), 0, "A4")
    probe.assert_cell_content((0, 4), 1, "4")
    probe.assert_cell_content((0, 4), 2, "<data 4>")

    # Test append/insert/modify/remove prior to tree expansion
    # Append a child to a non-expanded root
    widget.data[0].append({"a": "AX", "b": "BX", "c": "CX"})
    await probe.redraw("Full row has been appended to a non-expanded root")

    assert probe.child_count((0,)) == 6
    probe.assert_cell_content((0, 4), 0, "A4")
    probe.assert_cell_content((0, 5), 0, "AX")

    # Append a child to a non-expanded child
    widget.data[0][5].append({"a": "AXX", "b": "BXX", "c": "CXX"})
    await probe.redraw("Full row has been appended to a non-expanded child")

    assert probe.child_count((0, 5)) == 1
    probe.assert_cell_content((0, 5, 0), 0, "AXX")
    probe.assert_cell_content((0, 5, 0), 1, "BXX")
    probe.assert_cell_content((0, 5, 0), 2, "CXX")

    # Insert a row into the middle of the table;
    # Row is missing a B accessor
    widget.data[0].insert(2, {"a": "AY", "c": "CY"})
    await probe.redraw("Partial row has been appended to a non-expanded root")

    assert probe.child_count((0,)) == 7
    probe.assert_cell_content((0, 2), 0, "AY")
    probe.assert_cell_content((0, 5), 0, "A4")
    probe.assert_cell_content((0, 6), 0, "AX")

    # Missing value has been populated
    probe.assert_cell_content((0, 2), 1, "MISSING!")

    # Change content on the partial row
    widget.data[0][2].a = "ANEW"
    widget.data[0][2].b = "BNEW"
    await probe.redraw("Partial non-visible row has been updated")

    assert probe.child_count((0,)) == 7
    probe.assert_cell_content((0, 2), 0, "ANEW")
    probe.assert_cell_content((0, 5), 0, "A4")
    probe.assert_cell_content((0, 6), 0, "AX")

    # Missing value has the default empty string
    probe.assert_cell_content((0, 2), 1, "BNEW")

    # Delete a row
    del widget.data[0][3]
    await probe.redraw("Non-visible row has been removed")
    assert probe.child_count((0,)) == 6
    probe.assert_cell_content((0, 2), 0, "ANEW")
    probe.assert_cell_content((0, 4), 0, "A4")
    probe.assert_cell_content((0, 5), 0, "AX")

    # Insert a new root
    widget.data.insert(0, {"a": "A!", "b": "B!", "c": "C!"})
    await probe.redraw("New root row has been appended")

    assert probe.child_count() == 2
    assert probe.child_count((0,)) == 0
    probe.assert_cell_content((0,), 0, "A!")

    # Delete a root
    del widget.data[1]
    await probe.redraw("Old root row has been removed")

    assert probe.child_count() == 1
    assert probe.child_count((0,)) == 0
    probe.assert_cell_content((0,), 0, "A!")

    # Expand tree and check contents still correct
    await probe.expand_tree()
    await probe.redraw("Tree expanded")

    assert probe.child_count() == 1
    assert probe.child_count((0,)) == 0
    probe.assert_cell_content((0,), 0, "A!")
    probe.assert_cell_content((0,), 1, "B!")
    probe.assert_cell_content((0,), 2, "C!")

    # Clear the table
    widget.data.clear()
    await probe.redraw("Data has been cleared")
    assert probe.child_count() == 0

    # Test append/insert/modify/remove after tree expansion
    widget.data = small_data
    await probe.redraw("Data source has been changed")

    # Append a row to the table
    widget.data[0].append({"a": "AX", "b": "BX", "c": "CX"})
    await probe.redraw("Full row has been appended")

    assert probe.child_count((0,)) == 6
    probe.assert_cell_content((0, 4), 0, "A4")
    probe.assert_cell_content((0, 5), 0, "AX")

    # Insert a row into the middle of the table;
    # Row is missing a B accessor
    widget.data[0].insert(2, {"a": "AY", "c": "CY"})
    await probe.redraw("Partial row has been appended")

    assert probe.child_count((0,)) == 7
    probe.assert_cell_content((0, 2), 0, "AY")
    probe.assert_cell_content((0, 5), 0, "A4")
    probe.assert_cell_content((0, 6), 0, "AX")

    # Missing value has been populated
    probe.assert_cell_content((0, 2), 1, "MISSING!")

    # Change content on the partial row
    widget.data[0][2].a = "ANEW"
    widget.data[0][2].b = "BNEW"
    await probe.redraw("Partial row has been updated")

    assert probe.child_count((0,)) == 7
    probe.assert_cell_content((0, 2), 0, "ANEW")
    probe.assert_cell_content((0, 5), 0, "A4")
    probe.assert_cell_content((0, 6), 0, "AX")

    # Missing value has the default empty string
    probe.assert_cell_content((0, 2), 1, "BNEW")

    # Delete a row
    del widget.data[0][3]
    await probe.redraw("Row has been removed")
    assert probe.child_count((0,)) == 6
    probe.assert_cell_content((0, 2), 0, "ANEW")
    probe.assert_cell_content((0, 4), 0, "A4")
    probe.assert_cell_content((0, 5), 0, "AX")

    # Delete a selected row
    # - ensure row is visible
    await probe.expand_tree()
    await probe.redraw("Tree expanded")
    # - select row
    await probe.select_row((0, 2))
    await probe.redraw("Row has been selected")
    assert widget.selection == widget.data[0][2]
    # - delete row
    del widget.data[0][2]
    await probe.redraw("Row has been removed")
    assert probe.child_count((0,)) == 5
    probe.assert_cell_content((0, 2), 0, "A3")
    # - nothing should be selected
    assert widget.selection is None
    # - parent should still be expanded
    if not getattr(probe, COLLAPSE_ON_INSERT_DELETE, False):
        assert probe.is_expanded(widget.data[0])
    else:
        assert not probe.is_expanded(widget.data[0])

    # Insert a row at selection
    # - ensure row is visible
    await probe.expand_tree()
    await probe.redraw("Tree expanded")
    # - select row
    await probe.select_row((0, 2))
    await probe.redraw("Row has been selected")
    assert widget.selection == widget.data[0][2]
    # - insert row, which is missing a B accessor
    widget.data[0].insert(2, {"a": "AY", "c": "CY"})
    await probe.redraw("Partial row has been appended")
    assert probe.child_count((0,)) == 6
    probe.assert_cell_content((0, 2), 0, "AY")
    probe.assert_cell_content((0, 3), 0, "A3")
    # - check selection is original object or has been cleared
    if not getattr(probe, SELECTION_CLEARED_ON_INSERT_DELETE, False):
        assert widget.selection == widget.data[0][3]
    else:
        assert widget.selection is None
    # - parent should still be expanded
    if not getattr(probe, COLLAPSE_ON_INSERT_DELETE, False):
        assert probe.is_expanded(widget.data[0])
    else:
        assert not probe.is_expanded(widget.data[0])

    # Insert a new root
    widget.data.insert(0, {"a": "A!", "b": "B!", "c": "C!"})
    await probe.redraw("New root row has been appended")

    assert probe.child_count() == 2
    assert probe.child_count((0,)) == 0
    probe.assert_cell_content((0,), 0, "A!")

    # Delete a root
    del widget.data[1]
    await probe.redraw("Old root row has been removed")

    assert probe.child_count() == 1
    assert probe.child_count((0,)) == 0
    probe.assert_cell_content((0,), 0, "A!")

    # Clear the table
    widget.data.clear()
    await probe.redraw("Data has been cleared")
    assert probe.child_count() == 0


async def test_row_changes(widget, probe):
    """Rows can be added and removed"""
    # Header is visible
    assert probe.header_visible
    await _row_change_test(widget, probe)


async def test_headerless_row_changes(headerless_widget, headerless_probe):
    """Rows can be added and removed to a headerless table"""
    # Header doesn't exist
    assert not headerless_probe.header_visible
    await _row_change_test(headerless_widget, headerless_probe)


async def _column_change_test(widget, probe):
    """Meta test for adding and removing columns"""
    # Initially 3 columns; Cell 0,2 contains C0
    assert probe.column_count == 3
    probe.assert_cell_content((0,), 2, "C0")

    widget.append_column("E", accessor="e")
    await probe.redraw("E column appended")

    # 4 columns; the new content on row 0 is "E0"
    assert probe.column_count == 4
    probe.assert_cell_content((0,), 2, "C0")
    probe.assert_cell_content((0,), 3, "E0")

    widget.insert_column(3, "D", accessor="d")
    await probe.redraw("E column appended")

    # 5 columns; the new content on row 0 is "D0", between C0 and E0
    assert probe.column_count == 5
    probe.assert_cell_content((0,), 2, "C0")
    probe.assert_cell_content((0,), 3, "D0")
    probe.assert_cell_content((0,), 4, "E0")

    widget.remove_column(2)
    await probe.redraw("C column removed")

    # 4 columns; C0 has gone
    assert probe.column_count == 4
    probe.assert_cell_content((0,), 2, "D0")
    probe.assert_cell_content((0,), 3, "E0")


async def test_column_changes(widget, probe):
    """Columns can be added and removed"""
    # Header is visible, and has the right titles
    assert probe.header_visible
    assert probe.header_titles == ["A", "B", "C"]
    # Columns should be roughly equal in width; there's a healthy allowance for
    # inter-column padding etc.
    assert probe.column_width(0) == pytest.approx(probe.width / 3, abs=25)
    assert probe.column_width(1) == pytest.approx(probe.width / 3, abs=25)
    assert probe.column_width(2) == pytest.approx(probe.width / 3, abs=25)

    await _column_change_test(widget, probe)

    assert probe.header_titles == ["A", "B", "D", "E"]
    # The specific behavior for resizing is undefined; however, the columns should add
    # up to near the full width (allowing for inter-column padding, etc), and no single
    # column should be tiny.
    total_width = sum(probe.column_width(i) for i in range(4))
    assert total_width == pytest.approx(probe.width, abs=100)
    assert all(probe.column_width(i) > 80 for i in range(4))


async def test_headerless_column_changes(headerless_widget, headerless_probe):
    """Columns can be added and removed to a headerless table"""
    # Header is not visible
    assert not headerless_probe.header_visible

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
        (
            {"a": "A0", "b": "", "c": ""},
            [
                (
                    {
                        # Normal text,
                        "a": f"A{i}",
                        # A tuple
                        "b": ({0: None, 1: red, 2: green}[i % 3], f"B{i}"),
                        # An object with an icon attribute.
                        "c": MyIconData(f"C{i}", {0: red, 1: green, 2: None}[i % 3]),
                    },
                    None,
                )
                for i in range(50)
            ],
        )
    ]
    await probe.expand_tree()

    await probe.redraw("Tree has data with icons")

    probe.assert_cell_content((0, 0), 0, "A0")
    probe.assert_cell_content((0, 0), 1, "B0", icon=None)
    probe.assert_cell_content((0, 0), 2, "<icondata C0>", icon=red)

    probe.assert_cell_content((0, 1), 0, "A1")
    probe.assert_cell_content((0, 1), 1, "B1", icon=red)
    probe.assert_cell_content((0, 1), 2, "<icondata C1>", icon=green)

    probe.assert_cell_content((0, 2), 0, "A2")
    probe.assert_cell_content((0, 2), 1, "B2", icon=green)
    probe.assert_cell_content((0, 2), 2, "<icondata C2>", icon=None)


async def test_cell_widget(widget, probe):
    "A widget can be used as a cell value"
    data = [
        (
            {"a": "A0", "b": "", "c": ""},
            [
                (
                    {
                        # Normal text,
                        "a": f"A{i}",
                        "b": f"B{i}",
                        # Toga widgets.
                        "c": (
                            toga.Button(f"C{i}")
                            if i % 2 == 0
                            else toga.TextInput(value=f"edit C{i}")
                        ),
                    },
                    None,
                )
                for i in range(50)
            ],
        ),
    ]
    if probe.supports_widgets:
        warning_check = contextlib.nullcontext()
    else:
        warning_check = pytest.warns(
            match=".* does not support the use of widgets in cells"
        )

    with warning_check:
        widget.data = data

        # Qt backend doesn't know there are widgets until the row is expanded
        await probe.expand_tree()
        await probe.redraw("Tree has data with widgets")

    probe.assert_cell_content((0, 0), 0, "A0")
    probe.assert_cell_content((0, 0), 1, "B0")

    probe.assert_cell_content((0, 1), 0, "A1")
    probe.assert_cell_content((0, 1), 1, "B1")

    if probe.supports_widgets:
        probe.assert_cell_content((0, 0), 2, widget=widget.data[0][0].c)
        probe.assert_cell_content((0, 1), 2, widget=widget.data[0][1].c)
    else:
        # If the platform doesn't support cell widgets, the test should still *run* -
        # we just won't have widgets in the cells.
        probe.assert_cell_content((0, 0), 2, "MISSING!")
        probe.assert_cell_content((0, 1), 2, "MISSING!")


def test_tree_listener(widget):
    """Does the widget Implementation satisfy the ListListener and
    TreeListener APIs"""
    assert isinstance(widget._impl, ListListener)
    assert isinstance(widget._impl, TreeListener)
