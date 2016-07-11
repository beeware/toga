from __future__ import print_function, absolute_import, division, unicode_literals

from ..libs import *
from .base import Widget
from toga.constants import *


class Label(Widget):
    def __init__(self, text=None, alignment=LEFT_ALIGNED, style=None):
        super(Label, self).__init__(style=None)

        self.startup()

        self.alignment = alignment
        self.value = text

    def startup(self):
        self._impl = NSTextField.alloc().init()
        self._impl.interface = self

        self._impl.setDrawsBackground_(False)
        self._impl.setEditable_(False)
        self._impl.setBezeled_(False)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # Width & height of a label is known and fixed.
        self.style.hint(
            height=self._impl.fittingSize().height,
            width=self._impl.fittingSize().width
        )

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._impl.setAlignment_(NSTextAlignment(self._alignment))

    @property
    def value(self):
        return self._impl.stringValue

    @value.setter
    def value(self, value):
        if value:
            self._impl.stringValue = text(value)
