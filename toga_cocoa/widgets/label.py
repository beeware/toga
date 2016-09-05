from toga.interface import Label as LabelInterface

from ..libs import NSTextField, NSTextAlignment
from .base import WidgetMixin
from toga.constants import LEFT_ALIGNED


class Label(LabelInterface, WidgetMixin):
    def __init__(self, text, id=None, alignment=LEFT_ALIGNED, style=None):
        super().__init__(text, id=id, alignment=alignment, style=style)
        self.startup()
        self.alignment = alignment
        self.text = text

    def startup(self):
        self._impl = NSTextField.alloc().init()
        self._impl._interface = self

        self._impl.setDrawsBackground_(False)
        self._impl.setEditable_(False)
        self._impl.setBezeled_(False)

        # Width & height of a label is known and fixed.
        self.style.hint(
            height=self._impl.fittingSize().height,
            width=self._impl.fittingSize().width
        )

        # Add the layout constraints
        self._add_constraints()

    def _set_alignment(self, value):
        self._impl.setAlignment_(NSTextAlignment(value))

    def _set_text(self, value):
        self._impl.stringValue = self._text
