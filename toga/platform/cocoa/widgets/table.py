from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget


class TableImpl_impl(object):
    TableImpl = ObjCSubclass('NSTableView', 'TableImpl')

    # TableDataSource methods
    @TableImpl.method('i@')
    def numberOfRowsInTableView_(self, table):
        return 100

    @TableImpl.method('@@@i')
    def tableView_objectValueForTableColumn_row_(self, table, column, row):
        return get_NSString('Data %d' % row)

    # TableDelegate methods
    @TableImpl.method('v@')
    def tableViewSelectionDidChange_(self, notification):
        print ("selection changed")

TableImpl = ObjCClass('TableImpl')


class Table(Widget):
    def __init__(self, headings):
        super(Table, self).__init__()
        self.headings = headings

        self._impl = None
        self._table = None
        self._columns = None

    def _startup(self):
        # Create a table view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(True)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._table = TableImpl.alloc().init()
        self._table.interface = self
        self._table.setColumnAutoresizingStyle_(NSTableViewUniformColumnAutoresizingStyle)

        # Create columns for the table
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier_(get_NSString('col-%d' % i))
            for i, heading in enumerate(self.headings)
        ]

        for heading, column in zip(self.headings, self._columns):
            self._table.addTableColumn_(column)
            column.headerCell.setStringValue_(get_NSString(heading))

        self._table.setDelegate_(self._table)
        self._table.setDataSource_(self._table)

        # Embed the table view in the scroll view
        self._impl.setDocumentView_(self._table)
