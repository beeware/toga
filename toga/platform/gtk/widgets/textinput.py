from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget


class TextInput(Widget):
    def __init__(self, initial=None, placeholder=None, readonly=False):
        super(TextInput, self).__init__()
        self.placeholder = placeholder

        self.startup()

        self.value = initial
        self.readonly = readonly

    def startup(self):
        self._impl = Gtk.Entry()
        if self.placeholder:
            self._impl.set_placeholder_text(self.placeholder)

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.editable = not self._readonly

    @property
    def value(self):
        return self._impl.get_text()

    @value.setter
    def value(self, value):
        self._impl.set_text(unicode(value))
