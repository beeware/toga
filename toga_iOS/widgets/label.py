from __future__ import print_function, absolute_import, division

from ..libs import UILabel, NSTextAlignment, get_NSString
from .base import Widget
from toga.constants import *


class Label(Widget):
    def __init__(self, text=None, alignment=LEFT_ALIGNED):
        super(Label, self).__init__()

        self.text = text

        self.startup()

        self.alignment = alignment

    def startup(self):
        self._impl = UILabel.new()
        self._impl.setText_(get_NSString(self.text))

        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._impl.setTextAlignment_(NSTextAlignment(self._alignment))
