from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget


class MultilineTextInput(Widget):
    def __init__(self, initial=None, readonly=False):
        super(MultilineTextInput, self).__init__()

        self.startup()

        self.readonly = readonly
        self.value = initial

    def startup(self):
        self._buffer = Gtk.TextBuffer()

        if self.initial:
            self._buffer.set_text(self.initial)

        self._impl = Gtk.TextView()
        self._impl.set_buffer(self._buffer)

    @property
    def _width_hint(self):
        print ("WIDGET WIDTH", self, self._impl.get_preferred_width())
        return self._impl.get_preferred_width()

    @property
    def _height_hint(self):
        print ("WIDGET HEIGHT", self, self._impl.get_preferred_height())
        return self._impl.get_preferred_height()

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.editable = not self._readonly

    @property
    def value(self):
        # FIXME??
        return self._buffer.get_text(None, None, True)

    @value.setter
    def value(self, value):
        self._buffer.set_text(value)
