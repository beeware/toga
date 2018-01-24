from travertino.size import at_least

from toga_cocoa.color import native_color
from toga_cocoa.libs import NSTextField, NSTextAlignment

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = NSTextField.alloc().init()
        self.native.impl = self
        self.native.interface = self.interface

        self.native.drawsBackground = False
        self.native.editable = False
        self.native.bezeled = False

        # Add the layout constraints
        self.add_constraints()

    def set_alignment(self, value):
        self.native.alignment = NSTextAlignment(value)

    def set_color(self, value):
        if value:
            self.native.textColor = native_color(value)

    def set_font(self, value):
        if value:
            self.native.font = value._impl.native

    def set_text(self, value):
        self.native.stringValue = self.interface._text

    def rehint(self):
        # Width & height of a label is known and fixed.
        # print("REHINT label", self, self.native.fittingSize().width, self.native.fittingSize().height)
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height
