from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga_cocoa.libs import (
    NSIndexSet,
    NSMenu,
    NSTableColumn,
    NSTableView,
    NSTableViewColumnAutoresizingStyle,
)
from toga_cocoa.widgets.base import Widget
from toga_cocoa.widgets.internal.cells import TogaDetailedCell
from toga_cocoa.widgets.internal.data import TogaData
from toga_cocoa.widgets.internal.refresh import RefreshableScrollView


class TogaList(NSTableView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def didCloseMenu_withEvent_(self, menu, event) -> None:
        # When the menu closes, drop the reference to the menu object.
        self.impl._popup = None

    @objc_method
    def menuForEvent_(self, event):
        if self.impl.primary_action_enabled or self.impl.secondary_action_enabled:
            # Find the row under the mouse click
            mousePoint = self.convertPoint(event.locationInWindow, fromView=None)
            row = self.rowAtPoint(mousePoint)

            # Ensure the row is selected.
            self.selectRowIndexes(
                NSIndexSet.indexSetWithIndex(row),
                byExtendingSelection=False,
            )

            # Create a popup menu to display the possible actions.
            popup = NSMenu.alloc().initWithTitle("popup").autorelease()
            if self.impl.primary_action_enabled:
                primary_action_item = popup.addItemWithTitle(
                    self.interface._primary_action,
                    action=SEL("primaryActionOnRow:"),
                    keyEquivalent="",
                )
                primary_action_item.tag = row

            if self.impl.secondary_action_enabled:
                secondary_action_item = popup.addItemWithTitle(
                    self.interface._secondary_action,
                    action=SEL("secondaryActionOnRow:"),
                    keyEquivalent="",
                )
                secondary_action_item.tag = row

        else:
            popup = None

        # Preserve a Python reference to the popup for testing purposes.
        self.impl._popup = popup
        return popup

    @objc_method
    def primaryActionOnRow_(self, menuitem):
        row = self.interface.data[menuitem.tag]
        self.interface.on_primary_action(row=row)

    @objc_method
    def secondaryActionOnRow_(self, menuitem):
        row = self.interface.data[menuitem.tag]
        self.interface.on_secondary_action(row=row)

    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data) if self.interface.data else 0

    @objc_method
    def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
        value = self.interface.data[row]
        try:
            data = value._impl
        except AttributeError:
            data = TogaData.alloc().init()
            value._impl = data

        try:
            title = getattr(value, self.interface.accessors[0])
            if title is not None:
                title = str(title)
            else:
                title = self.interface.missing_value
        except AttributeError:
            title = self.interface.missing_value

        try:
            subtitle = getattr(value, self.interface.accessors[1])
            if subtitle is not None:
                subtitle = str(subtitle)
            else:
                subtitle = self.interface.missing_value
        except AttributeError:
            subtitle = self.interface.missing_value

        try:
            icon = getattr(value, self.interface.accessors[2])._impl.native
        except AttributeError:
            icon = None

        data.attrs = {
            "title": title,
            "subtitle": subtitle,
            "icon": icon,
        }

        return data

    # TableDelegate methods
    @objc_method
    def tableView_heightOfRow_(self, table, row: int) -> float:
        return 48.0

    @objc_method
    def selectionShouldChangeInTableView_(self, table) -> bool:
        # Explicitly allow selection on the table.
        # TODO: return False to disable selection.
        return True

    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        self.interface.on_select()


class DetailedList(Widget):
    def create(self):
        # Create a List, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.

        # Create the List widget
        self.native_detailedlist = TogaList.alloc().init()
        self.native_detailedlist.interface = self.interface
        self.native_detailedlist.impl = self
        self.native_detailedlist.columnAutoresizingStyle = (
            NSTableViewColumnAutoresizingStyle.Uniform
        )
        self.native_detailedlist.allowsMultipleSelection = False

        # Disable all actions by default.
        self.primary_action_enabled = False
        self.secondary_action_enabled = False

        self.native = RefreshableScrollView.alloc().initWithDocument(
            self.native_detailedlist
        )
        self.native.interface = self.interface
        self.native.impl = self

        # Create the column for the detailed list
        column = NSTableColumn.alloc().initWithIdentifier("data")
        self.native_detailedlist.addTableColumn(column)
        self.columns = [column]

        cell = TogaDetailedCell.alloc().init()
        column.dataCell = cell

        # Hide the column header.
        self.native_detailedlist.headerView = None

        self.native_detailedlist.delegate = self.native_detailedlist
        self.native_detailedlist.dataSource = self.native_detailedlist

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.native_detailedlist.reloadData()

    def insert(self, index, item):
        self.native_detailedlist.reloadData()

    def change(self, item):
        self.native_detailedlist.reloadData()

    def remove(self, index, item):
        self.native_detailedlist.reloadData()

        # After deletion, the selection changes, but Cocoa doesn't send
        # a tableViewSelectionDidChange: message.
        self.interface.on_select()

    def clear(self):
        self.native_detailedlist.reloadData()

    def set_refresh_enabled(self, enabled):
        self.native.setRefreshEnabled(enabled)

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def after_on_refresh(self, widget, result):
        self.native.finishedLoading()

    def get_selection(self):
        index = self.native_detailedlist.selectedRow
        if index == -1:
            return None
        else:
            return index

    def scroll_to_row(self, row):
        self.native_detailedlist.scrollRowToVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
