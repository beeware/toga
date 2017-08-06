from ..libs import NSTextField, NSTextAlignment
from .base import Widget
from toga.constants import LEFT_ALIGNED


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

    def set_text(self, value):
        self.native.stringValue = value

    def rehint(self):
        # Width & height of a label is known and fixed.
        # print("REHINT label", self, self.native.fittingSize().width, self.native.fittingSize().height)
        fitting_size = self.native.fittingSize()
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width
        )
