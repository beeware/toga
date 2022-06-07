from rubicon.objc import objc_property

import uuid
from toga_cocoa.libs import NSTableColumn, at

from .base import Widget


class Column(Widget):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    def create(self):
        self.native = NSTableColumn.alloc().initWithIdentifier(at(str(uuid.uuid4())))
        self.native.interface = self.interface
        self.native.impl = self

    def set_title(self, value):
        self.native.headerCell.stringValue = value

    def set_editable(self, value):
        self.native.editable = value
