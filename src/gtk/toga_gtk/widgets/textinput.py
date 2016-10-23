from gi.repository import Gtk

from toga.interface import TextInput as TextInputInterface

from .base import WidgetMixin
from ..utils import wrapped_handler


class TextInput(TextInputInterface, WidgetMixin):
    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False):
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)
        self._create()

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

    def rehint(self):
        # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        hints = {}
        width = self._impl.get_preferred_width()
        minimum_width = width[0]
        natural_width = width[1]

        height = self._impl.get_preferred_height()
        minimum_height = height[0]
        natural_height = height[1]

        if minimum_width > 0:
            hints['min_width'] = minimum_width
        if minimum_height > 0:
            hints['min_height'] = minimum_height
        if natural_height > 0:
            hints['height'] = natural_height

        if hints:
            self.style.hint(**hints)
