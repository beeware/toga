from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget
from ..libs import gtk_alignment
from toga.constants import *


class Label(Widget):
    def __init__(self, text=None, alignment=LEFT_ALIGNED):
        super(Label, self).__init__()

        self.text = text

        self.startup()

        self.alignment = alignment

    def startup(self):
        self._impl = Gtk.Label(self.text)
        self._impl.set_line_wrap(False)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        if self._impl:
            self._impl.set_alignment(*gtk_alignment(self._alignment))

