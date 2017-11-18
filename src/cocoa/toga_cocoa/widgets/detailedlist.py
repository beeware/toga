from rubicon.objc import *

from ..libs import *
from .base import Widget
from .table import TogaTable
from .utils import TogaIconCell, TogaData


NSBezierPath = ObjCClass('NSBezierPath')


class TogaDisplayListCell(NSTextFieldCell):
    @objc_method
    # def drawWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
    def drawInteriorWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
        # The data to display.
        label1 = self.objectValue.attrs['label1']
        label2 = self.objectValue.attrs['label2']
        icon = self.objectValue.attrs['icon']

        if icon:
            nicon = icon.native

            NSGraphicsContext.currentContext.saveGraphicsState()
            yOffset = cellFrame.origin.y
            if view.isFlipped:
                xform = NSAffineTransform.transform()
                xform.translateXBy(4, yBy=cellFrame.size.height)
                xform.scaleXBy(1.0, yBy=-1.0)
                xform.concat()
                yOffset = 0.5 - cellFrame.origin.y

            interpolation = NSGraphicsContext.currentContext.imageInterpolation
            NSGraphicsContext.currentContext.imageInterpolation = NSImageInterpolationHigh

            nicon.drawInRect(
                NSRect(NSPoint(cellFrame.origin.x, yOffset + 4), NSSize(40.0, 40.0)),
                fromRect=NSRect(NSPoint(0, 0), NSSize(nicon.size.width, nicon.size.height)),
                operation=NSCompositingOperationSourceOver,
                fraction=1.0
            )

            NSGraphicsContext.currentContext.imageInterpolation = interpolation
            NSGraphicsContext.currentContext.restoreGraphicsState()
        else:
            path = NSBezierPath.bezierPathWithRect(
                NSRect(NSPoint(cellFrame.origin.x, cellFrame.origin.y + 4), NSSize(40.0, 40.0))
            )
            NSColor.grayColor.set()
            path.fill()

        if label1:
            # Find the right color for the text
            if self.isHighlighted():
                primaryColor = NSColor.alternateSelectedControlTextColor
            else:
                if False:
                    primaryColor = NSColor.disabledControlTextColor
                else:
                    primaryColor = NSColor.textColor

            textAttributes = NSMutableDictionary.alloc().init()
            textAttributes[NSForegroundColorAttributeName] = primaryColor
            textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(13)

            at(label1).drawAtPoint(
                NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 4),
                withAttributes=textAttributes
            )

        if label2:
            # Find the right color for the text
            if self.isHighlighted():
                primaryColor = NSColor.alternateSelectedControlTextColor
            else:
                if False:
                    primaryColor = NSColor.disabledControlTextColor
                else:
                    primaryColor = NSColor.textColor

            textAttributes = NSMutableDictionary.alloc().init()
            textAttributes[NSForegroundColorAttributeName] = primaryColor
            textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(15)

            at(label2).drawAtPoint(
                NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 26),
                withAttributes=textAttributes
            )


class TogaDetailedList(NSTableView):
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
            'label1': str(getattr(value, 'label1')),
            'label2': str(getattr(value, 'label2')),
            'icon': icon,
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
        self.native = NSScrollView.alloc().init()
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

        # Create the column for the detailed list
        column = NSTableColumn.alloc().initWithIdentifier('data')
        self.detailedlist.addTableColumn(column)
        self.columns = [column]

        cell = TogaDisplayListCell.alloc().init()
        column.dataCell = cell

        cell.editable = False
        cell.selectable = False

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

    def set_on_select(self, handler):
        pass

    def set_on_delete(self, handler):
        pass
