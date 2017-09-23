import traceback

from toga.interface import DetailedList as DetailedListInterface

from .base import WidgetMixin
from .table import TogaTable, Table
from ..libs import *


class DetailedList(DetailedListInterface, WidgetMixin):
    def __init__(self, id=None, name=None, data=None, on_delete=None, on_refresh=None, style=None):
        self.headings = [name]
        super().__init__(id=id, data=data, on_delete=on_delete, on_refresh=on_refresh, style=style)
        self._create()

    def _create(self):
        self._data = []
        # Create a table view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.hasVerticalScroller = True
        self._impl.hasHorizontalScroller = False
        self._impl.autohidesScrollers = False
        self._impl.borderType = NSBezelBorder

        self._table = TogaTable.alloc().init()
        self._table._interface = self
        self._table.columnAutoresizingStyle = NSTableViewUniformColumnAutoresizingStyle

        # Use autolayout for the inner widget.
        self._table.translatesAutoresizingMaskIntoConstraints = True

        # Create columns for the table
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier('%d' % i)
            for i, heading in enumerate(self.headings)
        ]

        for heading, column in zip(self.headings, self._columns):
            self._table.addTableColumn(column)
            cell = column.dataCell
            cell.editable = False
            cell.selectable = False
            column.headerCell.stringValue = heading

        self._table.delegate = self._table
        self._table.dataSource = self._table

        # Embed the table view in the scroll view
        self._impl.documentView = self._table

        # Add the layout constraints
        self._add_constraints()

    def _add(self, item):
        self._data.append([item])
