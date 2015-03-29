from __future__ import print_function, absolute_import, division, unicode_literals

from ..libs import *
from .base import Widget
from toga.constants import *
from .textinput import TextFieldImpl


class Label(Widget):
    def __init__(self, text=None, alignment=LEFT_ALIGNED):
        super(Label, self).__init__()
        self.text = text

        self.startup()

        self.alignment = alignment

    def startup(self):
        self._impl = TextFieldImpl.alloc().init()
        self._impl.__dict__['interface'] = self
        self._impl.setStringValue_(self.text)

        self._impl.setDrawsBackground_(False)
        self._impl.setEditable_(False)
        self._impl.setBezeled_(False)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Width & height of a label is known and fixed.
        self.style(width=self._impl.fittingSize().width)
        self.style(height=self._impl.fittingSize().height)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._impl.setAlignment_(NSTextAlignment(self._alignment))
