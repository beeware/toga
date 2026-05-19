import warnings

from rubicon.objc import CGRect, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.libs import (
    NSIndexPath,
    UIFont,
    UILabel,
    UILayoutConstraintAxis,
    UIStackView,
    UIStackViewAlignment,
    UITableViewCell,
    UITableViewCellStyleDefault,
    UITableViewController,
    UITableViewScrollPositionBottom,
    UITableViewScrollPositionMiddle,
    UITableViewScrollPositionNone,
    UITableViewScrollPositionTop,
    UIViewAutoresizing,
)
from toga_iOS.widgets.base import Widget

HEADER_HEIGHT = 28.0


def _label(text, *, bold=False):
    label = UILabel.alloc().init()
    label.text = text
    if bold:
        label.font = UIFont.boldSystemFontOfSize(UIFont.labelFontSize)
    return label


def _row_stack():
    stack = UIStackView.alloc().init()
    stack.axis = UILayoutConstraintAxis.Horizontal.value
    stack.alignment = UIStackViewAlignment.Center.value
    stack.distribution = 1  # UIStackViewDistributionFillEqually
    stack.spacing = 8.0
    return stack


def _stack_for_cell(cell):
    for subview in cell.contentView.subviews():
        if isinstance(subview, UIStackView):
            return subview
    return None


class TogaTableViewController(UITableViewController):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def tableView_numberOfRowsInSection_(self, tableView, section: int) -> int:
        return len(getattr(self.interface, "data", ()))

    @objc_method
    def tableView_cellForRowAtIndexPath_(self, tableView, indexPath):
        cell = tableView.dequeueReusableCellWithIdentifier("row")
        if cell is None:
            cell = UITableViewCell.alloc().initWithStyle(
                UITableViewCellStyleDefault, reuseIdentifier="row"
            )

        stack = _stack_for_cell(cell)
        if stack is None:
            stack = _row_stack()
            stack.frame = cell.contentView.bounds
            stack.autoresizingMask = (
                UIViewAutoresizing.FlexibleWidth | UIViewAutoresizing.FlexibleHeight
            )
            cell.contentView.addSubview(stack)
        for view in list(stack.arrangedSubviews):
            stack.removeArrangedSubview(view)
            view.removeFromSuperview()

        self.impl._populate_row(stack, indexPath.row)
        return cell

    @objc_method
    def tableView_didSelectRowAtIndexPath_(self, tableView, indexPath):
        self.interface.on_select()

    @objc_method
    def tableView_didDeselectRowAtIndexPath_(self, tableView, indexPath):
        self.interface.on_select()


class Table(Widget):
    def _populate_row(self, stack, row_index):
        data_row = self.interface.data[row_index]
        missing = self.interface.missing_value
        for column in self.interface._columns:
            if column.widget(data_row) is not None:
                warnings.warn(
                    "iOS does not support the use of widgets in cells",
                    stacklevel=2,
                )
            stack.addArrangedSubview(_label(column.text(data_row, missing) or ""))

    def create(self):
        self.native_controller = TogaTableViewController.alloc().init()
        self.native_controller.interface = self.interface
        self.native_controller.impl = self

        self.native = self.native_controller.tableView
        self.native.delegate = self.native_controller
        self.native.dataSource = self.native_controller
        self.native.allowsMultipleSelection = self.interface.multiple_select

        self._rebuild_header()
        self.add_constraints()

    def _rebuild_header(self):
        columns = self.interface._columns
        if not self.interface._show_headings or not columns:
            self.native.tableHeaderView = None
            return

        width = self.native.bounds.size.width or 320.0
        stack = _row_stack()
        stack.frame = CGRect((0, 0), (width, HEADER_HEIGHT))
        stack.autoresizingMask = UIViewAutoresizing.FlexibleWidth
        for column in columns:
            stack.addArrangedSubview(_label(column.heading, bold=True))
        self.native.tableHeaderView = stack

    def change_source(self, source):
        self.native.reloadData()

    def insert(self, index, item):
        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        self.native.reloadData()

    def change(self, item):
        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        self.native.reloadData()

    def remove(self, index, item):
        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
        self.native.reloadData()

    def clear(self):
        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        self.native.reloadData()

    def get_selection(self):
        if self.interface.multiple_select:
            paths = self.native.indexPathsForSelectedRows
            if paths is None:
                return []
            return sorted(int(path.row) for path in paths)

        path = self.native.indexPathForSelectedRow
        return None if path is None else int(path.row)

    def scroll_to_row(self, row):
        data_len = len(self.interface.data)
        if data_len == 0:
            return

        if row < 0:
            index = max(data_len + row, 0)
            position = UITableViewScrollPositionBottom
        elif row == 0:
            index = 0
            position = UITableViewScrollPositionTop
        elif row >= data_len - 1:
            index = min(row, data_len - 1)
            position = UITableViewScrollPositionBottom
        else:
            index = row
            position = UITableViewScrollPositionMiddle

        self.native.scrollToRowAtIndexPath(
            NSIndexPath.indexPathForRow(index, inSection=0),
            atScrollPosition=position,
            animated=False,
        )

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def insert_column(self, index, column):
        self._rebuild_header()
        self.native.reloadData()

    def remove_column(self, index):
        self._rebuild_header()
        self.native.reloadData()
