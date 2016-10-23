from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget
from toga.constants import *


class ProgressBar(Widget):
    def __init__(self, max=None, value=None):
        super(ProgressBar, self).__init__()

        self.max = max
        self._running = True
        self._value = value
    
        self.startup()

    def startup(self):
        self._impl = Gtk.ProgressBar()

        if self._running:
            self._impl.set_fraction(float(self._value) / float(self.max))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._running = self._value is not None
        self._impl.set_fraction(float(value) / float(self.max))

    def start(self):
        if not self._running:
            self._running = True

    def stop(self):
        if self._running:
            self._running = False
