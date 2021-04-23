
import uuid
from toga_cocoa.libs import NSTableColumn, NSTableColumnUserResizingMask, at

from .base import Widget


class Column(Widget):
    def create(self):
        self.native = NSTableColumn.alloc().initWithIdentifier(at(str(uuid.uuid4())))
        self.native.interface = self.interface
        self.native._impl = self

        if self.interface.style.width > 0:
            # disable automatic resizing and set fixed width
            self.native.resizingMask = NSTableColumnUserResizingMask
            self.native.width = self.interface.style.width

    def set_title(self, value):
        self.native.headerCell.stringValue = value

    def set_editable(self, value):
        self.native.editable = value
