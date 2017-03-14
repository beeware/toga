from toga.interface import Label as LabelInterface

from ..libs import *
from .base import WidgetMixin
from toga.constants import LEFT_ALIGNED


class Label(LabelInterface, WidgetMixin):
    def __init__(self, text, id=None, style=None, alignment=LEFT_ALIGNED):
        super().__init__(id=id, style=style, text=text, alignment=alignment)
        self._create()

    def create(self):
        self._impl = WinForms.Label()

    def _set_alignment(self, value):
        # self._impl.setAlignment_(NSTextAlignment(value))
        pass

    def _set_text(self, value):
        self._impl.Text = self._text

    def rehint(self):
        # Width & height of a label is known and fixed.
        # self._impl.Size = Size(0, 0)
        # print("REHINT label", self, self._impl.PreferredSize)
        self.style.hint(
            height=self._impl.PreferredSize.Height,
            width=self._impl.PreferredSize.Width,
        )
