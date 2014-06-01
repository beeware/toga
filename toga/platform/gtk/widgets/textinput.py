from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget


class TextInput(Widget):
    def __init__(self, initial=None, placeholder=None):
        super(TextInput, self).__init__()
        self.initial = initial
        self.placeholder = placeholder

    def _startup(self):
        self._impl = Gtk.Entry()
        if self.initial:
            self._impl.set_text(self.initial)
        if self.placeholder:
            self._impl.set_placeholder_text(self.placeholder)

    def value(self):
        return self._impl.get_text()
