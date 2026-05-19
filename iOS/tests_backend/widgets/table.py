import pytest

from toga_iOS.libs import (
    NSIndexPath,
    UILabel,
    UIStackView,
    UITableView,
    UITableViewController,
    UITableViewScrollPositionNone,
)

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = UITableView
    supports_icons = False
    supports_keyboard_shortcuts = False
    supports_keyboard_boundary_shortcuts = False
    supports_widgets = False

    def __init__(self, widget):
        super().__init__(widget)
        self.native_controller = widget._impl.native_controller
        assert isinstance(self.native_controller, UITableViewController)

    @property
    def font(self):
        pytest.skip("Font changes not implemented for Table on iOS")

    def _header_scroll_offset(self):
        header = self.native.tableHeaderView
        if header is None:
            return 0
        return int(header.frame.size.height)

    def _cell_stack(self, cell):
        for subview in cell.contentView.subviews():
            if isinstance(subview, UIStackView):
                return subview
        raise AssertionError(f"No row stack found in {cell!r}")

    def _cell_at_row(self, row):
        path = NSIndexPath.indexPathForRow(row, inSection=0)
        cell = self.native.cellForRowAtIndexPath_(path)
        if cell is None:
            # Populate the cell via the data source; don't use the return value as
            # Rubicon can mis-handle returns from @objc_method when warnings fire.
            self.native_controller.tableView_cellForRowAtIndexPath_(
                self.native,
                path,
            )
            cell = self.native.cellForRowAtIndexPath_(path)
        assert cell is not None, f"Row {row} cell could not be loaded"
        return cell

    @property
    def row_count(self):
        return int(
            self.native.delegate.tableView_numberOfRowsInSection_(self.native, 0)
        )

    @property
    def column_count(self):
        return len(self.widget._columns)

    def _cell_labels(self, row):
        cell = self._cell_at_row(row)
        return [v for v in self._cell_stack(cell).arrangedSubviews if isinstance(v, UILabel)]

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        if widget is not None:
            pytest.skip("This backend doesn't support widgets in Tables")
        if icon is not None:
            pytest.skip("This backend doesn't support icons in Tables")
        assert str(self._cell_labels(row)[col].text) == value

    @property
    def max_scroll_position(self):
        return max(
            0,
            int(self.native.contentSize.height - self.native.frame.size.height),
        )

    @property
    def scroll_position(self):
        # With a tableHeaderView, contentOffset.y at the top equals the header height.
        return int(self.native.contentOffset.y) - self._header_scroll_offset()

    async def wait_for_scroll_completion(self):
        pass

    @property
    def header_visible(self):
        return self.native.tableHeaderView is not None

    @property
    def header_titles(self):
        header = self.native.tableHeaderView
        if header is None:
            return []
        return [str(v.text) for v in header.arrangedSubviews]

    def column_width(self, col):
        header = self.native.tableHeaderView
        if header is not None:
            stack = header
        else:
            stack = self._cell_stack(self._cell_at_row(0))
        return float(stack.arrangedSubviews[col].frame.size.width)

    async def resize_column(self, index, width):
        pytest.xfail("Table columns cannot be resized on iOS")

    async def select_row(self, row, add=False):
        path = NSIndexPath.indexPathForRow(row, inSection=0)
        delegate = self.native.delegate

        if self.widget.multiple_select and add:
            paths = self.native.indexPathsForSelectedRows
            selected_rows = {int(p.row) for p in paths} if paths is not None else set()
            if row in selected_rows:
                self.native.deselectRowAtIndexPath(path, animated=False)
                delegate.tableView_didDeselectRowAtIndexPath_(self.native, path)
            else:
                self.native.selectRowAtIndexPath(
                    path,
                    animated=False,
                    scrollPosition=UITableViewScrollPositionNone,
                )
                delegate.tableView_didSelectRowAtIndexPath_(self.native, path)
        else:
            paths = self.native.indexPathsForSelectedRows
            if paths is not None:
                for existing in list(paths):
                    self.native.deselectRowAtIndexPath(existing, animated=False)
            self.native.selectRowAtIndexPath(
                path,
                animated=False,
                scrollPosition=UITableViewScrollPositionNone,
            )
            delegate.tableView_didSelectRowAtIndexPath_(self.native, path)

    async def activate_row(self, row):
        pytest.xfail("on_activate is not supported on iOS Table")

    async def activate_header(self):
        pass

    async def select_first_row_keyboard(self):
        pytest.xfail("Keyboard selection not supported on iOS")
