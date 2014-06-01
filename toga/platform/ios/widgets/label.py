from __future__ import print_function, absolute_import, division

from ..libs import UILabel, NSTextAlignment, get_NSString
from .base import Widget
from toga.constants import *


class Label(Widget):
    def __init__(self, text=None, alignment=LEFT_ALIGNMENT):
        super(Label, self).__init__()

        self.text = text
        self._alignment = alignment

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        if self._impl:
            self._impl.textAlignment = NSTextAlignment(self._alignment)

    def _startup(self):
        self._impl = UILabel.new()
        self._impl.setText_(get_NSString(self.text))

        # self._impl.setDrawsBackground_(False)
        # self._impl.setEditable_(False)
        # self._impl.setBezeled_(False)
        print ("TEXT ALIGNMENT", NSTextAlignment(self._alignment))
        self._impl.setTextAlignment_(NSTextAlignment(self._alignment))
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
