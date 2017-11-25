from rubicon.objc import *

from ..libs import *
from .base import Widget
from .internal.cells import TogaDetailedCell
from .internal.data import TogaData
from .internal.refresh import RefreshableScrollView


class TogaDetailedList(NSTableView):
    @objc_method
    def menuForEvent_(self, event):
        if self.interface.on_delete:
            mousePoint = self.convertPoint(event.locationInWindow, fromView=None)
            row = self.rowAtPoint(mousePoint)

            popup = NSMenu.alloc().initWithTitle("popup")
            delete_item = popup.addItemWithTitle("Delete", action=SEL('actionDeleteRow:'), keyEquivalent="")
            delete_item.tag = row
            # action_item = popup.addItemWithTitle("???", action=SEL('actionRow:'), keyEquivalent="")
            # action_item.tag = row

            return popup

    @objc_method
    def actionDeleteRow_(self, menuitem):
        row = self.interface.data[menuitem.tag]
        self.interface.on_delete(self.interface, row=row)

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

        # If the value has an icon attribute, get the _impl.
        # Icons are deferred resources, so we provide the factory.
        try:
            icon = value.icon._impl(self.interface.factory)
        except AttributeError:
            icon = None

        data.attrs = {
            'icon': icon,
            'title': str(getattr(value, 'title')),
            'subtitle': str(getattr(value, 'subtitle')),
        }

        return data

    # TableDelegate methods
    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        self.interface.selection = notification.object.selectedRow
        self.interface.selected = self.interface.data[notification.object.selectedRow]
        if self.interface.on_select:
            row = notification.object.selectedRow if notification.object.selectedRow != -1 else None
            self.interface.on_select(self.interface, row=row)



class DetailedList(Widget):
    def create(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.native = RefreshableScrollView.alloc().init()
        self.native.interface = self.interface
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        # Create the DetailedList widget
        self.detailedlist = TogaDetailedList.alloc().init()
        self.detailedlist.interface = self.interface
        self.detailedlist._impl = self
        self.detailedlist.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle
        self.detailedlist.rowHeight = 48

        self.native.detailedlist = self.detailedlist

        # Create the column for the detailed list
        column = NSTableColumn.alloc().initWithIdentifier('data')
        self.detailedlist.addTableColumn(column)
        self.columns = [column]

        cell = TogaDetailedCell.alloc().init()
        column.dataCell = cell

        cell.editable = False
        cell.selectable = False

        # Hide the column header.
        self.detailedlist.headerView = None

        self.detailedlist.delegate = self.detailedlist
        self.detailedlist.dataSource = self.detailedlist

        # Embed the tree view in the scroll view
        self.native.documentView = self.detailedlist

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.detailedlist.reloadData()

    def insert(self, index, item):
        self.detailedlist.reloadData()

    def change(self, item):
        self.detailedlist.reloadData()

    def remove(self, item):
        self.detailedlist.reloadData()

    def clear(self):
        self.detailedlist.reloadData()

    def set_on_refresh(self, handler):
        pass

    def after_on_refresh(self):
        self.native.finishedLoading()

    def set_on_select(self, handler):
        pass

    def set_on_delete(self, handler):
        pass
