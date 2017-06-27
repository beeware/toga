from ..libs import NSTextField, NSTextAlignment
from .base import Widget
from toga.constants import LEFT_ALIGNED


class Label(Widget):

    def create(self):
        self._native = NSTextField.alloc().init()
        self._native._impl = self
        self._native._interface = self._interface

        self._native.setDrawsBackground_(False)
        self._native.setEditable_(False)
        self._native.setBezeled_(False)

        # Add the layout constraints
        self.add_constraints()

    def set_alignment(self, value):
        self._native.setAlignment_(NSTextAlignment(value))

    def set_text(self, value):
        self._native.stringValue = value

    def rehint(self):
        # Width & height of a label is known and fixed.
        # print("REHINT label", self, self._native.fittingSize().width, self._native.fittingSize().height)
        self._interface.style.hint(
            height=self._native.fittingSize().height,
            width=self._native.fittingSize().width
        )
