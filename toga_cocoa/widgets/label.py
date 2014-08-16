from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget
from toga.constants import *


class Label(Widget):
    def __init__(self, text=None, alignment=LEFT_ALIGNED):
        super(Label, self).__init__()
        self.text = text

        self.startup()

        self.alignment = alignment

    def startup(self):
        self._impl = NSTextField.new()
        self._impl.setStringValue_(get_NSString(self.text))

        self._impl.setDrawsBackground_(False)
        self._impl.setEditable_(False)
        self._impl.setBezeled_(False)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._impl.setAlignment_(NSTextAlignment(self._alignment))
