from gi.repository import Gtk

from toga.interface import TextInput as TextInputInterface

from .base import WidgetMixin
from ..utils import wrapped_handler


class TextInput(TextInputInterface, WidgetMixin):
    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False):
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)
        self._create()

        # Text inputs have a fixed drawn height.
        self._expand_vertical = False

    def create(self):
        self._impl = Gtk.Entry()
        self._impl._interface = self

        self._impl.connect('show', lambda event: self.rehint())

    def _set_readonly(self, value):
        self._impl.editable = not value

    def _get_value(self):
        return self._impl.get_text()

    def _set_value(self, value):
        self._impl.set_text(value)

    def _set_placeholder(self, value):
        self._impl.set_placeholder_text(self._placeholder)
