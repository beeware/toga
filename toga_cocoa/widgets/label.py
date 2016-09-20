from toga.interface import Label as LabelInterface

from ..libs import NSTextField, NSTextAlignment
from .base import WidgetMixin
from toga.constants import LEFT_ALIGNED


class Label(LabelInterface, WidgetMixin):
    def __init__(self, text, id=None, style=None, alignment=LEFT_ALIGNED):
        super().__init__(id=id, style=style, text=text, alignment=alignment)
        self._create()

    def create(self):
        self._impl = NSTextField.alloc().init()
        self._impl._interface = self

        self._impl.setDrawsBackground_(False)
        self._impl.setEditable_(False)
        self._impl.setBezeled_(False)

        # Add the layout constraints
        self._add_constraints()

    def _set_alignment(self, value):
        self._impl.setAlignment_(NSTextAlignment(value))

    def _set_text(self, value):
        self._impl.stringValue = self._text

    def rehint(self):
        # Width & height of a label is known and fixed.
        # print("REHINT label", self, self._impl.fittingSize().width, self._impl.fittingSize().height)
        self.style.hint(
            height=self._impl.fittingSize().height,
            width=self._impl.fittingSize().width
        )
