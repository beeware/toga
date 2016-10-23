from gi.repository import Gtk

from toga.constants import *
from toga.interface import Label as LabelInterface

from .base import WidgetMixin
from ..libs import gtk_alignment


class Label(LabelInterface, WidgetMixin):
    def __init__(self, text, id=None, style=None, alignment=LEFT_ALIGNED):
        super().__init__(id=id, style=style, text=text, alignment=alignment)
        self._create()

    def create(self):
        self._impl = Gtk.Label()
        self._impl.set_line_wrap(False)

        self._impl._interface = self

        self._impl.connect('show', lambda event: self.rehint())

    def _set_alignment(self, value):
        self._impl.set_alignment(*gtk_alignment(self._alignment))

    def _set_text(self, value):
        self._impl.set_text(self._text)

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

        if hints:
            self.style.hint(**hints)
